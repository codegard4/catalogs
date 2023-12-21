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
import gzip


def connectionParameters():
    """
    Returns the host, port, user, and password of the MySQL database to connect to.
    Args:
        None
    Returns:
        Tuple: (str, int, str, str) - host, port, user, password
    """
    config = configparser.ConfigParser()
    path = '/'.join((os.path.abspath("catalogs.conf").replace('\\', '/')).split('/')[:-1])
    config.read(os.path.join(path, 'catalogs.conf'))
    db_host = config['GAIA']['host']
    db_port = int(config['GAIA']['port'])
    db_user = config['GAIA']['user']
    db_password = config['GAIA']['password']
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
        conn = pymysql.connect(host = db_host, port = db_port, user = db_user, password = db_password,autocommit=True)
    else:
        conn = pymysql.connect(host = db_host, port = db_port, user = db_user, password = db_password, database = db_name,autocommit=True)
    return conn
    
def cnm(mag):
    """
    Checks null mag values and changes 99.9 values to NULL.
    Args:
        mag (float): Magnitude value.
    Returns:
        float or None: Returns mag if not 99.9, otherwise returns None.
    """
    if mag == 999.9:
        return None
    return round(mag, 6)

    
def createDatabase(databaseName = "GAIA_dev"): 
    """
    Creates the GSC240 database if it doesn't already exist.
    Args:
        databaseName (str): Name of the database. Default is "GSC240_dev".
    Returns:
        None
    """
    try:
        conn = connectToDatabase()
        cur = conn.cursor()
        cur.execute(f'CREATE DATABASE {databaseName};')
        conn.commit()
        conn.close()
        print(f"DB {databaseName} created")
    except:
        print("DB already created")
        pass
    
def createTable(databaseName = "GAIA_dev", tableName = "gaia"): 
    """
    Creates the specified table.
    Args:
        databaseName (str): Name of the database.
        tableName (str): Name of the table.
    """
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    if tableName == 'gaia' or tableName == 'gaia_not_visible':
       
        query = f"""CREATE TABLE {tableName} (\
                GAIA_ID VARCHAR(30) PRIMARY KEY,\
                RA VARCHAR(13),\
                Decl VARCHAR(13),\
                Ra_deg DOUBLE,\
                Decl_deg DOUBLE,\
                Ra_rad DOUBLE,\
                Decl_rad DOUBLE,\
                Epoch FLOAT,\
                pmra REAL,\
                pmdec REAL,\
                gmag REAL,\
                bpmag REAL,\
                rpmag REAL,\
                radial_velocity FLOAT,\
                parallax DOUBLE\
                );\
            """
        cur.execute(query)
        print(f"{tableName} created")
    elif tableName == 'gaia_errors_flags' or tableName == 'gaia_errors_flags_not_visible':
        query = f"""CREATE TABLE {tableName} (\
        GAIA_ID VARCHAR(30) PRIMARY KEY,\
        source_id BIGINT,\
        solution_id BIGINT,\
        random_index BIGINT,\
        ra_error FLOAT,\
        dec_error FLOAT,\
        parallax_error FLOAT,\
        parallax_over_error FLOAT,\
        pmra_error FLOAT,\
        pmdec_error FLOAT,\
        ra_dec_corr FLOAT,\
        ra_parallax_corr FLOAT,\
        ra_pmra_corr FLOAT,\
        ra_pmdec_corr FLOAT,\
        dec_parallax_corr FLOAT,
        dec_pmra_corr FLOAT,\
        dec_pmdec_corr FLOAT,\
        parallax_pmra_corr FLOAT,\
        parallax_pmdec_corr FLOAT,\
        pmra_pmdec_corr FLOAT,\
        astrometric_n_obs_al INT,\
        astrometric_n_obs_ac INT,\
        astrometric_n_good_obs_al INT,\
        astrometric_n_bad_obs_al INT,\
        astrometric_gof_al FLOAT,\
        astrometric_chi2_al FLOAT,\
        astrometric_excess_noise FLOAT,\
        astrometric_excess_noise_sig FLOAT,\
        astrometric_params_solved INT,\
        astrometric_primary_flag BOOLEAN,\
        astrometric_weight_al FLOAT,\
        astrometric_pseudo_colour FLOAT,\
        astrometric_pseudo_colour_error FLOAT,\
        mean_varpi_factor_al FLOAT,\
        astrometric_matched_observations INT,\
        visibility_periods_used INT,\
        astrometric_sigma5d_max FLOAT,\
        frame_rotator_object_type INT,\
        matched_observations INT,\
        duplicated_source BOOLEAN,\
        phot_g_n_obs INT,\
        phot_g_mean_flux FLOAT,\
        phot_g_mean_flux_error FLOAT,\
        phot_g_mean_flux_over_error FLOAT,\
        phot_bp_n_obs INT,\
        phot_bp_mean_flux FLOAT,\
        phot_bp_mean_flux_error FLOAT,\
        phot_bp_mean_flux_over_error FLOAT,\
        phot_rp_n_obs INT,\
        phot_rp_mean_flux FLOAT,\
        phot_rp_mean_flux_error FLOAT,\
        phot_rp_mean_flux_over_error FLOAT,\
        phot_bp_rp_excess_factor FLOAT,\
        phot_proc_mode VARCHAR(10),\
        bp_rp FLOAT,\
        bp_g FLOAT,\
        g_rp FLOAT,\
        radial_velocity_error FLOAT,\
        rv_nb_transits INT,\
        rv_template_teff INT,\
        rv_template_logg INT,\
        rv_template_fe_h INT,\
        phot_variable_flag VARCHAR(8),\
        l FLOAT,\
        b FLOAT,\
        ecl_lon FLOAT,\
        ecl_lat FLOAT,\
        priam_flags INT,\
        teff_val FLOAT,\
        teff_percentile_lower FLOAT,\
        teff_percentile_upper FLOAT,\
        a_g_val FLOAT,\
        a_g_percentile_lower FLOAT,\
        a_g_percentile_upper FLOAT,\
        e_bp_min_rp_val FLOAT,\
        e_bp_min_rp_percentile_lower FLOAT,\
        e_bp_min_rp_percentile_upper FLOAT,\
        flame_flags INT,\
        radius_val FLOAT,\
        radius_percentile_lower FLOAT,\
        radius_percentile_upper FLOAT,\
        lum_val FLOAT,\
        lum_percentile_lower FLOAT,\
        lum_percentile_upper FLOAT);\
        """    
        cur.execute(query)
        print(f"{tableName} created")
    conn.commit()
    conn.close()
    
def cbf(value):
    """
    Check Blank Float: Checks for blank float inputs.
    Args:
        value (str): The input value to be converted to float.
    Returns:
        float or None: The converted float value or None if the input is an empty string.
    """
    if value == '':
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
    if value == '':
        return None
    return int(float(value))


def cbb(value):
    """
    Check Blank Boolean: Checks for blank boolean inputs.
    Args:
        value (str): The input value to be converted to boolean.
    Returns:
        bool or None: The converted boolean value or None if the input is an empty string.
    """
    if value == '':
        return None
    return bool(value)


def cpvf(value):
    """
    Check Phot Variable Flag: Checks phot_variable_flag input for null.
    Args:
        value (str): The input value.
    Returns:
        str or None: The input value or None if the input is "NOT_AVAILABLE".
    """
    if value == "NOT_AVAILABLE":
        return None
    return str(value)


def viewTable(databaseName = "GAIA_dev", tableName = "gaia"):
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
          
def insertTable(databaseName = "GAIA_dev", tableNames = [], directName = "file-aa-dir", verbose = False): 
    """
    description:
        Inserts data into four tables based on the provided catalog files in the specified directory.
    args:
        databaseName (str): Name of the database to connect to (default is "GAIA_dev").
        tableNames (list): List of table names to insert data into (default is an empty list).
        directName (str): Name of the directory containing CSV files (default is "file-aa-dir").
    returns:
        None
    """
    sql_gaia = f"""INSERT INTO gaia (\
        GAIA_ID, RA, Decl, Ra_deg, Decl_deg, Ra_rad, Decl_rad, Epoch, pmra, pmdec, gmag, bpmag, rpmag, radial_velocity, parallax) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);\
        """
    sql_gaia_nv = f"""INSERT INTO gaia_not_visible (\
        GAIA_ID, RA, Decl, Ra_deg, Decl_deg, Ra_rad, Decl_rad, Epoch, pmra, pmdec, gmag, bpmag, rpmag, radial_velocity, parallax) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);\
        """
    sql_gaia_ef = f"""INSERT INTO gaia_errors_flags (\
        GAIA_ID, solution_id, source_id, random_index, ra_error, dec_error, parallax_error, parallax_over_error,\
        pmra_error, pmdec_error, ra_dec_corr, ra_parallax_corr, ra_pmra_corr, ra_pmdec_corr,\
        dec_parallax_corr, dec_pmra_corr, dec_pmdec_corr, parallax_pmra_corr, parallax_pmdec_corr,\
        pmra_pmdec_corr, astrometric_n_obs_al, astrometric_n_obs_ac, astrometric_n_good_obs_al,\
        astrometric_n_bad_obs_al, astrometric_gof_al, astrometric_chi2_al, astrometric_excess_noise,\
        astrometric_excess_noise_sig, astrometric_params_solved, astrometric_primary_flag,\
        astrometric_weight_al, astrometric_pseudo_colour, astrometric_pseudo_colour_error,\
        mean_varpi_factor_al, astrometric_matched_observations, visibility_periods_used,\
        astrometric_sigma5d_max, frame_rotator_object_type, matched_observations, duplicated_source,\
        phot_g_n_obs, phot_g_mean_flux, phot_g_mean_flux_error, phot_g_mean_flux_over_error,\
        phot_bp_n_obs, phot_bp_mean_flux, phot_bp_mean_flux_error, phot_bp_mean_flux_over_error,\
        phot_rp_n_obs, phot_rp_mean_flux, phot_rp_mean_flux_error, phot_rp_mean_flux_over_error,\
        phot_bp_rp_excess_factor, phot_proc_mode, bp_rp, bp_g, g_rp, \
        radial_velocity_error, rv_nb_transits, rv_template_teff, rv_template_logg, rv_template_fe_h,\
        phot_variable_flag, l, b, ecl_lon, ecl_lat, priam_flags, teff_val, teff_percentile_lower,\
        teff_percentile_upper, a_g_val, a_g_percentile_lower, a_g_percentile_upper, e_bp_min_rp_val,\
        e_bp_min_rp_percentile_lower, e_bp_min_rp_percentile_upper, flame_flags, radius_val,\
        radius_percentile_lower, radius_percentile_upper, lum_val, lum_percentile_lower, lum_percentile_upper) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); \
        """
    sql_gaia_ef_nv = f"""INSERT INTO gaia_errors_flags_not_visible (\
        GAIA_ID, solution_id, source_id, random_index, ra_error, dec_error, parallax_error, parallax_over_error,\
        pmra_error, pmdec_error, ra_dec_corr, ra_parallax_corr, ra_pmra_corr, ra_pmdec_corr,\
        dec_parallax_corr, dec_pmra_corr, dec_pmdec_corr, parallax_pmra_corr, parallax_pmdec_corr,\
        pmra_pmdec_corr, astrometric_n_obs_al, astrometric_n_obs_ac, astrometric_n_good_obs_al,\
        astrometric_n_bad_obs_al, astrometric_gof_al, astrometric_chi2_al, astrometric_excess_noise,\
        astrometric_excess_noise_sig, astrometric_params_solved, astrometric_primary_flag,\
        astrometric_weight_al, astrometric_pseudo_colour, astrometric_pseudo_colour_error,\
        mean_varpi_factor_al, astrometric_matched_observations, visibility_periods_used,\
        astrometric_sigma5d_max, frame_rotator_object_type, matched_observations, duplicated_source,\
        phot_g_n_obs, phot_g_mean_flux, phot_g_mean_flux_error, phot_g_mean_flux_over_error,\
        phot_bp_n_obs, phot_bp_mean_flux, phot_bp_mean_flux_error, phot_bp_mean_flux_over_error,\
        phot_rp_n_obs, phot_rp_mean_flux, phot_rp_mean_flux_error, phot_rp_mean_flux_over_error,\
        phot_bp_rp_excess_factor, phot_proc_mode, bp_rp, bp_g, g_rp,\
        radial_velocity_error, rv_nb_transits, rv_template_teff, rv_template_logg, rv_template_fe_h,\
        phot_variable_flag, l, b, ecl_lon, ecl_lat, priam_flags, teff_val, teff_percentile_lower,\
        teff_percentile_upper, a_g_val, a_g_percentile_lower, a_g_percentile_upper, e_bp_min_rp_val,\
        e_bp_min_rp_percentile_lower, e_bp_min_rp_percentile_upper, flame_flags, radius_val,\
        radius_percentile_lower, radius_percentile_upper, lum_val, lum_percentile_lower, lum_percentile_upper) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); \
        """
    conn = connectToDatabase(db_name = databaseName)
    cur = conn.cursor()
    try:
        directory = os.getcwd()
        os.chdir(f"{directName}")
        if(verbose):
            print(f"Current Directory: {os.getcwd()}")
        count,counterror=0,0
        for filename in tqdm(os.listdir(os.getcwd())):
            try:
                with open(filename, 'r') as f:
                    reader = csv.reader(f)
                    for line in reader:
                        try:
                            count+=1
                            check = line[2]
                            if check == 'source_id':
                                pass
                            else:
                                solution_id = cbi(line[0])
                                designation = line[1]
                                source_id = cbi(line[2])
                                random_index = cbi(line[3])
                                ref_epoch = cbf(line[4])
                                ra_deg = cbf(line[5])
                                dec_deg = cbf(line[7])
                                ra_rad = degToRad(ra_deg)
                                dec_rad = degToRad(dec_deg)
                                ra = deg2SexagHrs(ra_deg)
                                dec = deg2Sexag(dec_deg)
                                ra_error = cbf(line[6])
                                dec_error = cbf(line[8])
                                parallax = cbf(line[9])
                                parallax_error = cbf(line[10])
                                parallax_over_error = cbf(line[11])
                                pmra = cbf(line[12])
                                pmra_error = cbf(line[13])
                                pmdec = cbf(line[14])
                                pmdec_error = cbf(line[15])
                                ra_dec_corr = cbf(line[16])
                                ra_parallax_corr = cbf(line[17])
                                ra_pmra_corr = cbf(line[18])
                                ra_pmdec_corr = cbf(line[19])
                                dec_parallax_corr = cbf(line[20])
                                dec_pmra_corr = cbf(line[21])
                                dec_pmdec_corr = cbf(line[22])
                                parallax_pmra_corr = cbf(line[23])
                                parallax_pmdec_corr = cbf(line[24])
                                pmra_pmdec_corr = cbf(line[25])
                                astrometric_n_obs_al = cbi(line[26])
                                astrometric_n_obs_ac = cbi(line[27])
                                astrometric_n_good_obs_al = cbi(line[28])
                                astrometric_n_bad_obs_al = cbi(line[29])
                                astrometric_gof_al = cbf(line[30])
                                astrometric_chi2_al = cbf(line[31])
                                astrometric_excess_noise = cbf(line[32])
                                astrometric_excess_noise_sig = cbf(line[33])
                                astrometric_params_solved = cbi(line[34])
                                astrometric_primary_flag = cbb(line[35])
                                astrometric_weight_al = cbf(line[36])
                                astrometric_pseudo_colour = cbf(line[37])
                                astrometric_pseudo_colour_error = cbf(line[38])
                                mean_varpi_factor_al = cbf(line[39])
                                astrometric_matched_observations = cbi(line[40])
                                visibility_periods_used = cbi(line[41])
                                astrometric_sigma5d_max = cbf(line[42])
                                frame_rotator_object_type = cbi(line[43])
                                matched_observations = cbi(line[44])
                                duplicated_source = cbb(line[45])
                                phot_g_n_obs = cbi(line[46])
                                phot_g_mean_flux = cbf(line[47])
                                phot_g_mean_flux_error = cbf(line[48])
                                phot_g_mean_flux_over_error = cbf(line[49])
                                phot_g_mean_mag = cbf(line[50])
                                phot_bp_n_obs = cbi(line[51])
                                phot_bp_mean_flux = cbf(line[52])
                                phot_bp_mean_flux_error = cbf(line[53])
                                phot_bp_mean_flux_over_error = cbf(line[54])
                                phot_bp_mean_mag = cbf(line[55])
                                phot_rp_n_obs = cbi(line[56])
                                phot_rp_mean_flux = cbf(line[57])
                                phot_rp_mean_flux_error = cbf(line[58])
                                phot_rp_mean_flux_over_error = cbf(line[59])
                                phot_rp_mean_mag = cbf(line[60])
                                phot_bp_rp_excess_factor = cbf(line[61])
                                phot_proc_mode = str(line[62])
                                bp_rp = cbf(line[63])
                                bp_g = cbf(line[64])
                                g_rp = cbf(line[65])
                                radial_velocity = cbf(line[66])
                                radial_velocity_error = cbf(line[67])
                                rv_nb_transits = cbf(line[68])
                                rv_template_teff = cbf(line[69])
                                rv_template_logg = cbf(line[70])
                                rv_template_fe_h = cbf(line[71])
                                phot_variable_flag = cpvf(line[72])
                                l = cbf(line[73])
                                b = cbf(line[74])
                                ecl_lon = cbf(line[75])
                                ecl_lat = cbf(line[76])
                                priam_flags = cbf(line[77])
                                teff_val = cbf(line[78])
                                teff_percentile_lower = cbf(line[79])
                                teff_percentile_upper = cbf(line[80])
                                a_g_val = cbf(line[81])
                                a_g_percentile_lower = cbf(line[82])
                                a_g_percentile_upper = cbf(line[83])
                                e_bp_min_rp_val = cbf(line[84])
                                e_bp_min_rp_percentile_lower = cbf(line[85])
                                e_bp_min_rp_percentile_upper = cbf(line[86])
                                flame_flags = cbf(line[87])
                                radius_val = cbf(line[88])
                                radius_percentile_lower = cbf(line[89])
                                radius_percentile_upper = cbf(line[90])
                                lum_val = cbf(line[91])
                                lum_percentile_lower = cbf(line[92])
                                lum_percentile_upper = cbf(line[93])
                                if dec_deg < -70.:
                                    conn = connectToDatabase(db_name = databaseName)
                                    cur = conn.cursor()
                                    cur.execute(sql_gaia_ef_nv,(designation, solution_id, source_id, 
                                        random_index, ra_error, dec_error, parallax_error, parallax_over_error, 
                                        pmra_error, pmdec_error, ra_dec_corr, ra_parallax_corr, ra_pmra_corr, 
                                        ra_pmdec_corr, dec_parallax_corr, dec_pmra_corr, dec_pmdec_corr, parallax_pmra_corr, 
                                        parallax_pmdec_corr, pmra_pmdec_corr, astrometric_n_obs_al, astrometric_n_obs_ac, 
                                        astrometric_n_good_obs_al, astrometric_n_bad_obs_al, astrometric_gof_al, 
                                        astrometric_chi2_al, astrometric_excess_noise, astrometric_excess_noise_sig, 
                                        astrometric_params_solved, astrometric_primary_flag, astrometric_weight_al, 
                                        astrometric_pseudo_colour, astrometric_pseudo_colour_error, mean_varpi_factor_al, 
                                        astrometric_matched_observations, visibility_periods_used, astrometric_sigma5d_max, 
                                        frame_rotator_object_type, matched_observations, duplicated_source, phot_g_n_obs, 
                                        phot_g_mean_flux, phot_g_mean_flux_error, phot_g_mean_flux_over_error, 
                                        phot_bp_n_obs, phot_bp_mean_flux, phot_bp_mean_flux_error, phot_bp_mean_flux_over_error, 
                                        phot_rp_n_obs, phot_rp_mean_flux, phot_rp_mean_flux_error, phot_rp_mean_flux_over_error, 
                                        phot_bp_rp_excess_factor, phot_proc_mode, bp_rp, bp_g, g_rp, 
                                        radial_velocity_error, rv_nb_transits, rv_template_teff, rv_template_logg, 
                                        rv_template_fe_h, phot_variable_flag, l, b, ecl_lon, ecl_lat, priam_flags, 
                                        teff_val, teff_percentile_lower, teff_percentile_upper, a_g_val, a_g_percentile_lower, 
                                        a_g_percentile_upper, e_bp_min_rp_val, e_bp_min_rp_percentile_lower, e_bp_min_rp_percentile_upper,
                                        flame_flags, radius_val, radius_percentile_lower, radius_percentile_upper, 
                                        lum_val, lum_percentile_lower, lum_percentile_upper))
                                    cur.execute(sql_gaia_nv,(designation,ra,dec,ra_deg,dec_deg,ra_rad,dec_rad,
                                        ref_epoch,pmra,pmdec,phot_g_mean_mag,phot_bp_mean_mag,phot_rp_mean_mag,radial_velocity, parallax))
                                    conn.commit()
                                else:
                                    cur.execute(sql_gaia_ef,(designation, solution_id, source_id, 
                                        random_index, ra_error, dec_error, parallax_error, parallax_over_error, 
                                        pmra_error, pmdec_error, ra_dec_corr, ra_parallax_corr, ra_pmra_corr, 
                                        ra_pmdec_corr, dec_parallax_corr, dec_pmra_corr, dec_pmdec_corr, parallax_pmra_corr, 
                                        parallax_pmdec_corr, pmra_pmdec_corr, astrometric_n_obs_al, astrometric_n_obs_ac, 
                                        astrometric_n_good_obs_al, astrometric_n_bad_obs_al, astrometric_gof_al, 
                                        astrometric_chi2_al, astrometric_excess_noise, astrometric_excess_noise_sig, 
                                        astrometric_params_solved, astrometric_primary_flag, astrometric_weight_al, 
                                        astrometric_pseudo_colour, astrometric_pseudo_colour_error, mean_varpi_factor_al, 
                                        astrometric_matched_observations, visibility_periods_used, astrometric_sigma5d_max, 
                                        frame_rotator_object_type, matched_observations, duplicated_source, phot_g_n_obs, 
                                        phot_g_mean_flux, phot_g_mean_flux_error, phot_g_mean_flux_over_error, 
                                        phot_bp_n_obs, phot_bp_mean_flux, phot_bp_mean_flux_error, phot_bp_mean_flux_over_error, 
                                        phot_rp_n_obs, phot_rp_mean_flux, phot_rp_mean_flux_error, phot_rp_mean_flux_over_error, 
                                        phot_bp_rp_excess_factor, phot_proc_mode, bp_rp, bp_g, g_rp, 
                                        radial_velocity_error, rv_nb_transits, rv_template_teff, rv_template_logg, 
                                        rv_template_fe_h, phot_variable_flag, l, b, ecl_lon, ecl_lat, priam_flags, 
                                        teff_val, teff_percentile_lower, teff_percentile_upper, a_g_val, a_g_percentile_lower, 
                                        a_g_percentile_upper, e_bp_min_rp_val, e_bp_min_rp_percentile_lower, e_bp_min_rp_percentile_upper,
                                        flame_flags, radius_val, radius_percentile_lower, radius_percentile_upper, 
                                        lum_val, lum_percentile_lower, lum_percentile_upper))
                                    cur.execute(sql_gaia,(designation,ra,dec,ra_deg,dec_deg,ra_rad,dec_rad,
                                        ref_epoch,pmra,pmdec,phot_g_mean_mag,phot_bp_mean_mag,phot_rp_mean_mag,radial_velocity, parallax))
                                    conn.commit()
                        except Exception as e:
                            if e.args[0] != 1062:
                                print(e)
                                print(line)
                            # print(e)
                            counterror+=1
            except Exception as e:
                if(verbose):
                    print(f"File Error: {e}")
        if(verbose):
            print(f"{count} new stars and {counterror} duplicates")
        os.chdir(directory)
    except Exception as e: 
        print(f"Directory Error: {e}")
    conn.ping()
    conn.close()
                    
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
    
def radToDeg(radians):
    """
    Converts radians to degrees.
    Args:
        radians (float): Radian value.
    Returns:
        float: Degree value.
    """
    return math.degrees(radians)

def degToRad(degrees):
    """
    Converts degrees to radians.
    Args:
        degrees (float): Degree value.
    Returns:
        float: Radian value.
    """
    return math.radians(degrees)
        
def folderRange(start_folder, end_folder):
    # Extract the prefix and suffix from the start and end folders
    folders = []
    start_prefix, start_suffix = start_folder[:1], start_folder[1:]
    end_prefix, end_suffix = end_folder[:1], end_folder[1:]
    print(start_prefix, start_suffix, end_prefix, end_suffix)
    current_folder = start_folder
    while current_folder <= end_folder:
        folders.append(current_folder)
        prefix, suffix = current_folder[:1], current_folder[1:]
        if suffix == 'z':
            current_folder = chr(ord(prefix) + 1) + 'a'
        else:
            current_folder = prefix + chr(ord(suffix) + 1)
    return folders

def dropTable(databaseName = "GAIA_dev", tableName = "gaia"):
    """
    Deletes the specified table.
    Args:
        databaseName (str): Name of the database.
        tableName (str): Name of the table.
    """
    try: 
        print("dropping table")
        conn = connectToDatabase(db_name = databaseName)
        cur = conn.cursor()
        cur.execute(f"DROP TABLE {tableName};")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        
def killConnections(databaseName = "GAIA_dev"):
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
        print("Killing connections")
    except:
        print("Could not kill connections")

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
    parser.add_argument("-d", "--databaseName", dest = "dName", type = str, help = "Name of the database to insert the tables into (default = 'GAIA_dev')", default = "GAIA_dev")
    parser.add_argument("-n", "--NumFiles", dest = "fNum", type = int, help = "Number of files to randomly insert into the database (default = 307)", default = 307)
    parser.add_argument("-r", "--randomInsertion", dest ="rIns", type = bool, help = "Randomly select folders to insert? (default = F)", default = False)
    parser.add_argument("-mr", "--manualRange", dest = "mr", type = str, help = "Start insertion from a folder and end at a folder (default: aa,lu)", default = "aa,lu")
    parser.add_argument("-k", "--dropTables", dest = "kill", type = bool, help = "Drop Current tables and restart DB ingestion? (default = False)", default = False)
    parser.add_argument("-f", "--filePath", dest = "path", type = str, help = "path to reach gaia catalog unzipped files (default = None)", default = "")
    parser.add_argument("-v", "--verbose", dest = "verbose", type = bool, help = "Print errors & star numbers (default = False", default = False)
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
    Args:
        None
    Returns:
        None
    """
    letters = [chr(letter) for letter in range(ord('a'), ord('z') + 1)]
    path = os.path.abspath("gaia_unzipped.py")
    tNames =['gaia','gaia_errors_flags','gaia_not_visible','gaia_errors_flags_not_visible']
    args = parseArguments(sys.argv) 
    numFiles = args.fNum
    frange = args.mr.split(",")
    start, end = frange[0], frange[1]
    killConnections()
    createDatabase(args.dName)
    if args.kill:
        for i in range(len(tNames)):
            print("Drop statement: Dropping Tables")
            dropTable(databaseName = args.dName, tableName = tNames[i])
            createTable(databaseName = args.dName, tableName = tNames[i])
    if len(args.mr) > 0:
        print("Range Insertion")
        folders = folderRange(start, end)
        for folder in tqdm(folders):
            dirName = f"{args.path}file-{folder}-dir"
            print(f"{folder}")
            insertTable(databaseName = args.dName, tableNames = tNames, directName = dirName, verbose = args.verbose)
    elif args.rIns:
        print("Random Insertion")
        dirs = []
        for i in tqdm(range(args.fNum)):
            letter1, letter2 = letters[int(random.uniform(0,25))],letters[int(random.uniform(0,25))]
            dirName = f"{args.path}file-{letter1}{letter2}-dir"
            dirs.append(dirName)
            insertTable(databaseName = args.dName, tableNames = tNames, directName = dirName, verbose = args.verbose)
        print(dirs)
if __name__ == "__main__":
    ingestDB()