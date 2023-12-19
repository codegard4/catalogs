import pymysql 
from tqdm import tqdm
import argparse
import os
import sys
import math
import time
import os.path
import numpy as np
import pandas as pd
import subprocess
import requests
import json
import random
from tqdm import tqdm
import configparser
import plotly as plt
from time import sleep


def rasAndDecs(searches=10, radius = 1):
    """
    Generates random RA and Decl values.
    Args:
        searches (int): Number of random searches to generate.
    Returns:
        Tuple: Lists of random RA and Decl values.
    """
    ras = []
    decs = []
    for _ in range(searches):
        ras.append(random.uniform(0 + (radius / 2), 360 - (radius / 2)))
        decs.append(random.uniform(-90 + (radius / 2), 90 - (radius / 2)))
    return ras,decs


def apiSearch(ra_vals, dec_vals, radius = 1, catalog = "sao2000"):
    """
    Searches the existing catalog for each ID from the list of IDs up to the predefined limit.
    Args:
        ra_vals (List): List of RA values.
        dec_vals (List): List of Decl values.
        searches (int): Number of searches to perform.
    Returns:
        List: Stars information from the API.
    """
    print("")
    print(f"API Search | Radius: {radius} | Catalog: {catalog}")
   
    successful_queries = 0
    catalogs = ['gsc240','gaia','sao2000','2mass','ucac4']
    if catalog not in catalogs:
        print(f"{catalog} is not a valid catalog")
        print(f"Choose from: {catalogs}")
    else:  
        time1 = time.time()
        times,queries = [], []
        for i in tqdm(range(len(ra_vals))):
            start = time.time()
            ra_d = ra_vals[i]
            dec_d = dec_vals[i]
            r,d = "{:.1f}".format(ra_d),"{:.1f}".format(dec_d)
            print(r,d)
            position = {"ra": ra_d, "dec": dec_d}
            params = {"position": json.dumps(position),"radius": radius,"catalog": {catalog}}
            base_url = 'https://vm-appserver.keck.hawaii.edu/catalogs-test/sources/magiq/'
            p = requests.get(f"{base_url}", params=params)
            # print(p.text)
            if p.text[0] != '{':
                successful_queries += 1
                end = time.time()
                times.append(end - start)
                queries.append(len(p.text.splitlines()) - 1)
        time2 = time.time()
        dur = '{:.2f}'.format(time2 - time1)
        avg = '{:.2f}'.format(sum(times) / len(times))
        avgstar = '{:.2f}'.format(sum(queries) / len(queries))
        percent = '{:.2f}'.format(successful_queries * 100 / len(ra_vals))
        
        print(f"It took {dur} secs to run {len(ra_vals)} queries")
        print(f"Average Query Time: {avg} | Average Stars Returned: {avgstar}")
        print(f"{percent}% of the queries were successful")
        
        # for i in range(successful_queries):
        #     r,d,t,q = '{:.2f}'.format(ra_vals[i]),'{:.2f}'.format(dec_vals[i]),'{:.2f}'.format(times[i]),'{:.2f}'.format(queries[i])
        #     print(f"|Query {i}: RA:{r} | Dec:{d} | Time Taken: {t} secs | Stars Returned: {q}|")

    return ra_vals, dec_vals, times, queries

def connectionParameters():
    """
    Returns the host, port, user, and password of the MySQL database to connect to.
    Returns:
        Tuple: (host, port, user, password)
    """
    config = configparser.ConfigParser()
    config.read('catalogs.conf')
    db_host = config['DEFAULT']['host']
    db_port = int(config['DEFAULT']['port'])
    db_user = config['DEFAULT']['user']
    db_password = config['DEFAULT']['password']
    return db_host, db_port, db_user, db_password

def connectToDatabase(db_name = None):
    """
    Returns a connection to the database.
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

              
#########################################
#------------------Fix------------------#
#########################################
def databaseCheck(ravals, decvals, radius, limit, catalog):
    """
    Queries the database for the specified table and checks the information against the API results.

    Args:
        
    Returns:
        None
    """
    limit_statement = ""
    if(limit != None):
        limit_statement = f"LIMIT {limit}"
    print("")
    print(f"SQL Query | Radius: {radius} | Catalog: {catalog}")
    time1 = time.time()
    successful_queries = 0
    i = ['gsc240','gaia','sao2000','2mass','ucac4'].index(catalog)
    dbs = ['GSC240','GAIA','SAO','2MASS','UCAC4']
    time1 = time.time()
    times,queries = [], []
    conn = connectToDatabase(db_name = dbs[i])
    cur = conn.cursor()
    radius = radius / 2
    num_queries = len(ra_vals)
    i = 0
    while i < num_queries:
        print(f"{i} / {num_queries}")
        start = time.time()
        ra_d = ra_vals[i]
        dec_d = dec_vals[i]
        print(ra_d, dec_d)
        ra1, ra2, dec1, dec2 = ra_d - radius, ra_d + radius, dec_d - radius, dec_d + radius 
        query = f"""select *,  SQRT(POW(decl_deg-1.0, 2) + POW(ra_deg-14.0, 2)) AS 
        distance from {catalog} where decl_deg < {dec2} and decl_deg > {dec1} and 
        ra_deg < {ra2} and ra_deg > {ra1} order by distance {limit_statement};
        """
        # query = f"""select * from {catalog} where decl_deg < {dec2} and decl_deg > {dec1} and 
        # ra_deg < {ra2} and ra_deg > {ra1} {limit_statement};
        # """
        cur.execute(query)
        table = cur.fetchall()
        # print(table)
        if len(table) > 0:
            successful_queries += 1
            end = time.time()
            times.append(end - start)
            queries.append(len(table))
            i += 1
        else: 
            print(query)
    time2 = time.time()
    dur = '{:.2f}'.format(time2 - time1)
    avg = '{:.2f}'.format(sum(times) / len(times))
    avgstar = '{:.2f}'.format(sum(queries) / len(queries))
    percent = '{:.2f}'.format(successful_queries * 100 / len(ra_vals))
    
    print(f"It took {dur} secs to run {len(ra_vals)} queries")
    print(f"Average Query Time: {avg} | Average Stars Returned: {avgstar}")
    print(f"{percent}% of the queries were successful")

    # for i in range(successful_queries):
    #     r,d,t,q = '{:.2f}'.format(ra_vals[i]),'{:.2f}'.format(dec_vals[i]),'{:.2f}'.format(times[i]),'{:.2f}'.format(queries[i])
    #     print(f"|Query {i}: RA:{r} | Dec:{d} | Time Taken: {t} secs | Stars Returned: {q}|")
    conn.close()
    return ra_vals, dec_vals, times, queries
    
def killConnections(databaseName = "GSC240"):
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
    Parses command-line arguments when the Python script is called.
    Args:
        in_args (List): List of command-line arguments.
    Returns:
        Namespace: Parsed arguments.
    """
    description = "Compares the API and SQL DB for performance across either catalogs or radii"
    usage = "\n{} [-d databaseName] \n".format(in_args[0])
    epilog = ""

    parser = argparse.ArgumentParser(description = description, usage = usage, epilog = epilog)
    parser.add_argument("-d", "--databaseName", dest = "dName", type = str, help = "Catalog to check ('gsc240','gaia','sao2000','2mass','ucac4')", default = "sao2000")
    parser.add_argument("-n", "--numberOfChecks", dest = "n", type = int, help = "Number of different random api/sql calls", default = 10)
    parser.add_argument("-r", "--radius", dest = "r", type = int, help = "Radius of the database/api check (Default = 4)", default = 4)
    parser.add_argument("-q", "--radiusRange", dest = "range", type = str, help = "Range of radii to check (use -z to specify increments) (Ex: 1-4) (Default = None)", default = None)
    parser.add_argument("-z", "--radiusIncrements", dest = "rinc", type = float, help = "Radii increments (use -q to specify range) ", default = None)
    parser.add_argument("-l", "--limit", dest = "l", type = int, help = "Limit SQL values returned (Default = 10) *API also has a built in limit of 10", default = None)
    parser.add_argument("-c", "--compareCatalogs", dest = "c", type = bool, help = "Compare by Catalog? (Default = False)", default = None)
    args = None
    try:
        args = parser.parse_args(in_args[1:])
    except Exception as e:
        print(e)
        parser.print_help()
        sys.exit(0) 
    return args
           

if __name__ == '__main__':
    catalogs = ['gsc240','sao2000']#,'gaia','2mass','ucac4'
    # args = parseArguments(sys.argv)
    # catalog = args.dName
    # searches = args.n
    # radius = args.r
    # limit = args.l
    # q = args.q
    # z = args.z
    # c = args.c
    ##################Testing##################
    c = True
    # q = "1-4"
    # z = .5
    q,z = None,None
    catalog = "gsc240"
    searches = 2
    # radius = 0.95
    limit = 10
    ##########################################
    if q != None:
        if z != None:
            rangeRad = q.split("-")
            start, end = int(rangeRad[0]), int(rangeRad[1])
            radii = np.arange(start, (end + z), z)
            r_api,r_sql = [], []
            ra_vals, dec_vals = rasAndDecs(searches, radius)
            for r in radii:
                radius = r
                ra_api, dec_api, times_api, stars_api = apiSearch(ra_vals, dec_vals, radius, catalog)
                ra_sql, dec_sql, times_sql, stars_sql = databaseCheck(ra_vals, dec_vals, radius, limit, catalog)
                r_api.append(times_api)
                r_sql.append(times_sql)
        plot = np.zeros(len(r_api)*3).reshape(len(r_api),3)
        for i in range(len(r_api)):
            avg_api = '{:.2f}'.format(sum(r_api[i]) / len(r_api[i]))
            avg_sql = '{:.2f}'.format(sum(r_sql[i]) / len(r_sql[i]))
            diff = '{:.2f}'.format((sum(r_api[i]) - sum(r_sql[i])) / len(r_api[i]) *100 / (sum(r_api[i]) / len(r_api[i])))
            plot[i][0] = radii[i]
            plot[i][1] = avg_api
            plot[i][2] = avg_sql
            print(f"|{radii[i]} Radius Search | API Avg. Time: {avg_api}s | SQL Avg. Time: {avg_sql}s | SQL {diff}% faster")
        df = pd.DataFrame(plot, columns=['Radius', 'API Time', 'SQL Time'])
        fig1 = px.bar(df, x = "Radius", y = "API Time", barmode = "group", color_discrete_sequence = ['dark blue'])
        fig2 = px.bar(df, x = "Radius", y = "SQL Time", barmode = "group", color_discrete_sequence = ['dark red'])
        fig = go.Figure(data = fig1.data + fig2.data)
        fig.update_layout(title = "API and MySQL Radius vs Response Time", xaxis_title = "Radius", yaxis_title = "Average Search Time (secs)", showlegend = True)
        fig.show()
    elif c:
        radius = 4
        r_api,r_sql = [], []
        ra_vals, dec_vals = rasAndDecs(searches, radius)
        with tqdm(total=10) as progbar:
            for i in range(10):
                sleep(0.1)
                progbar.update(10)
        for catalog in catalogs:
            ra_api, dec_api, times_api, stars_api = apiSearch(ra_vals, dec_vals, radius, catalog)
            ra_sql, dec_sql, times_sql, stars_sql = databaseCheck(ra_vals, dec_vals, radius, limit, catalog)
            r_api.append(times_api)
            r_sql.append(times_sql)
        plot = np.zeros(len(r_api)*3).reshape(len(r_api),3)
        for i in range(len(r_api)):
            avg_api = '{:.2f}'.format(sum(r_api[i]) / len(r_api[i]))
            avg_sql = '{:.2f}'.format(sum(r_sql[i]) / len(r_sql[i]))
            diff = '{:.2f}'.format((sum(r_api[i]) - sum(r_sql[i])) / len(r_api[i]) *100 / (sum(r_api[i]) / len(r_api[i])))
            plot[i][0] = catalogs[i]
            plot[i][1] = avg_api
            plot[i][2] = avg_sql
            print(f"|{catalogs[i]} Radius Search | API Avg. Time: {avg_api}s | SQL Avg. Time: {avg_sql}s | SQL {diff}% faster")
        df = pd.DataFrame(plot, columns=['Catalog', 'API Time', 'SQL Time'])
        fig1 = px.bar(df, x = "Catalog", y = "API Time", barmode = "group", color_discrete_sequence = ['dark blue'])
        fig2 = px.bar(df, x = "Catalog", y = "SQL Time", barmode = "group", color_discrete_sequence = ['dark red'])
        fig = go.Figure(data = fig1.data + fig2.data)
        fig.update_layout(title = "API and MySQL Radius vs Response Time", xaxis_title = "Radius", yaxis_title = "Average Search Time (secs)", showlegend = True)
        fig.show()    
        
    killConnections(catalog)
    

