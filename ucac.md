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

|Column Name|SQL Type|Description|
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


