# sao2000
Links
=====

[SAO2000 Catalog in text format](https://cdsarc.cds.unistra.fr/viz-bin/nph-Cat/txt?I/131A)

[SAO2000 Catalog  READM](https://heasarc.gsfc.nasa.gov/W3Browse/star-catalog/sao.html)

[SAO2000 Catalog  Query](https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3table.pl?tablehead=name%3Dsao&Action=More+Options)

Requirements
============

It is recommended that this project be run with Anaconda Python 3.5 or above.

The current Python library requirements for this project are:

	pymysql 
	math
	tqdm
	argparse
	sys
	os
	numpy
	configparser

How to Run the sao2000.py File
===============================

1. Edit the catalogs.conf file under [SAO2000] to include the server host, port, user and password you wish to have the database created on.

2. Navigate to the command line and run the sao2000.py file by the 'python sao2000.py' command

*The default file will create an SAO2000_dev database with all rows of the SAO2000 catalog inserted into the sao1950 and sao2000 files

*The sao.dat file must be either in the same location as the sao2000.py file or a path to the sao.dat file must be specified

Command Line Execution
===============================

|Command|Description|Default|
|:-----:|:----------|:------|
|python sao2000.py  |creates SAO2000_dev database by pulling from the sao.dat file and adds all rows of the catalog to sao1950 and sao2000 tables||
|python sao2000.py -d |changes the name of the database that is created to store the sao catalog| SAO2000|
|python sao2000.py -f |specifies an alternate location for the sao.dat file| sao.dat|
|python sao2000.py -r |specifies the number of rows to be inserted from the sao2000 catalog| All Rows|

sao2000 Table Columns
===============================

|Column Name|SQL Type|Description|
|:-----|:----:|:----------|
|SaoNumber     | INT         | The SaoNumber of the star|
|RA            | VARCHAR(13) | Right Ascension, J2000.0, in hrs:mins:secs |
|PMRA          | FLOAT       | Right Ascension annual proper motion, J2000.0, FK5 system |
|Decl          | VARCHAR(13) | Declination, J2000.0, in degs:mins:secs|
|PMDec         | FLOAT       | Declination annual proper motion, J2000.0, FK5 system |
|RA_rad        | FLOAT       | Right Ascension, J2000.0, in radians|
|Dec_rad       | FLOAT       | Declination, J2000.0, in radians|
|RA_deg        | FLOAT       | Right Ascension, J2000.0, in degrees|
|Dec_deg       | FLOAT       | Declination, J2000.0, in degrees|
|PhotMag       | FLOAT       | Photographic magnitude|
|VMag          | FLOAT       | Visual magnitude|
|SpectralType  | VARCHAR(3)  | Spectral type, '+++' for composite spectra|
|VMag_delta    | INT         | Accuracy of V: 0 = 2 decimals, 1=1 decimal|
|PhotMag_delta | INT         | Accuracy of Ptg: 0 = 2 decimals, 1=1 decimal|

sao2000_errors_flags Table Columns
===============================

| Column               | Type          | Description                                      |
|----------------------|---------------|--------------------------------------------------|
| SaoNumber            | INT           | Sao Number                                       |
| Dup                  | VARCHAR(1)    | Duplicate Flag                                   |
| RA1950               | VARCHAR(10)   | Right Ascension at 1950                          |
| PMRA_1950            | FLOAT         | Proper Motion in Right Ascension at 1950         |
| PMRA_1950mu          | FLOAT         | Proper Motion in Right Ascension at 1950 (mu)    |
| RA2m_flag            | VARCHAR(1)    | Right Ascension 2nd moment Flag                  |
| RA1950_precessed     | FLOAT         | Precessed Right Ascension at 1950                |
| RA1950_precessed_sd  | FLOAT         | Standard Deviation of Precessed RA at 1950       |
| Original_Epoch       | FLOAT         | Original Epoch                                   |
| Dec1950              | VARCHAR(11)   | Declination at 1950                              |
| PMDec_1950           | FLOAT         | Proper Motion in Declination at 1950             |
| PMDec_1950mu         | FLOAT         | Proper Motion in Declination at 1950 (mu)        |
| D2m_Flag             | VARCHAR(1)    | Declination 2nd moment Flag                      |
| DE2s                 | FLOAT         | Declination at 1950 (2nd moment)                 |
| e_DE2                | FLOAT         | Error in Declination at 1950 (2nd moment)        |
| Dec_orig_epoch       | FLOAT         | Declination at Original Epoch                    |
| e_Pos                | FLOAT         | Error in Position                                |
| VMag_src             | INT           | Visual Magnitude (Source)                        |
| StarNum_src          | INT           | Star Number (Source)                             |
| PhotMag_src          | INT           | Photographic Magnitude (Source)                  |
| PM_src               | INT           | Proper Motion (Source)                           |
| SpecType_src         | INT           | Spectral Type (Source)                           |
| Rem                  | INT           | Remark                                           |
| SrcCatCode           | INT           | Source Catalog Code                              |
| SrcCatNum            | INT           | Source Catalog Number                            |
| Dec1950_rad          | FLOAT         | Declination at 1950 (in radians)                 |
| DurchmusterungID     | VARCHAR(14)   | Durchmusterung ID                                |
| HenryDraperCatNum    | VARCHAR(6)    | Henry Draper Catalog Number                      |
| HDDuplicateID        | VARCHAR(1)    | Henry Draper Duplicate ID                        |
| GeneralCatalogNumber1950 | VARCHAR(5) | General Catalog Number at 1950                  |
| RA1950_rad           | FLOAT         | Right Ascension at 1950 (in radians)             |
| Dec1950_rad          | FLOAT         | Declination at 1950 (in radians)                 |


# ucac4
Links
=====

[UCAC4 Catalog Column Overview](https://irsa.ipac.caltech.edu/data/UCAC4/ucac4.html)

Requirements
============

It is recommended that this project be run with Anaconda Python 3.5 or above.

The current Python library requirements for this project are:

	pymysql 
	tqdm 
	argparse  
	os
	sys 
	math
	datetime 
	numpy 
	pandas
	struct 
	random 
	configparser     


How to Run the ucac4.py File
===============================

1. Edit the catalogs.conf file under [UCAC4] to include the server host, port, user and password you wish to have the database created on.

2. Navigate to the command line and run the ucac4.py file by the 'python ucac4.py' command

3. Ensure that the ucac4 catalog is in the same folder as the ucac4.py file or that an appropriate file path is specified to reach the u4b folder and that the ucac4 zone files are in the u4b folder

Overview of possible execution commands:

|Command|Description|Default|
|:-----:|:----------|:------|
|python ucac4.py|creates UCAC4_dev database by pulling from the zone files in the u4b folder of the catalog and adds all rows of the catalog to ucac4, ucac4_errors_flags, ucac4_not_visible, and ucac4_errors_flags_not_visible tables||
|python ucac4.py -d|specifies the name of the database to insert the four tables into|"UCAC4_dev"|
|python ucac4.py -n|specifies the number of zone files that should be inserted. For full insertion leave blank|900|
|python ucac4.py -f|specifies the path to the ucac4 zone files path should be "../location/u4b"|u4b|
|python ucac4.py -t|specifies the names of the tables that should be created. Should only be changed to remove _not_visible files|ucac4, ucac4_errors_flags,ucac4_not_visible, ucac4_errors_flags_not_visible|
|python ucac4.py -r|specifies whether the files should be randomly or uniformly chosen for insertion. If r==True then files will be randomly chosen up to the specified number of files|False|


Overview of ucac4 table columns
===============================

|Column Name|SQL Type|Description|
|:-----|:----:|:----------|
|UCAC_ID       | INT         | The unique UCAC ID for the star |
|2MASS_ID      | INT         | The unique ID for the star in the 2MASS catalog|
|RA            | VARCHAR(13) | Right ascension, J2000.0, in hrs:mins:secs |
|Decl          | VARCHAR(13) | Declination, J2000.0, in degs:mins:secs|
|RA_deg        | FLOAT       | Right ascension, J2000.0, in degrees|
|Decl_deg      | FLOAT       | Declination, J2000.0, in degrees|
|RA_orig       | INT         | Original Catalog Right Ascension, J2000.0 |
|Decl_orig     | INT         | Original Catalog Declination, J2000.0 |
|MagModel      | FLOAT       | Model Magnitude converted to mag units|
|MagApperature | FLOAT       | Model Aperture converted to mag units|
|Objt          | INT         | Object type|
|Cdf           | INT         | Combined double star flag|
|SigRA         | INT         | Right Ascension epoch standard error|
|SigDec        | INT         | Declination epoch standard error|
|CepRA         | FLOAT       | Right Ascension epoch converted to years|
|CepDec        | FLOAT       | Declination epoch converted to years|
|PmRA          | FLOAT       | Right Ascension proper motion, J2000.0|
|PmDec         | FLOAT       | Declination proper motion, J2000.0 |
|SigPmRA       | INT         | Right Ascension proper motion, J2000.0, standard error|
|SigPmDec      | INT         | Declination proper motion, J2000.0, standard error|
|2MASS_J       | FLOAT       | J Magnitude 2MASS Catalog|
|2MASS_H       | FLOAT       | H Magnitude 2MASS Catalog|
|2MASS_K       | FLOAT       | K Magnitude 2MASS Catalog|
|APASS_B       | FLOAT       | B Magnitude APASS Catalog|
|APASS_V       | FLOAT       | V Magnitude APASS Catalog|
|APASS_g       | FLOAT       | g Magnitude APASS Catalog|
|APASS_r       | FLOAT       | r Magnitude APASS Catalog|
|APASS_i       | FLOAT       | i Magnitude APASS Catalog|

Overview of ucac4_errors_flags table columns
===============================

| Column         | SQL Type | Description                                       |
|----------------|----------|---------------------------------------------------|
| UCAC_ID        | INT      | Primary Key                                       |
| SigMag         | FLOAT    | Significant Magnitude                            |
| Na1            | INT      | Na1                                               |
| Nu1            | INT      | Nu1                                               |
| Cu1            | INT      | Cu1                                               |
| icqflg_J       | INT      | ICQ Flag for J Band                              |
| icqflg_H       | INT      | ICQ Flag for H Band                              |
| icqflg_K       | INT      | ICQ Flag for K Band                              |
| e2mpho_J       | INT      | Error in 2MASS Photometry for J Band             |
| e2mpho_H       | INT      | Error in 2MASS Photometry for H Band             |
| e2mpho_K       | INT      | Error in 2MASS Photometry for K Band             |
| APASS_B_err    | INT      | Error in APASS B Band Magnitude                  |
| APASS_V_err    | INT      | Error in APASS V Band Magnitude                  |
| APASS_g_err    | INT      | Error in APASS g Band Magnitude                  |
| APASS_r_err    | INT      | Error in APASS r Band Magnitude                  |
| APASS_i_err    | INT      | Error in APASS i Band Magnitude                  |
| gcflg          | INT      | Yale San Juan first epoch Southern Proper Motion|
| icf            | VARCHAR(20) | ICF                                            |
| leda           | INT      | LEDA                                              |
| x2m            | INT      | X2M                                               |
| zn2            | INT      | Zone Astrog. catalog match flag                   |
| rn2            | INT      | NPM Lick catalog match flag                      |



How to Run the gsc240.py File
===============================

1. Edit the catalogs.conf file under [GSC240] to include the server host, port, user and password you wish to have the database created on.

2. Navigate to the command line and run the ucac4.py file by the 'python gsc240.py' command

3. Ensure that the gsc240 catalog is in the same folder as the gsc240.py file or that an appropriate file path is specified to reach the csv folder

Overview of possible execution commands:

| Command                  | Description                                                                         | Default                |
| :-----------------------: | :---------------------------------------------------------------------------------- | :---------------------- |
| python gsc240.py -d      | Name of the database to insert the tables into                                    | "GSC240_dev"            |
| python gsc240.py -n      | Number of Dec files to insert into the database                                  | 180                    |
| python gsc240.py -f      | Location of the GSC240 CSV folder                                                | "../gsc240/csv"         |
| python gsc240.py -t      | Names of the tables to be created                                                 | ['gsc240', 'gsc240_errors_flags', 'gsc240_not_visible', 'gsc240_errors_flags_not_visible'] |
| python gsc240.py -r      | Randomly select files to insert?                                                  | False                  |
| python gsc240.py -m      | Manually insert a file or set of files                                            | None                   |
| python gsc240.py -k      | Drop current tables and restart DB ingestion                                     | False                  |


Overview of gsc240 table columns
===============================

| Column Name     | SQL Type      |
| :-------------- | :------------ | 
| GSCID           | INT           | 
| GSC1ID          | VARCHAR(11)   |             
| HSTID           | VARCHAR(11)   |             
| RA              | VARCHAR(13)   |             
| DECL            | VARCHAR(13)   |             
| RA_rad          | DOUBLE        |             
| Decl_rad        | DOUBLE        |             
| RA_deg          | DOUBLE        |            
| Decl_deg        | DOUBLE        |             
| Original_Epoch  | REAL          |             
| RA_eps          | REAL          |            
| Decl_eps        | REAL          |            
| PmRA            | REAL          |            
| PmDec           | REAL          |             
| Delta_Epoch     | REAL          |             
| FpgMag          | REAL          |            
| JpgMag          | REAL          |             
| VMag            | REAL          |             
| NpgMag          | REAL          |             
| UMag            | REAL          |            
| BMag            | REAL          |             
| RMag            | REAL          |             
| IMag            | REAL          |             
| JMag            | REAL          |             
| HMag            | REAL          |             
| KMag            | REAL          |             
| Classification  | INT           |             
| SemiMajorAxis   | REAL          |             
| Eccentricity    | REAL          |             
| PositionAngle   | REAL          |            
| SourceStatus    | INT           |             

Overview of gsc240_errors_flags table columns
===============================

| Column Name  | SQL Type   | 
| :----------- | :--------- | 
| GSCID        | INT        |             
| GSC1ID       | VARCHAR(11)|            
| HSTID        | VARCHAR(11)|            
| PmRA_mu      | REAL       |             
| PmDec_mu     | REAL       |             
| FpgMag_err   | REAL       |             
| FpgMag_code  | INT        |             
| JpgMag_err   | REAL       |             
| JpgMag_code  | INT        |             
| VMag_err     | REAL       |             
| VMag_code    | INT        |             
| NpgMag_err   | REAL       |             
| NpgMag_code  | INT        |             
| UMag_err     | REAL       |             
| UMag_code    | INT        |             
| BMag_err     | REAL       |             
| BMag_code    | INT        |             
| RMag_err     | REAL       |             
| RMag_code    | INT        |             
| IMag_err     | REAL       |             
| IMag_code    | INT        |             
| JMag_err     | REAL       |             
| JMag_code    | INT        |             
| HMag_err     | REAL       |             
| HMag_code    | INT        |             
| KMag_err     | REAL       |             
| KMag_code    | INT        |             
| VariableFlag | INT        |             
| MultipleFlag | INT        |             
