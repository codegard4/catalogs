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



# gsc240
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
