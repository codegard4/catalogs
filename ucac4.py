import pymysql 
import argparse
import os
import sys
import math
import os.path
import numpy as np
import struct
import random
import configparser
from tqdm import tqdm

def connectionParameters():
    """
    Returns the host, port, user, and password of the MySQL database to connect to.
    Returns:
        Tuple: (str, int, str, str) - host, port, user, password
    """
    config = configparser.ConfigParser()
    config.read('catalogs.conf')
    db_host = config['UCAC4']['host']
    db_port = int(config['UCAC4']['port'])
    db_user = config['UCAC4']['user']
    db_password = config['UCAC4']['password']
    return db_host, db_port, db_user, db_password

def connectToDatabase(db_name = None):
    """
    Returns a connection to the database.
    Args:
        db_name (str): Name of the database.
    Returns:
        pymysql.connections.Connection: Database connection.
    """
    db_host,db_port,db_user,db_password = connectionParameters()
    if db_name == None:
        conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password)
    else:
        conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, database = db_name)
    return conn
        
def checkMag(mag):
     """
    Changes blank magnitude values to NULL.
    Args:
        mag (float): Magnitude value.
    Returns:
        float or None: Magnitude value or None.
    """
    if mag >= 20000:
        return None
    return mag / 1000
    
def createDatabase(databaseName = "UCAC4_dev"): 
    """
    Creates the specified database if it doesn't already exist.
    Args:
        databaseName (str): Name of the database.
    Returns:
        None
    """
    try:
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f'CREATE DATABASE {databaseName} ;')
        conn.commit()
        conn.close()
    except:
        print("DB already created")
    
def createTable(databaseName = "UCAC4_dev", tableName = "ucac4"): 
    """
    Creates the specified table.
    Args:
        databaseName (str): Name of the database.
        tableName (str): Name of the table.
    Returns:
        None
    """
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE {tableName} (UCAC_ID INT PRIMARY KEY);')
    if tableName == 'ucac4' or tableName == 'ucac4_not_visible':
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
    elif tableName == 'ucac4_errors_flags' or tableName == 'ucac4_errors_flags_not_visible':
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
    """
    Queries the database for the specified table.
    Args:
        databaseName (str): Name of the database.
        tableName (str): Name of the table.
    Returns:
        List: Result of the query.
    """
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
    """
    Inserts data from the z*filenum* file into the specified tables.
    Args:
        databaseName (str): Name of the database.
        fileNum (int): Number of the file to insert data from.
        tableNames (List): Names of the tables to insert data into.
        path (str): Path to the folder containing the files.
    Returns:
        None
    """
    try:
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        fileName = "{:>03}".format(fileNum)
        if fileNum < 100:
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
            ok = True
            incr = ""
            while ok:
                record = f.read(78)
                if not record:
                    break
                raw = struct.unpack("<iiHHBBB" + "bbBBBHH" + "hhbb" + "IHHHBBBBBBHHHHHbbbbbb" + "IbbIHI", record) #unpacks the binary record to the correct format
                tMASS_pts_key = raw[18]
                if tMASS_pts_key == 0:
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
                if APASS_B_err == 99:
                    APASS_B_err = None
                if APASS_V_err == 99:
                    APASS_V_err = None
                if APASS_g_err == 99:
                    APASS_g_err = None
                if APASS_r_err == 99:
                    APASS_r_err = None
                if APASS_i_err == 99:
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
    """
    Converts degrees to sexagesimal format (degs:mins:secs).
    Args:
        deg (float): Degree value.
    Returns:
        str: Sexagesimal representation of the degree.
    """
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
    """
    Converts degrees to sexagesimal format for RA (hrs:mins:secs).
    Args:
        deg (float): Degree value.
    Returns:
        str: Sexagesimal representation of the degree for RA.
    """
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
    """
    Converts radians to degrees.
    Args:
        radians (float): Radian value.
    Returns:
        float: Degree value.
    """
    return math.degrees(radians)
        

def dropTable(databaseName = "UCAC4", tableName = "ucac4"):
    """
    Deletes the specified table.
    Args:
        databaseName (str): Name of the database.
        tableName (str): Name of the table.
    Returns:
        None
    """
    try: 
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f"DROP TABLE {tableName};")
        conn.commit()
        conn.close()
    except Exception as e: 
        print(e)
        
def killConnections(databaseName = "UCAC4_dev"):
    """
    Closes open connections.
    Args:
        databaseName (str): Name of the database.
    Returns:
        None
    """
    try:
        _,_,user,_ = connectionParameters()
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f"SELECT CONCAT('KILL ', id, ';') FROM INFORMATION_SCHEMA.PROCESSLIST WHERE user = '{user}';")
        kills = cur.fetchall()
        for kill in kills:
            cur.execute(str(kill[0]))
        conn.commit()
        conn.close()
    except:
        pass

def parseArguments(in_args):
    """
    Parses command-line arguments.
    Args:
        in_args (List): List of command-line arguments.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    description = "Reads star files into mySQL DB"
    usage = "\n{} [-d databaseName] \n".format(in_args[0])
    epilog = ""
    parser = argparse.ArgumentParser(description=description, usage=usage, epilog=epilog)
    parser.add_argument("-d", "--databaseName", dest="dName", type=str, help="Name of the database to insert the tables into (default = 'UCAC4_dev')", default="UCAC4_dev")
    parser.add_argument("-n", "--NumFiles", dest="fNum", type=int, help="Number of files to insert into the database (default = 900)", default=900)
    parser.add_argument("-f", "--filePath", dest="fPath", type=str, help="location of the u4b folder (default = None)", default="")
    parser.add_argument("-r", "--randomInsertion", dest="rIns", type=bool, help="Randomly select files to insert? (default = False)", default=False)
    parser.add_argument("-m", "--manuallyInsert", dest="mIns", type=str, help="Manually insert zone files in a specified range (default = 0,0)", default=None)
    parser.add_argument("-k", "--dropTables", dest="kill", type=bool, help="Drop Current tables and restart DB ingestion? (default = False)", default=False)
    args = None
    try:
        args = parser.parse_args(in_args[1:])
    except Exception as e:
        print(e)
        parser.print_help()
        sys.exit(0) 
    return args 

def ingestDB():
    """
    Main function for ingesting data into the database based on command-line arguments.
    Returns:
        None
    """
    tNames = ['ucac4', 'ucac4_errors_flags', 'ucac4_not_visible', 'ucac4_errors_flags_not_visible']
    args = parseArguments(sys.argv) 
    numFiles = args.fNum
    killConnections(args.dName)
    createDatabase(args.dName)
    if args.kill: #Clear the tables and restart
        for i in range(len(tNames)):
            print("Dropping Tables")
            dropTable(databaseName = args.dName, tableName = tNames[i])
            createTable(databaseName = args.dName, tableName = tNames[i])
    if args.mIns != None: #manually insert files
        files = args.mIns.split(",")
        nums = np.arange(int(files[0]),int(files[1])+1,1)
        numFiles = len(nums)
        print(f"Manually Inserting files {files[0]} through {files[1]}")
    elif(args.rIns): #randomly insert files (for database testing on dev)
        nums = random.sample(range(1, 901), args.fNum)
    else: #insert a specified number of files
        nums = np.arange(1,901,int(900/args.fNum))    
    for i in tqdm(range(1,numFiles+1)):
        insertTable(databaseName = args.dName, fileNum = nums[i-1], tableNames = tNames, path = args.fPath)
    print(f"Zone Files Inserted: {nums}")

if __name__ == "__main__":
    ingestDB()