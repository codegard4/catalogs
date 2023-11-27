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

|Column Name|SQL Type|Description|
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
