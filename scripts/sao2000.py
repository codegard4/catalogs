import pymysql 
import math
import argparse
import os
import sys
import configparser
from tqdm import tqdm
  
def connectionParameters():
    """
    Retrieves MySQL connection parameters from the config file.
    Returns:
        Tuple: (host, port, user, password)
    """
    config = configparser.ConfigParser()
    config.read('catalogs.conf')
    db_host = config['SAO2000']['host']
    db_port = int(config['SAO2000']['port'])
    db_user = config['SAO2000']['user']
    db_password = config['SAO2000']['password']
    return db_host, db_port, db_user, db_password

def connectToDatabase(db_name = None):
    """
    Connects to the MySQL database on the specified server.
    Args:
        db_name (str): Name of the database.
    Returns:
        pymysql.connections.Connection: MySQL database connection.
    """
    db_host,db_port,db_user,db_password = connectionParameters()
    if db_name == None:
        conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password)
    else:
        conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, database = db_name)
    return conn   
    
def createDatabase(databaseName = "SAO2000_dev"): 
    """
    Creates the SAO2000 database if it doesn't already exist.
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
    
def createTable1950(databaseName = "SAO2000_dev"):
    """
    Creates the sao1950 table.
    Args:
        databaseName (str): Name of the database.
    Returns:
        None
    """
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    cur.execute('CREATE TABLE sao1950 (SaoNumber INT PRIMARY KEY);')
    query = """ALTER TABLE sao1950 ADD Dup VARCHAR(1), \
                ADD RA1950 VARCHAR(14), ADD PMRA_1950 FLOAT, \
                ADD PMRA_1950mu FLOAT, ADD RA2m_Flag VARCHAR(1), \
                ADD RA1950_precessed FLOAT, ADD RA1950_precessed_sd FLOAT, \
                ADD Original_Epoch FLOAT, ADD Dec1950 VARCHAR(14), \
                ADD PMDec_1950 FLOAT, ADD PMDec_1950mu FLOAT, \
                ADD D2m_Flag VARCHAR(1), ADD DE2s FLOAT, \
                ADD e_DE2 FLOAT, ADD Dec_orig_epoch FLOAT, \
                ADD e_Pos FLOAT, ADD VMag_src INT, \
                ADD StarNum_src INT, \
                ADD PhotMag_src INT, \
                ADD PM_src INT, \
                ADD SpecType_src INT, \
                ADD Rem INT, \
                ADD SrcCatCode INT, \
                ADD SrcCatNum INT, \
                ADD DurchmusterungID VARCHAR(14), \
                ADD HenryDraperCatNum VARCHAR(6), \
                ADD HDDuplicateID VARCHAR(1), \
                ADD GeneralCatalogNumber1950 VARCHAR(5), \
                ADD RA1950_rad FLOAT, \
                ADD Dec1950_rad FLOAT; \
            """
    cur.execute(query)
    conn.commit()
    conn.close()

def viewTable(databaseName = "SAO2000_dev", name = "sao2000"):
    """
    Returns in Python the view from selecting a certain table. Function unused in database setup.
    Args:
        databaseName (str): Name of the database.
        name (str): Name of the table.
    Returns:
        List: Rows of the selected table.
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

def insertIntoTable1950(databaseName = "SAO2000_dev", numRows = 5, fileName = "sao.dat"):  
    """
    Inserts the specified number of rows into the sao1950 table.
    Args:
        databaseName (str): Name of the database.
        numRows (int): Number of rows to insert.
        fileName (str): Name of the file containing data.
    Returns:
        None
    """
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    sql = """INSERT INTO sao1950 (SaoNumber, Dup, RA1950, \
                PMRA_1950,PMRA_1950mu,RA2m_Flag, \
                RA1950_precessed,RA1950_precessed_sd, \
                Original_Epoch, Dec1950, PMDec_1950, \
                PMDec_1950mu, D2m_Flag, DE2s, e_DE2, \
                Dec_orig_epoch, e_Pos, VMag_src, StarNum_src, \
                PhotMag_src, PM_src, SpecType_src, Rem, \
                SrcCatCode, SrcCatNum, \
                DurchmusterungID, HenryDraperCatNum, HDDuplicateID, \
                GeneralCatalogNumber1950, RA1950_rad, Dec1950_rad) \
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); 
        """
    with open(f'{fileName}', 'r') as f:
        for line in tqdm(f):
            line = str.encode(line)
            SaoNumber = int(line[0:6].decode()) 
            if SaoNumber > numRows:
                break
            Dup = str(line[6:7].decode())
            if Dup == ' ':
                Dup = None
            rah = str("{:02d}".format(int(line[7:9].decode())))
            ram = str("{:02d}".format(int(line[9:11].decode())))
            ras = str("{:02d}".format(int(line[11:13].decode())))
            rass = str(line[13:17].decode())
            RA1950 =  rah + ":" + ram + ":" + ras + rass
            PMRA_1950 = line[17:24].decode()
            PMRA_1950mu = int(line[24:26].decode())
            RA2m_Flag = str(line[26:27].decode())
            if RA2m_Flag == ' ':
                RA2m_Flag = None
            RA1950_precessed = float(line[27:33].decode())
            RA1950_precessed_sd = int(line[33:35].decode())
            Original_Epoch = float(line[35:41].decode())
            decsign = str(line[41:42].decode())
            decd = str("{:02d}".format(int(line[42:44].decode())))
            decm = str("{:02d}".format(int(line[44:46].decode())))
            decs = str("{:02d}".format(int(line[46:48].decode())))
            decss = str(line[48:51].decode())
            if decsign == '+':
                decsign = ''
            Dec1950 = decsign + decd + ":" + decm + ":" + decs + decss
            PMDec_1950 = line[51:57].decode()
            PMDec_1950mu = int(line[57:59].decode())
            D2m_Flag = str(line[59:60].decode())
            if D2m_Flag == ' ':
                D2m_Flag = None
            DE2s = float(line[60:65].decode())
            e_DE2 = int(line[65:67].decode())
            Dec_orig_epoch = float(line[67:73].decode())
            e_Pos = int(line[73:76].decode())
            VMag_src = int(line[87:89].decode())
            StarNum_src = int(line[89:91].decode())
            PhotMag_src = int(line[91:92].decode())
            PM_src = int(line[92:93].decode())
            SpecType_src = int(line[93:94].decode())
            Rem = int(line[94:95].decode())
            SrcCatCode = int(line[97:99].decode())
            SrcCatNum = int(line[99:104].decode())
            DurchmusterungID = str(line[104:117].decode())
            HenryDraperCatNum = str(line[117:123].decode())
            HDDuplicateID =str(line[123:124].decode())
            if HDDuplicateID == ' ':
                HDDuplicateID = None
            GeneralCatalogNumber1950 =str(line[124:129].decode())
            RA1950_rad = float(line[129:139].decode())
            Dec1950_rad = float(line[139:150].decode())  
            if PMRA_1950 == '      ':
                PMRA_1950 = 0
            PMRA_1950 = float(PMRA_1950)
            if PMDec_1950 == '      ':
                PMDec_1950 = 0
            PMDec_1950 = str(PMDec_1950)
            cur.execute(sql,(SaoNumber, Dup, 
                RA1950, PMRA_1950, PMRA_1950mu,
                RA2m_Flag, RA1950_precessed,
                RA1950_precessed_sd, Original_Epoch,
                Dec1950, PMDec_1950, PMDec_1950mu,
                D2m_Flag, DE2s, e_DE2, Dec_orig_epoch,
                e_Pos, VMag_src, StarNum_src,
                PhotMag_src, PM_src, SpecType_src,
                Rem, SrcCatCode, SrcCatNum, DurchmusterungID,
                HenryDraperCatNum, HDDuplicateID,
                GeneralCatalogNumber1950,
                RA1950_rad, Dec1950_rad))
    conn.commit()
    conn.close()
                    
def createTable2000(databaseName = "SAO2000_dev"): 
    """
    Creates the sao2000 table.
    Args:
        databaseName (str): Name of the database.
    Returns:
        None
    """
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    cur.execute('CREATE TABLE sao2000 (SaoNumber INT PRIMARY KEY);')
    query = """ALTER TABLE sao2000 ADD RA VARCHAR(13), \
            ADD PMRA FLOAT, ADD Decl VARCHAR(13), \
            ADD PMDec FLOAT, \
            ADD RA_rad FLOAT, \
            ADD Dec_rad FLOAT, \
            ADD RA_deg FLOAT, \
            ADD Dec_deg FLOAT, \
            ADD PhotMag FLOAT, \
            ADD VMag FLOAT, \
            ADD SpectralType VARCHAR(3), \
            ADD VMag_delta FLOAT, \
            ADD PhotMag_delta FLOAT; \
            """
    cur.execute(query)
    conn.commit()
    conn.close()
    
def radToDeg(radians):
    """
    Converts radians to degrees.
    Args:
        radians (float): Angle in radians.
    Returns:
        float: Angle in degrees.
    """
    return math.degrees(radians)
        
def insertIntoTable2000(databaseName = "SAO2000_dev", numRows = 5, fileName = "sao.dat"): 
    """
    Inserts the specified number of rows into the sao2000 table.
    Args:
        databaseName (str): Name of the database.
        numRows (int): Number of rows to insert.
        fileName (str): Name of the file containing data.
    Returns:
        None
    """
    countra, countdec = 0,0
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    sql = """INSERT INTO sao2000 (SaoNumber, RA, PMRA, Decl, PMDec, \
                                    RA_rad, Dec_rad, RA_deg, Dec_deg, \
                                    PhotMag, VMag, SpectralType, \
                                    VMag_delta, PhotMag_delta) \
             VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s); 
        """
    with open(f'{fileName}', 'r') as f:
        for line in tqdm(f):
            line = str.encode(line)
            SaoNumber = int(line[0:6].decode())
            if SaoNumber > numRows:
                break
            rah = str("{:02d}".format(int(line[150:152].decode())))
            ram = str("{:02d}".format(int(line[152:154].decode())))
            ras = str("{:02d}".format(int(line[154:156].decode())))
            rass = str(line[156:160].decode())
            RA =  rah + ":" + ram + ":" + ras + rass
            PMRA = line[160:167].decode()
            decsign = str(line[167:168].decode())
            if decsign == '+':
                decsign = ''
            decd = str("{:02d}".format(int(line[168:170].decode())))
            decm = str("{:02d}".format(int(line[170:172].decode())))
            decs = str("{:02d}".format(int(line[172:174].decode())))
            decss = str(line[174:177].decode())
            Decl = decsign + decd + ":" + decm + ":" + decs + decss
            PMDec = line[177:183].decode() 
            RA_rad = float(line[183:193].decode())
            Dec_rad = float(line[193:204].decode())
            Dec_deg = radToDeg(float(line[193:204].decode()))
            RA_deg = radToDeg(float(line[183:193].decode()))
            PhotMag = float(line[76:80].decode())
            VMag = float(line[80:84].decode())
            SpectralType = str(line[84:87].decode())
            VMag_delta = int(line[95:96].decode())
            PhotMag_delta = int(line[96:97].decode())
            if PMRA == '      ':
                countra +=1
                PMRA = 0
            PMRA = float(PMRA)
            if PMDec == '      ':
                countdec+=1
                PMDec = 0
            PMDec = float(PMDec)
            if VMag == 99.9:
                VMag = None
            if PhotMag == 99.9:
                PhotMag = None
            cur.execute(sql,(SaoNumber,RA,PMRA,
                    Decl,PMDec,RA_rad,Dec_rad,
                    RA_deg,Dec_deg,PhotMag,
                    VMag,SpectralType,
                    VMag_delta,PhotMag_delta))
    conn.commit()
    conn.close() 
    
def dropTable(databaseName = "SAO2000_dev", tableName = "sao2000"):
    """
    Drops the specified table if it already exists.
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
        
def killConnections():
    """
    Kills any open connections to the database from the user.
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
    Parses command-line arguments when the Python script is called.
    Args:
        in_args (List): List of command-line arguments.
    Returns:
        Namespace: Parsed arguments.
    """
    description = "Reads star files from sao2000 catalog into mySQL DB"
    usage = "\n{} [-d databaseName] \n".format(in_args[0])
    epilog = ""
    parser = argparse.ArgumentParser(description = description, usage = usage, epilog = epilog)
    parser.add_argument("-d", "--databaseName", dest = "dName", type = str, help = "Name of the database to insert the tables into (default = SAO2000_dev", default = "SAO2000_dev")
    parser.add_argument("-f", "--fileName", dest = "fName", type = str, help = "Path to the star catalog file sao.dat (default = None)", default = "")
    parser.add_argument("-r", "--rows", dest = "rows", type = int, help = "Number of rows to insert into the database (default = All rows)", default = 99999999)
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
    Creates the full SAO2000 Database.
    Returns:
        None
    """
    args = parseArguments(sys.argv)
    killConnections()
    createDatabase(databaseName = args.dName)
    dropTable(databaseName = args.dName, tableName = "sao1950")
    dropTable(databaseName = args.dName, tableName = "sao2000")
    createTable1950(databaseName = args.dName)
    createTable2000(databaseName = args.dName)
    insertIntoTable1950(databaseName = args.dName, numRows = args.rows, fileName = args.fName)
    insertIntoTable2000(databaseName = args.dName, numRows = args.rows, fileName = args.fName)
    
if __name__ == "__main__":
    ingestDB()
    
