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
import csv

def connectionParameters():
    #Returns the host, port, user and pw of the mySQL database to connect to
    config = configparser.ConfigParser()
    config.read('catalogs.conf')
    db_host = config['GSC240']['host']
    db_port = int(config['GSC240']['port'])
    db_user = config['GSC240']['user']
    db_password = config['GSC240']['password']
    return db_host, db_port, db_user, db_password

def connectToDatabase(db_name = None):
    #returns a connection to the database
    db_host,db_port,db_user,db_password = connectionParameters()
    if (db_name == None):
        conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password)
    else:
        conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, database = db_name)
    return conn
        
def cnm(mag):
    #Checks null mag values and changes 99.9 vals to NULL
    if mag == 99.9:
        return None
    return mag

def cnc(code):
    #Checks null code values and changes 99 vals to NULL
    if code == 99:
        return None
    return code
    
def createDatabase(databaseName = "GSC240_dev"): 
    #Creates the GSC240 database if it doesnt already exist
    try:
        conn = connectToDatabase()
        cur = conn.cursor()
        cur.execute(f'CREATE DATABASE {databaseName} ;')
        conn.commit()
        conn.close()
        print(f"DB {databaseName} created")
    except:
        pass
        # print("DB already created")
    
def createTable(databaseName = "GSC240_dev", tableName = "gsc240"): 
    #Creates the specified table
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE {tableName} (GSCID INT PRIMARY KEY);')
    if(tableName == 'gsc240' or tableName == 'gsc240_not_visible'):
        query = f"""ALTER TABLE {tableName}\
            ADD GSC1ID VARCHAR(11),\
            ADD HSTID VARCHAR(11),\
            ADD RA VARCHAR(13),\
            ADD Decl VARCHAR(13),\
            ADD RA_rad DOUBLE,\
            ADD Decl_rad DOUBLE,\
            ADD RA_deg DOUBLE,\
            ADD Decl_deg DOUBLE,\
            ADD Original_Epoch REAL,\
            ADD RA_eps REAL,\
            ADD Decl_eps REAL,\
            ADD PmRA REAL,\
            ADD PmDec REAL,\
            ADD Delta_Epoch REAL,\
            ADD FpgMag REAL,\
            ADD JpgMag REAL,\
            ADD VMag REAL,\
            ADD NpgMag REAL,\
            ADD UMag REAL,\
            ADD BMag REAL,\
            ADD RMag REAL,\
            ADD IMag REAL,\
            ADD JMag REAL,\
            ADD HMag REAL,\
            ADD KMag REAL,\
            ADD Classification INT,\
            ADD SemiMajorAxis REAL,\
            ADD Eccentricity REAL,\
            ADD PositionAngle REAL,\
            ADD SourceStatus INT;\
            """
        cur.execute(query)
    elif(tableName == 'gsc240_errors_flags' or tableName == 'gsc240_errors_flags_not_visible'):
        query = f"""ALTER TABLE {tableName}\
            ADD GSC1ID VARCHAR(11), \
            ADD HSTID VARCHAR(11), \
            ADD PmRA_mu REAL, \
            ADD PmDec_mu REAL, \
            ADD FpgMag_err REAL, \
            ADD FpgMag_code INT, \
            ADD JpgMag_err REAL, \
            ADD JpgMag_code INT, \
            ADD VMag_err REAL, \
            ADD VMag_code INT, \
            ADD NpgMag_err REAL, \
            ADD NpgMag_code INT, \
            ADD UMag_err REAL, \
            ADD UMag_code INT, \
            ADD BMag_err REAL, \
            ADD BMag_code INT, \
            ADD RMag_err REAL, \
            ADD RMag_code INT, \
            ADD IMag_err REAL, \
            ADD IMag_code INT, \
            ADD JMag_err REAL, \
            ADD JMag_code INT, \
            ADD HMag_err REAL, \
            ADD HMag_code INT, \
            ADD KMag_err REAL, \
            ADD KMag_code INT, \
            ADD VariableFlag INT, \
            ADD MultipleFlag INT;\
            """
        cur.execute(query)
    conn.commit()
    conn.close()

def viewTable(databaseName = "GSC240_dev", tableName = "gsc240"):
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

    
def insertTable(databaseName = "GSC240_dev", tableNames = ['gsc240', 'gsc240_errors_flags', 'gsc240_not_visible', 'gsc240_errors_flags_not_visible'], path = "csv", dec1="000", dec2="0000", ra="000"):  
    #Inserts data from the dec1 dec2 ra file
    #ex: 1,1,1 would go to the 001 dec directory and then the 001 dec decimal directory and then the 001 RA directory and insert those stars
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor() 
    try:
        if(int(dec1) < 20):
            loc = 2
        else:
            loc = 0
        sql = f"""INSERT INTO {tableNames[loc]} ( \
                GSCID, GSC1ID, HSTID, RA, Decl, RA_rad, Decl_rad, RA_deg, Decl_deg, Original_Epoch, \
                RA_eps, Decl_eps, PmRA, PmDec, Delta_Epoch, \
                FpgMag, JpgMag, VMag, NpgMag, UMag, BMag, RMag, IMag, JMag, HMag, \
                KMag, Classification, SemiMajorAxis, Eccentricity, PositionAngle, SourceStatus) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  \
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); \
            """
        sql_ef= f"""INSERT INTO {tableNames[loc+1]} ( \
                GSCID, GSC1ID, HSTID, PmRA_mu, PmDec_mu, FpgMag_err, \
                FpgMag_code, JpgMag_err, JpgMag_code, VMag_err, VMag_code, \
                NpgMag_err, NpgMag_code, UMag_err, UMag_code, BMag_err, \
                BMag_code, RMag_err, RMag_code, IMag_err, IMag_code, \
                JMag_err, JMag_code, HMag_err, HMag_code, KMag_err, \
                KMag_code, VariableFlag, MultipleFlag)\
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);\
            """
        file = f"{dec1}/{dec2}/{ra}.csv"
        with open(f'{path}/{file}', 'r') as f:
            csvFile = csv.reader(f)
            for line in csvFile:
                # print(line)
                GSCID = line[0]
                GSC1ID = str(line[1])
                if(GSC1ID == "___NULL___"):
                    GSC1ID = None
                HSTID = line[2]
                RA_rad = float(line[3])
                Decl_rad = float(line[4])
                RA_deg = radToDeg(RA_rad)
                Decl_deg = radToDeg(Decl_rad)
                RA = deg2SexagHrs(RA_deg)
                Decl = deg2Sexag(Decl_deg)
                Original_Epoch = line[5]
                RA_eps = line[6]
                Decl_eps = line[7]
                PmRA = cnm(float(line[8]))
                PmDec = cnm(float(line[9]))
                Delta_Epoch = line[12]
                FpgMag = cnm(float(line[13]))
                JpgMag = cnm(float(line[16]))
                VMag = cnm(float(line[19]))
                NpgMag = cnm(float(line[22]))
                UMag = cnm(float(line[25]))
                BMag = cnm(float(line[28]))
                RMag = cnm(float(line[31]))
                IMag = cnm(float(line[34]))
                JMag = cnm(float(line[37]))
                HMag = cnm(float(line[40]))
                KMag = cnm(float(line[43]))
                Classification = line[46]
                SemiMajorAxis = line[47]
                Eccentricity = line[48]
                PositionAngle = line[49]
                SourceStatus = line[50]
                #gsc240_errors_flags
                PmRA_mu = cnm(float(line[10]))
                PmDec_mu = cnm(float(line[11]))
                FpgMag_err = cnm(float(line[14]))
                FpgMag_code = cnc(int(line[15]))
                JpgMag_err = cnm(float(line[17]))
                JpgMag_code = cnc(int(line[18]))
                VMag_err = cnm(float(line[20]))
                VMag_code = cnc(int(line[21]))
                NpgMag_err = cnm(float(line[23]))
                NpgMag_code = cnc(int(line[24]))
                UMag_err = cnm(float(line[26]))
                UMag_code = cnc(int(line[27]))
                BMag_err = cnm(float(line[29]))
                BMag_code = cnc(int(line[30]))
                RMag_err = cnm(float(line[32]))
                RMag_code = cnc(int(line[33]))
                IMag_err = cnm(float(line[35]))
                IMag_code = cnc(int(line[36]))
                JMag_err = cnm(float(line[38]))
                JMag_code = cnc(int(line[39]))
                HMag_err = cnm(float(line[41]))
                HMag_code = cnc(int(line[42]))
                KMag_err = cnm(float(line[44]))
                KMag_code = cnc(int(line[45]))
                VariableFlag = line[51]
                MultipleFlag = line[52]
                cur.execute(sql,(
                    GSCID, GSC1ID, HSTID, RA, Decl, RA_rad, Decl_rad, 
                    RA_deg, Decl_deg, Original_Epoch, RA_eps, Decl_eps, 
                    PmRA, PmDec, Delta_Epoch, FpgMag, JpgMag, VMag, 
                    NpgMag, UMag, BMag, RMag, IMag, JMag, HMag, KMag, 
                    Classification, SemiMajorAxis, Eccentricity, PositionAngle, SourceStatus))
                cur.execute(sql_ef,(
                    GSCID, GSC1ID, HSTID, PmRA_mu, PmDec_mu,
                    FpgMag_err, FpgMag_code, JpgMag_err, JpgMag_code,
                    VMag_err, VMag_code, NpgMag_err, NpgMag_code,
                    UMag_err, UMag_code, BMag_err, BMag_code,
                    RMag_err, RMag_code, IMag_err, IMag_code,
                    JMag_err, JMag_code, HMag_err, HMag_code,
                    KMag_err, KMag_code, VariableFlag, MultipleFlag))
    except Exception as e:
        pass
        # print(e)   
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
        

def dropTable(databaseName = "GSC240_dev", tableName = "gsc240"):
    #deletes the table specified
    try: 
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f"DROP TABLE {tableName};")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        
def killConnections(databaseName = "GSC240_dev"):
    #closes open connections
    #used to make sure that any open connections are closed so that the following SQL commands will run
    #(when a function breaks before running the connection will not close)
    try:
        host,_,user,_ = connectionParameters()
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f"SELECT CONCAT('KILL ', id, ';') FROM INFORMATION_SCHEMA.PROCESSLIST WHERE user = '{user}';")
        kills = cur.fetchall()
        for kill in kills:
            # print(kill[0])
            cur.execute(str(kill[0]))
        conn.commit()
        conn.close()
    except:
        pass

def parseArguments(in_args):
    description = "Reads star files into mySQL DB"
    usage = "\n{} [-d databaseName] \n".format(in_args[0])
    epilog = ""
    parser = argparse.ArgumentParser(description=description, usage=usage, epilog=epilog)
    parser.add_argument("-d", "--databaseName", dest="dName", type=str, help="Name of the database to insert the tables into (default = 'GSC240_dev')", default="GSC240_dev")
    parser.add_argument("-n", "--NumDec", dest="fNum", type=int, help="Number of Dec files to insert into the database (default = 180)", default=180)
    parser.add_argument("-f", "--filePath", dest="fPath", type=str, help="location of the gsc240 csv folder", default="../gsc240/csv")
    parser.add_argument("-t", "--tableNames", dest="tNames", type=list, help="names of the tables (default = ['gsc240', 'gsc240_errors_flags', 'gsc240_not_visible', 'gsc240_errors_flags_not_visible'])", default=['gsc240', 'gsc240_errors_flags', 'gsc240_not_visible', 'gsc240_errors_flags_not_visible'])
    parser.add_argument("-r", "--randomInsertion", dest="rIns", type=bool, help="Randomly select files to insert? (default = F)", default=False)
    parser.add_argument("-m", "--manuallyInsert", dest="mIns", type=str, help="Manually insert a file or set of files (Dec (1-180),Decl decimal(1-10), ra(1-360)) Ex: 179,1,1 or 179,1 or 179 are all valid inputs", default=None)
    parser.add_argument("-k", "--dropTables", dest="kill", type=bool, help="Drop Current tables and restart DB ingestion? (Default = False)", default=False)
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
    numFiles = args.fNum
    killConnections()
    createDatabase(args.dName)
    if(args.kill):
        for i in range(len(args.tNames)):
            print("Dropping Tables")
            dropTable(databaseName = args.dName, tableName = args.tNames[i])
            createTable(databaseName = args.dName, tableName = args.tNames[i])
    files = []
    if(args.mIns != None):
        print("Manual Insertion")
        text = args.mIns.split(",")
        try:
            lenDec = min(int(text[0]),180)
        except: 
            lenDec = 180
        try:
            lenDecDecimal = min(int(text[1]),10)
        except:
            lenDecDecimal = 10
        try:
            lenRA = min(int(text[2]),360)
        except:
            lenRA = 360
        print(lenDec, lenDecDecimal, lenRA)
        for decDeg in tqdm(range(0,lenDec)):
            for decDec in range(0,lenDecDecimal):
                for Ra in range(0,lenRA):
                    dec = "{:>03}".format(decDeg)
                    decdec = "{:>04}".format(decDec)
                    ra = "{:>03}".format(Ra)
                    insertTable(databaseName = args.dName, tableNames = args.tNames, path = args.fPath, dec1 = dec, dec2 = decdec, ra = ra)
                    files.append([dec,decdec,ra])
    elif(args.rIns):
        print("Random Insertion")
        for i in tqdm(range(args.fNum)):
            dec = int(random.uniform(0,179))
            decdec = int(random.uniform(0,9))
            ra = int(random.uniform(0,359))
            dec = "{:>03}".format(dec)
            decdec = "{:>04}".format(decdec)
            ra = "{:>03}".format(ra)
            insertTable(databaseName = args.dName, tableNames = args.tNames, path = args.fPath, dec1 = dec, dec2 = decdec, ra = ra)
            files.append([dec,decdec,ra])
        print(files)
    else:
        print("'Number of files' Insertion")
        for decDeg in tqdm(range(0,args.fNum)):
            for decDec in tqdm(range(10)):
                for Ra in range(360):#0-360
                    dec = "{:>03}".format(decDeg)
                    decdec = "{:>04}".format(decDec)
                    ra = "{:>03}".format(Ra)
                    insertTable(databaseName = args.dName, tableNames = args.tNames, path = args.fPath, dec1 = dec, dec2 = decdec, ra = ra)
                    files.append([dec,decdec,ra])
                # files.append([dec,decdec,ra])
    # print(f"Files Inserted into database: {files}")

    
    
if __name__ == "__main__":
    ingestDB()