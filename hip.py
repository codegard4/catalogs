import pymysql 
from tqdm import tqdm
import argparse
import os
import sys
import math
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
    db_host = config['HIP']['host']
    db_port = int(config['HIP']['port'])
    db_user = config['HIP']['user']
    db_password = config['HIP']['password']
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
    
    
def createDatabase(databaseName = "HIP_dev"): 
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
        
def cbf(value):
    """
    Check Blank Float: Checks for blank float inputs.
    Args:
        value (str): The input value to be converted to float.
    Returns:
        float or None: The converted float value or None if the input is an empty string.
    """
    if value == '' or value == ' ':
        return None
    return float(value)


def cbi(value):
    """
    Check Blank Integer: Checks for blank integer inputs.
    Args:
        value (str): The input value to be converted to integer.
    Returns:
        int or None: The converted integer value or None if the input is an empty string.
    """
    if value == '' or value == ' ':
        return None
    return int(float(value))


def cbs(value):
    """
    Check Blank String: Checks for blank string inputs.
    Args:
        value (str): The input value to be converted to boolean.
    Returns:
        str or None: The converted string value or None if the input is an empty string.
    """
    if value == '' or value == ' ':
        return None
    return str(value)

def createTable(databaseName = "HIP_dev", tableName = "hip"): 
    """
    Creates the specified table.
    Args:
        databaseName (str): Name of the database.
        tableName (str): Name of the table.
    """
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    sql = f"""CREATE TABLE hip (\
        HIP_ID INT PRIMARY KEY,\
        RA VARCHAR(13),\
        Decl VARCHAR(13),\
        RA_Deg REAL,\
        Decl_Deg REAL,\
        RA_Rad REAL,\
        Decl_Rad REAL,\
        Vmag REAL,\
        Parallax REAL,\
        pm_RA REAL,\
        pm_Dec REAL,\
        BT_Mag REAL,\
        VT_Mag REAL,\
        Hip_Mag REAL,\
        BV_Color REAL,\
        VI_Color REAL\
    );\
    """
    sql_ef = f"""CREATE TABLE hip_errors_flags (\
        HIP_ID INT PRIMARY KEY,\
        Prox_10asec VARCHAR(10),\
        Var_Flag VARCHAR(10),\
        Vmag_Source VARCHAR(10),\
        Astrom_Ref_Dbl VARCHAR(10),\
        RA_Error REAL,\
        Dec_Error REAL,\
        Parallax_Error REAL,\
        pm_RA_Error REAL,\
        pm_Dec_Error REAL,\
        Crl_Dec_RA REAL,\
        Crl_Plx_RA REAL,\
        Crl_Plx_Dec REAL,\
        Crl_pmRA_RA REAL,\
        Crl_pmRA_Dec REAL,\
        Crl_pmRA_Plx REAL,\
        Crl_pmDec_RA REAL,\
        Crl_pmDec_Dec REAL,\
        Crl_pmDec_Plx REAL,\
        Crl_pmDec_pmRA REAL,\
        Reject_Percent REAL,\
        Quality_Fit REAL,\
        BT_Mag_Error REAL,\
        VT_Mag_Error REAL,\
        BT_Mag_Ref_Dbl VARCHAR(10),\
        BV_Color_Error REAL,\
        BV_Mag_Source VARCHAR(10),\
        VI_Color_Error REAL,\
        VI_Color_Source VARCHAR(10),\
        Mag_Ref_Dbl VARCHAR(10),\
        Hip_Mag_Error REAL,\
        Scat_Hip_Mag REAL,\
        N_Obs_Hip_Mag INT,\
        Hip_Mag_Ref_Dbl VARCHAR(10),\
        Hip_Mag_Max REAL,\
        Hip_Mag_Min REAL,\
        Var_Period VARCHAR(10),\
        Hip_Var_Type VARCHAR(10),\
        Var_Data_Annex VARCHAR(10),\
        Var_Curv_Annex VARCHAR(10),\
        CCDM_Id VARCHAR(10),\
        CCDM_History VARCHAR(10),\
        CCDM_N_Entries VARCHAR(10),\
        CCDM_N_Comp INT,\
        Dbl_Mult_Annex VARCHAR(10),\
        Astrom_Mult_Source VARCHAR(10),\
        Dbl_Soln_Qual VARCHAR(10),\
        Dbl_Ref_ID VARCHAR(10),\
        Dbl_Theta VARCHAR(10),\
        Dbl_Rho VARCHAR(10),\
        Rho_Error VARCHAR(10),\
        Diff_Hip_Mag VARCHAR(10),\
        dHip_Mag_Error VARCHAR(10),\
        Survey_Star VARCHAR(1),\
        ID_Chart VARCHAR(10),\
        Notes VARCHAR(10),\
        HD_Id INT,\
        BD_Id VARCHAR(20),\
        CoD_Id VARCHAR(10),\
        CPD_Id VARCHAR(10),\
        VI_Color_Reduct REAL,\
        Spect_Type VARCHAR(20),\
        Spect_Type_Source VARCHAR(10));\
    """
    if tableName == 'hip':
        cur.execute(sql)
    elif tableName == 'hip_errors_flags':
        cur.execute(sql_ef)
    conn.commit()
    conn.close()

def viewTable(databaseName = "HIP_dev", tableName = "hip"):
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

def sexag2Deg(sexag):
    """
    Converts sexagesimal format (degs:mins:secs) to degrees.
    Args:
        sexag (str): Sexagesimal formatted string.
    Returns:
        float: Degree value.
    """
    parts = sexag.split(' ')
    sign = 1
    if parts[0][0] == '-':
        sign = -1
        parts[0] = parts[0][1:]
    deg = float(parts[0])
    deg += float(parts[1]) / 60
    deg += float(parts[2]) / 3600
    return deg * sign

def sexag2DegHrs(sexag):
    """
    Converts sexagesimal format for RA (hrs:mins:secs) to degrees.
    Args:
        sexag (str): Sexagesimal formatted string.
    Returns:
        float: Degree value.
    """
    parts = sexag.split(' ')
    hrs = float(parts[0])
    hrs += float(parts[1]) / 60
    hrs += float(parts[2]) / 3600
    return (hrs / 24) * 360
    
def insertTable(databaseName = "HIP_dev", path = "", verbose = False):  
    """
    Inserts data from the dec1 dec2 ra file.
    Args:
        databaseName (str): Name of the database.
        path (str): Path to the CSV files.
        verbose (bool): Whether to print flags
    Returns:
        None
    """
    
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor() 

    sql = f"""INSERT INTO hip (\
    HIP_ID, RA, Decl, RA_deg, Decl_deg, RA_rad, Decl_rad, Vmag, Parallax, pm_RA, pm_Dec, BT_Mag, VT_Mag, Hip_Mag, BV_Color, VI_Color) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); \
    """
    sql_errors_flags = f"""INSERT INTO hip_errors_flags (\
    HIP_ID, Prox_10asec, Var_Flag, Vmag_Source, Astrom_Ref_Dbl, RA_Error, Dec_Error, Parallax_Error, pm_RA_Error, pm_Dec_Error, \
    Crl_Dec_RA, Crl_Plx_RA, Crl_Plx_Dec, Crl_pmRA_RA, Crl_pmRA_Dec, Crl_pmRA_Plx, Crl_pmDec_RA, Crl_pmDec_Dec, Crl_pmDec_Plx, \
    Crl_pmDec_pmRA, Reject_Percent, Quality_Fit, BT_Mag_Error, VT_Mag_Error, BT_Mag_Ref_Dbl, BV_Color_Error, BV_Mag_Source, \
    VI_Color_Error, VI_Color_Source, Mag_Ref_Dbl, Hip_Mag_Error, Scat_Hip_Mag, N_Obs_Hip_Mag, Hip_Mag_Ref_Dbl, Hip_Mag_Max, \
    Hip_Mag_Min, Var_Period, Hip_Var_Type, Var_Data_Annex, Var_Curv_Annex, CCDM_Id, CCDM_History, CCDM_N_Entries, CCDM_N_Comp, \
    Dbl_Mult_Annex, Astrom_Mult_Source, Dbl_Soln_Qual, Dbl_Ref_ID, Dbl_Theta, Dbl_Rho, Rho_Error, Diff_Hip_Mag, dHip_Mag_Error, \
    Survey_Star, ID_Chart, Notes, HD_Id, BD_Id, CoD_Id, CPD_Id, VI_Color_Reduct, Spect_Type, Spect_Type_Source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  \
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  \
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \
    ); \
    """
    filename = "hip_main.csv"
    with open(path+filename, 'r') as f:
        count, countdup = 0,0
        r = csv.reader(f)
        for line in tqdm(r):
            try: #will correctly fail if there is a duplicate star
                HIP_ID = int(line[1])
                Prox_10asec = cbs(line[2])
                RA = line[3]
                Dec = line[4]
                Vmag = cbf(line[5])
                Var_Flag = cbs(line[6])
                Vmag_Source = cbs(line[7])
                RA_Deg = cbf(line[8])
                Decl_Deg = cbf(line[9])
                if RA_Deg == None or Decl_Deg == None:
                    RA_Deg = sexag2DegHrs(RA)
                    Decl_Deg = sexag2Deg(Dec)
                RA = deg2SexagHrs(RA_Deg)
                Decl = deg2Sexag(Decl_Deg)
                RA_Rad = degToRad(RA_Deg)
                Decl_Rad = degToRad(Decl_Deg)
                Astrom_Ref_Dbl = cbs(line[10])
                Parallax = cbf(line[11])
                pm_RA = cbf(line[12])
                pm_Dec = cbf(line[13])
                RA_Error = cbf(line[14])
                Dec_Error = cbf(line[15])
                Parallax_Error = cbf(line[16])
                pm_RA_Error = cbf(line[17])
                pm_Dec_Error = cbf(line[18])
                Crl_Dec_RA = cbf(line[19])
                Crl_Plx_RA = cbf(line[20])
                Crl_Plx_Dec = cbf(line[21])
                Crl_pmRA_RA = cbf(line[22])
                Crl_pmRA_Dec = cbf(line[23])
                Crl_pmRA_Plx = cbf(line[24])
                Crl_pmDec_RA = cbf(line[25])
                Crl_pmDec_Dec = cbf(line[26])
                Crl_pmDec_Plx = cbf(line[27])
                Crl_pmDec_pmRA = cbf(line[28])
                Reject_Percent = cbf(line[29])
                Quality_Fit = cbf(line[30])
                # not_displayed = line[31]
                BT_Mag = cbf(line[32])
                BT_Mag_Error = cbf(line[33])
                VT_Mag = cbf(line[34])
                VT_Mag_Error = cbf(line[35])
                BT_Mag_Ref_Dbl = cbs(line[36])
                BV_Color = cbf(line[37])
                BV_Color_Error = cbf(line[38])
                BV_Mag_Source = cbs(line[39])
                VI_Color = cbf(line[40])
                VI_Color_Error = cbf(line[41])
                VI_Color_Source = cbs(line[42])
                Mag_Ref_Dbl = cbs(line[43])
                Hip_Mag = cbf(line[44])
                Hip_Mag_Error = cbf(line[45])
                Scat_Hip_Mag = cbf(line[46])
                N_Obs_Hip_Mag = cbi(line[47])
                Hip_Mag_Ref_Dbl = cbs(line[48])
                Hip_Mag_Max = cbf(line[49])
                Hip_Mag_Min = cbf(line[50])
                Var_Period = cbs(line[51])
                Hip_Var_Type = cbs(line[52])
                Var_Data_Annex = cbs(line[53])
                Var_Curv_Annex = cbs(line[54])
                CCDM_Id = cbs(line[55])
                CCDM_History = cbs(line[56])
                CCDM_N_Entries = cbs(line[57])
                CCDM_N_Comp = cbi(line[58])
                Dbl_Mult_Annex = cbs(line[59])
                Astrom_Mult_Source = cbs(line[60])
                Dbl_Soln_Qual = cbs(line[61])
                Dbl_Ref_ID = cbs(line[62])
                Dbl_Theta = cbs(line[63])
                Dbl_Rho = cbs(line[64])
                Rho_Error = cbs(line[65])
                Diff_Hip_Mag = cbs(line[66])
                dHip_Mag_Error = cbs(line[67])
                Survey_Star = cbs(line[68])
                ID_Chart = cbs(line[69])
                Notes = cbs(line[70])
                HD_Id = cbi(line[71])
                BD_Id = cbs(line[72])
                CoD_Id = cbs(line[73])
                CPD_Id = cbs(line[74])
                VI_Color_Reduct = cbs(line[75])
                Spect_Type = cbs(line[76])
                Spect_Type_Source = cbs(line[77])
                cur.execute(sql, (
                    HIP_ID, RA, Decl, RA_Deg, Decl_Deg, RA_Rad, Decl_Rad, Vmag, Parallax, pm_RA, pm_Dec, BT_Mag, VT_Mag, Hip_Mag, BV_Color, VI_Color))
                cur.execute(sql_errors_flags,(
                    HIP_ID, Prox_10asec, Var_Flag, Vmag_Source, Astrom_Ref_Dbl, RA_Error, Dec_Error, Parallax_Error, pm_RA_Error, pm_Dec_Error,
                    Crl_Dec_RA, Crl_Plx_RA, Crl_Plx_Dec, Crl_pmRA_RA, Crl_pmRA_Dec, Crl_pmRA_Plx, Crl_pmDec_RA, Crl_pmDec_Dec, Crl_pmDec_Plx,
                    Crl_pmDec_pmRA, Reject_Percent, Quality_Fit, BT_Mag_Error, VT_Mag_Error, BT_Mag_Ref_Dbl, BV_Color_Error, BV_Mag_Source,
                    VI_Color_Error, VI_Color_Source, Mag_Ref_Dbl, Hip_Mag_Error, Scat_Hip_Mag, N_Obs_Hip_Mag, Hip_Mag_Ref_Dbl, Hip_Mag_Max,
                    Hip_Mag_Min, Var_Period, Hip_Var_Type, Var_Data_Annex, Var_Curv_Annex, CCDM_Id, CCDM_History, CCDM_N_Entries, CCDM_N_Comp,
                    Dbl_Mult_Annex, Astrom_Mult_Source, Dbl_Soln_Qual, Dbl_Ref_ID, Dbl_Theta, Dbl_Rho, Rho_Error, Diff_Hip_Mag, dHip_Mag_Error,
                    Survey_Star, ID_Chart, Notes, HD_Id, BD_Id, CoD_Id, CPD_Id, VI_Color_Reduct, Spect_Type, Spect_Type_Source))
                count+=1            
            except Exception as e:
                countdup+=1
                if e.args[0] != 1062:
                    print(e)
                elif verbose:
                    if e.args[0] == 1062:
                        print(e)      
    conn.commit()
    conn.close()
    if(verbose):
        print(f"{count} stars inserted | {countdup} duplicates")
                           
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
        

def dropTable(databaseName = "HIP_dev", tableName = "hip"):
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
        
def killConnections(databaseName = "HIP_dev"):
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
        kills = cur.fetchall()#list of kill commands to execute
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
    parser.add_argument("-d", "--databaseName", dest = "dName", type = str, help = "Name of the database to insert the tables into (default = 'HIP_dev')", default = "HIP_dev")
    parser.add_argument("-f", "--filePath", dest = "fPath", type = str, help = "location of the hip data file (default = None)", default = "")
    parser.add_argument("-k", "--dropTables", dest = "kill", type = bool, help = "Drop Current tables and restart DB ingestion? (default = False)", default = False)
    parser.add_argument("-v", "--verbose", dest = "verbose", type = bool, help = "Print number of duplicate/new stars to command line (default=False)", default = False)
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
    tNames = ['hip', 'hip_errors_flags']
    killConnections(args.dName)#make sure that any processes still running are closed--for DB performance
    createDatabase(args.dName)
    if args.kill:
        for i in range(len(tNames)):
            print("Dropping Tables")
            dropTable(databaseName = args.dName, tableName = tNames[i])
            createTable(databaseName = args.dName, tableName = tNames[i])
    insertTable(databaseName = args.dName, path = args.fPath, verbose = args.verbose)
   
    
    
if __name__ == "__main__":
    ingestDB()