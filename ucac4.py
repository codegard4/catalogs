import pymysql 
from tqdm import tqdm
import argparse
import os
import sys, math
import datetime
import os.path
import numpy as np
import pandas as pd
import struct
import random
import configparser

def connectionParameters():
    #Returns the host, port, user and pw of the mySQL database to connect to
    config = configparser.ConfigParser()
    config.read('catalogs.conf')
    db_host = config['UCAC4']['host']
    db_port = int(config['UCAC4']['port'])
    db_user = config['UCAC4']['user']
    db_password = config['UCAC4']['password']
    return db_host, db_port, db_user, db_password

def connectToDatabase(db_name = None):
    #returns a connection to the database
    db_host,db_port,db_user,db_password = connectionParameters()
    if (db_name == None):
        conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password)
    else:
        conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, database = db_name)
    return conn

def getOffsets(zoneNr):
    #Retrieves file offsets from the UCAC offsets file
    fileName = "%s/u4i/z%03d.idx" % ("../ucac4/", zoneNr)
    with open(fileName, "rb") as fh:
        out = [0] * 360
        for line in fh:
            if not line:
                break
            parts = line.strip().split()
            i = int(parts[0])
            if i >= 360:
                continue
            out[i] = int(parts[1])
        return out
        
def checkMag(mag):
    #Changes blank magnitude values to NULL
    if mag >= 20000:
        return None
    return mag / 1000
    
def createDatabase(databaseName = "UCAC4_dev"): 
    #Creates the UCAC4 database if it doesnt already exist
    try:
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f'CREATE DATABASE {databaseName} ;')
        conn.commit()
        conn.close()
    except:
        print("DB already created")
    
def createTable(databaseName = "UCAC4_dev", tableName = "ucac4"): 
    #Creates the specified table
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE {tableName} (UCAC_ID INT PRIMARY KEY);')
    if(tableName == 'ucac4' or tableName == 'ucac4_not_visible'):
        query = f"""ALTER TABLE {tableName} ADD 2MASS_ID INT, ADD RA VARCHAR(14), ADD Decl VARCHAR(14), \
                ADD RA_deg FLOAT, ADD Decl_deg FLOAT, \
                ADD RA_orig INT, ADD Decl_orig INT, \
                ADD MagModel FLOAT, ADD MagApperature FLOAT, \
                ADD Objt INT, \
                ADD Cdf INT, \
                ADD SigRA INT, ADD SigDec INT, \
                ADD CepRA INT, ADD CepDec INT, \
                ADD PmRA FLOAT, ADD PmDec FLOAT, \
                ADD SigPmRA INT, ADD SigPmDec INT, \
                ADD 2MASS_J FLOAT, ADD 2MASS_H FLOAT, ADD 2MASS_K FLOAT, \
                ADD APASS_B FLOAT, ADD APASS_V FLOAT, ADD APASS_g FLOAT, \
                ADD APASS_r FLOAT, ADD APASS_i FLOAT; \
                """
    elif(tableName == 'ucac4_errors_flags' or tableName == 'ucac4_errors_flags_not_visible'):
        query = f"""ALTER TABLE {tableName} ADD SigMag FLOAT, \
                ADD Na1 INT, ADD Nu1 INT, ADD Cu1 INT, \
                ADD icqflg_J INT, ADD icqflg_H INT, ADD icqflg_K INT, \
                ADD e2mpho_J INT, ADD e2mpho_H INT, ADD e2mpho_K INT, \
                ADD APASS_B_err INT, ADD APASS_V_err INT, ADD APASS_g_err INT, \
                ADD APASS_r_err INT, ADD APASS_i_err INT, \
                ADD gcflg INT, \
                ADD icf VARCHAR(20), \
                ADD leda INT, ADD x2m INT, \
                ADD zn2 INT, ADD rn2 INT; \
                """
    cur.execute(query)
    conn.commit()
    conn.close()

def viewTable(databaseName = "UCAC4_dev", tableName = "ucac4"):
    #queries the database for the table specified
    try:
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {tableName};')
        table = cur.fetchall()
        conn.commit()
        conn.close()
        return table
    except:
        print("Cannot View: That table doesn't exist")

    
def insertTable(databaseName = "UCAC4_dev", fileNum = 1, tableNames = ['ucac4', 'ucac4_errors_flags', 'ucac4_not_visible', 'ucac4_errors_flags_not_visible'], path = "u4b"):  
    #Inserts data from the z*filenum* file 
    #ex: fileNum:1 would insert data from z001 file
    try:
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        fileName = "{:>03}".format(fileNum)
        if(fileNum < 100):
            loc = 2
        else:
            loc = 0
        sql = f"""INSERT INTO {tableNames[loc]} (UCAC_ID, 2MASS_ID, \
                RA, Decl, RA_deg, Decl_deg, RA_orig, Decl_orig, MagModel, MagApperature, Objt, \
                Cdf, SigRA, SigDec, CepRA, CepDec, PmRA, PmDec, SigPmRA, SigPmDec, \
                2MASS_J, 2MASS_H, 2MASS_K, APASS_B, APASS_V, APASS_g, APASS_r, APASS_i) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); 
            """
        sql_ef = f"""INSERT INTO {tableNames[loc+1]} (UCAC_ID, SigMag, \
                    Na1, Nu1, Cu1, icqflg_J, icqflg_H, icqflg_K, e2mpho_J, e2mpho_H, e2mpho_K, \
                    APASS_B_err, APASS_V_err, APASS_g_err, APASS_r_err, APASS_i_err, gcflg, \
                    icf, leda, x2m, zn2, rn2) \
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);  
                """
        with open(f'{path}/z{fileName}', 'rb') as f:
            offsets = getOffsets(fileNum)  
            f.seek(offsets[int(fileNum*0.2)] * 78, 0)
            ok = True
            incr = ""
            while ok:
                record = f.read(78)
                if not record:
                    break
                raw = struct.unpack("<iiHHBBB" + "bbBBBHH" + "hhbb" + "IHHHBBBBBBHHHHHbbbbbb" + "IbbIHI", record)
                tMASS_pts_key = raw[18]
                if(tMASS_pts_key == 0):
                    tMASS_pts_key = None
                RA_orig = raw[0]
                Decl_orig = raw[1]
                MagModel = checkMag(raw[2])
                MagApperature = checkMag(raw[3])
                Objt = raw[5]
                Cdf= raw[6]
                SigRA= raw[7]
                SigDec= raw[8]
                CepRA= raw[12]
                CepDec= raw[13]
                PmRA= raw[14]
                PmDec= raw[15]
                SigPmRA= raw[16]
                SigPmDec= raw[17]
                tMASS_J= checkMag(raw[19]) 
                tMASS_H= checkMag(raw[20]) 
                tMASS_K= checkMag(raw[21]) 
                APASS_B= checkMag(raw[28])
                APASS_V= checkMag(raw[29])
                APASS_g= checkMag(raw[30])
                APASS_r= checkMag(raw[31])
                APASS_i = checkMag(raw[32])
                RA_deg = RA_orig / 1000 / 3600 
                Dec_deg = Decl_orig / 1000 / 3600 - 90
                RA = deg2SexagHrs(RA_deg)
                Decl = deg2Sexag(Dec_deg)
                PmRA /= 10000 * 15
                PmDec /= 10000
                Sigmag = raw[4]
                Na1 = raw[9]
                Nu1 = raw[10]
                Cu1 = raw[11]
                icqflg_J = raw[22]
                icqflg_H = raw[23]
                icqflg_K = raw[24]
                e2mpho_J = raw[25]
                e2mpho_H = raw[26]
                e2mpho_K = raw[27]
                APASS_B_err = raw[33]
                APASS_V_err = raw[34]
                APASS_g_err = raw[35]
                APASS_r_err = raw[36]
                APASS_i_err = raw[37]
                if(APASS_B_err == 99):
                    APASS_B_err = None
                if(APASS_V_err == 99):
                    APASS_V_err = None
                if(APASS_g_err == 99):
                    APASS_g_err = None
                if(APASS_r_err == 99):
                    APASS_r_err = None
                if(APASS_i_err == 99):
                    APASS_i_err = None
                gcflg = raw[38]
                icf = raw[39]
                leda = raw[40]
                x2m = raw[41]
                rnm = raw[42]
                zn2 = raw[43]
                rn2 = raw[44]
                cur.execute(sql,(rnm, tMASS_pts_key, RA, Decl,
                RA_deg, Dec_deg, RA_orig, Decl_orig, MagModel, MagApperature, Objt, Cdf, SigRA, SigDec,
                CepRA, CepDec, PmRA, PmDec, SigPmRA, SigPmDec, tMASS_J, tMASS_H, tMASS_K,
                APASS_B, APASS_V, APASS_g, APASS_r, APASS_i))
                cur.execute(sql_ef,(rnm, Sigmag,
                Na1, Nu1, Cu1, icqflg_J, icqflg_H, icqflg_K, e2mpho_J, e2mpho_H, e2mpho_K,
                APASS_B_err, APASS_V_err, APASS_g_err, APASS_r_err, APASS_i_err,
                gcflg, icf, leda, x2m, zn2, rn2))
    except Exception as e: 
        print(e)         
    conn.commit()
    conn.close()
                    
def deg2Sexag(deg):
    #converts degrees to sexagesimal format (degs:mins:secs)
    sign = " "
    if deg < 0:
        sign = "-"
        deg = -deg
    dd = int(deg)
    rest = (deg - dd) * 60
    mm = int(rest)
    rest = (rest - mm) * 60
    ss = int(rest)
    rest = (rest - ss) * 1000
    ms = int(rest)
    return "%c%02d:%02d:%02d.%03d" % (sign, dd, mm, ss, ms)   
    
def deg2SexagHrs(deg):
    #converts degrees to sexagesimal format for RA (hrs:mins:secs)
    deg = (deg / 360) * 24
    hrs = int(deg)
    rest = (deg - hrs) * 60
    mins = int(rest)
    rest = (rest - mins) * 60
    secs = int(rest)
    rest = (rest - secs) * 1000
    ms = int(rest)
    return "%02d:%02d:%02d.%03d" % (hrs, mins, secs, ms)   
    
def radToDeg(radians):
    #converst radians to degrees
    return math.degrees(radians)
        

def dropTable(databaseName = "UCAC4", tableName = "ucac4"):
    #deletes the table specified
    try: 
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f"DROP TABLE {tableName};")
        conn.commit()
        conn.close()
    except Exception as e: 
        print(e)
        
def killConnections(databaseName = "UCAC4_dev"):
    #closes open connections
    #used to make sure that any open connections are closed so that the following SQL commands will run
    #(when a function breaks before running the connection will not close)
    try: 
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f"SELECT CONCAT('KILL', id, ';') FROM INFORMATION_SCHEMA.PROCESSLIST WHERE 'user' = 'vm-internship.keck.hawaii.edu';")
        conn.commit()
        conn.close()
        print("successful")
    except:
        pass

def parseArguments(in_args):
    description = "Reads star files into mySQL DB"
    usage = "\n{} [-d databaseName] \n".format(in_args[0])
    epilog = ""
    parser = argparse.ArgumentParser(description=description, usage=usage, epilog=epilog)
    parser.add_argument("-d", "--databaseName", dest="dName", type=str, help="Name of the database to insert the tables into (default = 'UCAC4_dev')", default="UCAC4_dev")
    parser.add_argument("-n", "--NumFiles", dest="fNum", type=int, help="Number of files to insert into the database (default = 900)", default=900)
    parser.add_argument("-f", "--filePath", dest="fPath", type=str, help="location of the u4b folder", default="u4b")
    parser.add_argument("-t", "--tableNames", dest="tNames", type=list, help="names of the tables (default = [ucac4,ucac4_errors_flags,ucac4_errors_flags_not_visible,ucac4_not_visible])", default=['ucac4', 'ucac4_errors_flags', 'ucac4_not_visible', 'ucac4_errors_flags_not_visible'])
    parser.add_argument("-r", "--randomInsertion", dest="rIns", type=bool, help="Randomly select files to insert? (default = F)", default=False)
    args = None
    try:
        args = parser.parse_args(in_args[1:])
    except Exception as e:
        print(e)
        parser.print_help()
        sys.exit(0) 
    return args 

def ingestDB():
    args = parseArguments(sys.argv)
    killConnections()
    createDatabase(args.dName)
    for i in range(len(args.tNames)):
        dropTable(databaseName = args.dName, tableName = args.tNames[i])
        createTable(databaseName = args.dName, tableName = args.tNames[i])
        print(args.tNames[i])
    if(args.rIns):
        nums = random.sample(range(1, 900), args.fNum)
    else:
        nums = np.arange(1,900,int(900/args.fNum))
    for i in tqdm(range(1,args.fNum+1)):
        insertTable(databaseName = args.dName, fileNum = nums[i-1], tableNames = args.tNames, path = args.fPath)
    print(f"Zone Files Inserted: {nums}")
    
    
if __name__ == "__main__":
    ingestDB()