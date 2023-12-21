import pymysql 
from tqdm import tqdm
import argparse
import os
import sys
import math
import os.path
import random
import configparser
import csv

def connectionParameters():
    """
    Returns the host, port, user, and password of the MySQL database to connect to.
    Returns:
        Tuple: (str, int, str, str) - host, port, user, password
    """
    config = configparser.ConfigParser()
    config.read('catalogs.conf')
    db_host = config['2MASS']['host']
    db_port = int(config['2MASS']['port'])
    db_user = config['2MASS']['user']
    db_password = config['2MASS']['password']
    return db_host, db_port, db_user, db_password

def connectToDatabase(db_name = None):
    """
    Returns a connection to the MySQL database.
    Args:
        db_name (str): Name of the database.
    Returns:
        pymysql.Connection: MySQL database connection.
    """
    db_host, db_port, db_user, db_password = connectionParameters()
    if db_name == None:
        conn = pymysql.connect(host = db_host, port = db_port, user = db_user, password = db_password)
    else:
        conn = pymysql.connect(host = db_host, port = db_port, user = db_user, password = db_password, database = db_name)
    return conn
    
    
def createDatabase(databaseName = "2MASS_dev"): 
    """
    Creates the specified database if it doesn't already exist.
    Args:
        databaseName (str): Name of the database.
    """
    try:
        conn = connectToDatabase()
        cur = conn.cursor()
        cur.execute(f'CREATE DATABASE {databaseName};')
        conn.commit()
        conn.close()
        print(f"DB {databaseName} created")
    except:
        pass
        
    
def createTable(databaseName = "2MASS_dev", tableName = "2mass"): 
    """
    Creates the specified table.
    Args:
        databaseName (str): Name of the database.
        tableName (str): Name of the table.
    """
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE {tableName} (2mass_ID VARCHAR(20) PRIMARY KEY);')
    if tableName == '2mass' or tableName == '2mass_not_visible':
        query = f"""ALTER TABLE {tableName} \
            ADD RA VARCHAR(13), \
            ADD Decl VARCHAR(13), \
            ADD RA_rad DOUBLE(5,7), \
            ADD Decl_rad DOUBLE(5,7), \
            ADD RA_deg DOUBLE(5,7), \
            ADD Decl_deg DOUBLE(5,7), \
            ADD JMag REAL, \
            ADD HMag REAL, \
            ADD KMag REAL, \
            ADD ph_qual VARCHAR(3), \
            ADD rd_flg INT; \
            """
        cur.execute(query)
    conn.commit()
    conn.close()

def viewTable(databaseName = "2MASS_dev", tableName = "2mass"):
    """
    Queries the database for the specified table.
    Args:
        databaseName (str): Name of the database.
        tableName (str): Name of the table.
    Returns:
        List: List of rows from the table.
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

def cnm(value):
    """
    Check Null Magnitude: Checks for blank magnitude inputs to convert to null
    Args:
        value (str): The input value
    Returns:
        Float or None: The float value or None if the input is an empty string.
    """
    if value == "":
        return None
    return float(value)
        
def insertTable(databaseName = "2MASS_dev", tableNames = ['2mass', '2mass_not_visible'], path = "", dec1="000", dec2="0000", ra="000", verbose = False):  
    """
    Inserts data from the dec1 dec2 ra file.
    Args:
        databaseName (str): Name of the database.
        tableNames (List): List of table names.
        path (str): Path to the CSV files.
        dec1 (str): Declination degree.
        dec2 (str): Declination decimal.
        ra (str): Right ascension.
        verbose (bool): Whether to print flags
    Returns:
        None
    """
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor() 
    try:
        sql = f"""INSERT INTO 2mass ( \
        2mass_ID, RA, Decl, RA_rad, Decl_rad, RA_deg, Decl_deg, JMag, HMag, KMag, ph_qual, rd_flg)\
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); \
            """
        sql_nv= f"""INSERT INTO 2mass_not_visible ( \
                2mass_ID, RA, Decl, RA_rad, Decl_rad, RA_deg, Decl_deg, JMag, HMag, KMag, ph_qual, rd_flg)\
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); \
            """
        file = f"{dec1}/{dec2}/{ra}.dat"
        count = 0
        countdup = 0
        with open(f'{path}/{file}', 'r') as f:
            csvFile = csv.reader(f)
            for line in csvFile:
                try:
                    ra_deg = float(line[0])
                    dec_deg = float(line[1])
                    twomass_id = line[2]
                    ra_rad = degToRad(ra_deg)
                    dec_rad = degToRad(dec_deg)
                    RA = deg2SexagHrs(ra_deg)
                    Decl = deg2Sexag(dec_deg)
                    JMag = cnm(line[3])
                    HMag = cnm(line[4])
                    KMag = cnm(line[5])
                    ph_qual = line[6]
                    rd_flg = float(line[7])
                    if dec_deg < -70.:
                        cur.execute(sql_nv,(
                            twomass_id, RA, Decl, ra_deg, dec_deg, ra_rad, dec_rad, JMag, HMag, KMag, ph_qual, rd_flg))
                    else:
                        cur.execute(sql,(
                            twomass_id, RA, Decl, ra_deg, dec_deg, ra_rad, dec_rad, JMag, HMag, KMag, ph_qual, rd_flg))
                    count+=1
                except Exception as e:
                    #This exception will print all error messages that are not a duplicate primary key
                    #--------------------------#
                    if int(e.args[0]) != 1062:
                        print(e)
                        print(line)
                    # elif verbose:
                    #     if int(e.args[0]) == 1062:
                    #         print(e)
                    #-------------------------#
                    
                    countdup+=1
    except Exception as e:
        #this exception catches files that do not exist
        if(verbose):
            print(e)
        pass
    conn.ping()
    conn.commit()
    conn.close()
    if(verbose):
        #print(f"{count} stars inserted | {countdup} duplicates")
        return count, countdup
                    
def deg2Sexag(deg):
    """
    Converts degrees to sexagesimal format (degs:mins:secs).
    Args:
        deg (float): Degree value.
    Returns:
        str: Sexagesimal formatted string.
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
        str: Sexagesimal formatted string.
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
    
def degToRad(degrees):
    """
    Converts degrees to radians.
    Args:
        degrees (float): Degree value.
    Returns:
        float: Radian value.
    """
    return math.radians(degrees)
        

def dropTable(databaseName = "2MASS_dev", tableName = "2mass"):
    """
    Deletes the specified table.
    Args:
        databaseName (str): Name of the database.
        tableName (str): Name of the table.
    """
    try: 
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f"DROP TABLE {tableName};")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        
def killConnections(databaseName = "2MASS_dev"):
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
    parser = argparse.ArgumentParser(description = description, usage = usage, epilog = epilog)
    parser.add_argument("-d", "--databaseName", dest = "dName", type = str, help = "Name of the database to insert the tables into (default = '2MASS_dev')", default = "2MASS_dev")
    parser.add_argument("-n", "--NumDec", dest = "fNum", type = int, help = "Number of Dec files to insert into the database (default = 180)", default = 180)
    parser.add_argument("-f", "--filePath", dest = "fPath", type = str, help = "location of the 2mass data folder (default = None)", default = "")
    parser.add_argument("-r", "--randomInsertion", dest ="rIns", type = bool, help = "Randomly select files to insert? (default = F)", default = False)
    parser.add_argument("-m", "--manuallyInsert", dest = "mIns", type = str, help = "Manually insert a file or set of files (Dec (1-180),Decl decimal(1-10), ra(1-360)) Ex: 179,1,1 or 179,1 or 179 are all valid inputs (default = None)", default = None)
    parser.add_argument("-k", "--dropTables", dest = "kill", type = bool, help = "Drop Current tables and restart DB ingestion? (default = False)", default = False)
    parser.add_argument("-mr", "--manualRange", dest = "mr", type = str, help = "Manually insert a set of files (1,180--insert dec files 0-179) (default = None)", default = "")
    parser.add_argument("-v", "--verbose", dest = "verbose", type = bool, help = "Print number of duplicate/new stars to command line (default = False)", default = False)
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
    args = parseArguments(sys.argv) 
    numFiles = args.fNum
    killConnections()
    createDatabase(args.dName)
    tNames = ['2mass', '2mass_not_visible']
    if args.kill:
        for i in range(len(args.tNames)):
            print("Dropping Tables")
            dropTable(databaseName = args.dName, tableName = tNames[i])
            createTable(databaseName = args.dName, tableName = tNames[i])
    files = []
    if len(args.mr) > 0:
        print("Manual Range Insertion")
        text = args.mr.split(",")
        for decDeg in tqdm(range(int(text[0]),int(text[1]))):
            for decDec in tqdm(range(10)):
                count,countdups = 0,0
                for Ra in range(360):
                    dec = "{:>03}".format(decDeg)
                    decdec = "{:>04}".format(decDec)
                    ra = "{:>03}".format(Ra)
                    c,cd = insertTable(databaseName = args.dName, tableNames = tNames, path = args.fPath, dec1 = dec, dec2 = decdec, ra = ra, verbose = args.verbose)
                    count+=c
                    countdups+=cd
                files.append([dec,decdec])   
                print(f"{count} new stars | {countdups} duplicates")
    elif args.mIns != None:
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
        for decDeg in range(lenDec,lenDec+1):
            for decDec in range(lenDecDecimal,lenDecDecimal+1):
                count,countdups = 0,0
                for Ra in tqdm(range(0,lenRA)):
                    dec = "{:>03}".format(decDeg)
                    decdec = "{:>04}".format(decDec)
                    ra = "{:>03}".format(Ra)
                    c,cd = insertTable(databaseName = args.dName, tableNames = tNames, path = args.fPath, dec1 = dec, dec2 = decdec, ra = ra, verbose = args.verbose)
                    count+=c
                    countdups+=cd
                    files.append([dec,decdec,ra])
                print(f"{count} stars inserted | {countdups} duplicate stars")
    elif(args.rIns):
        print("Random Insertion")
        for i in tqdm(range(args.fNum)):
            dec = int(random.uniform(0,179))
            decdec = int(random.uniform(0,9))
            ra = int(random.uniform(0,359))
            dec = "{:>03}".format(dec)
            decdec = "{:>04}".format(decdec)
            ra = "{:>03}".format(ra)
            insertTable(databaseName = args.dName, tableNames = tNames, path = args.fPath, dec1 = dec, dec2 = decdec, ra = ra, verbose = args.verbose)
            files.append([dec,decdec,ra])
        print(files)
    else:
        print("'Number of files' Insertion")
        for decDeg in tqdm(range(0,args.fNum)):
            for decDec in tqdm(range(10)):
                count,countdups = 0,0
                for Ra in range(360):
                    dec = "{:>03}".format(decDeg)
                    decdec = "{:>04}".format(decDec)
                    ra = "{:>03}".format(Ra)
                    c,cd = insertTable(databaseName = args.dName, tableNames = tNames, path = args.fPath, dec1 = dec, dec2 = decdec, ra = ra, verbose = args.verbose)
                    count+=c
                    countdups+=cd
                files.append([dec,decdec])
                print(f"{decDeg}: {count} stars inserted | {countdups} duplicate stars")
    if(args.verbose):
        for file in files:
            print(file)
    
if __name__ == "__main__":
    ingestDB()