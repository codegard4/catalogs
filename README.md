# UNIVERSAL CATALOG FEATURES

Universal Import Requirements
============

It is recommended that this project be run with Anaconda Python 3.5 or above.

The current Python library requirements for this project are:

	pymysql 
	tqdm 
	argparse  
	os
	sys 
	math
	numpy 
	pandas
	configparser  

Universal Commands
==================
|Command|Description|
|:-----:|:----------|
|python filename.py -d |changes the name of the database that is created; should be each catalog in caps with numbers removed (Ex: sao2000-->SAO)|
|python filename.py -f |specifies an alternate location for the catalog's data file|

# SAO2000

How to Run the sao2000.py File
===============================

1. Edit the catalogs.conf file under [SAO2000] to include the server host, port, user and password you wish to have the database created on.
2. Navigate to the command line and run the sao2000.py file by the 'python sao2000.py' command
3. The sao.dat file must be either in the same location as the sao2000.py file or a path to the sao.dat file must be specified

*The default file will create an SAO2000_dev database with all rows of the SAO2000 catalog inserted into the sao1950 and sao2000 files

Additional SAO Commands
===============================

|Command|Description|Default|
|:-----:|:----------|:------|
|python sao2000.py -r |specifies the number of rows to be inserted from the sao2000 catalog| All Rows|

* to run sao ingestion use python sao2000.py -d SAO -f *your local path to the sao.dat file*

# UCAC4

Additional Package Requirements
============

	struct 
	random 

How to Run the ucac4.py File
===============================

1. Edit the catalogs.conf file under [UCAC4] to include the server host, port, user and password you wish to have the database created on.
2. Navigate to the command line and run the ucac4.py file by the 'python ucac4.py' command
3. Ensure that the ucac4 catalog is in the same folder as the ucac4.py file or that an appropriate file path is specified to reach the u4b folder and that the ucac4 zone files are in the u4b folder

Additional UCAC Commands
===============================
|Command|Description|Default|
|:-----:|:----------|:------|
|python ucac4.py -n|specifies the number of zone files that should be inserted. For full insertion leave blank|900|
|python ucac4.py -r|specifies whether the files should be randomly or uniformly chosen for insertion. If r==True then files will be randomly chosen up to the specified number of files|False|

* to run ucac ingestion use python ucac4.py -d UCAC -f *your local path to the 900 UCAC zone files* 



# GSC240

Additional Package Requirements
============

	random  
	csv

How to Run the gsc240.py File
===============================

1. Edit the catalogs.conf file under [GSC240] to include the server host, port, user and password you wish to have the database created on.
2. Navigate to the command line and run the gsc240.py file by the 'python gsc240.py' command
3. Ensure that the gsc240 catalog is in the same folder as the gsc240.py file or that an appropriate file path is specified to reach the csv folder

Additional GSC Commands
===============================

| Command                  | Description                                                                         | Default                  |
| :-----------------------:| :---------------------------------------------------------------------------------- | :----------------------  |
| python gsc240.py -n      | Number of Dec files to insert into the database                                  | 180                         |
| python gsc240.py -r      | Randomly select files to insert?                                                 | False                       |
| python gsc240.py -m      | Manually insert a file or set of files                                           | None                        |
| python gsc240.py -k      | Drop current tables and restart DB ingestion                                     | False                       |
| python gsc240.py -mr     | Manually Insert a range of files                                                 | None                        |
| python gsc240.py -v      | Print the number of duplicate & new stars to the command line                    | False                       |


* to run gsc240 ingestion use python gsc240.py -d GSC -f *your local path to the 180 gsc folders* -k True -v True
	* -k True will clear the database, do NOT use this in the main GSC catalog. Only use it for clearing test databases in dev or when you first run the gsc ingestion in a database
	* -v True will print any errors that the file throws when running db ingestion. It will not print duplicate star errors, which are the most common. The SQL DB will throw this error if you try to insert a file that has already been inserted



# GAIA

Additional Requirements
============

	random  
	csv
	gzip *if reading from gaia zipped files

How to run the gaia.py or gaia_unzipped.py files
===============================

1. Edit the catalogs.conf file under [GAIA] to include the server host, port, user and password you wish to have the database created on.
2. Navigate to the command line and run the gaia.py file by the 'python gaia.py' command
3. Ensure that the appropriate file path is specified to reach the gaia data folder

Additional GAIA Commands
===============================

| Command                   | Description                                                                          | Default                        |
| :-----------------------: | :----------------------------------------------------------------------------------  | :----------------------        |
| python gaia.py -n         | Number of files to randomly insert into the database                                 | 307                            |
| python gaia.py -r         | Randomly select folders to insert?                                                   | False                          |
| python gaia.py -mr        | Start insertion from a folder and end at a folder (default: aa,lu)                   | "aa,lu"                        |
| python gaia.py -k         | Drop current tables and restart DB ingestion?                                        | False                          |
| python gaia.py -v         | Print errors & star numbers                                                          | False                          |


* to run gaia ingestion use python gaia.py -d GAIA -f *your local path to the gaia folders* -k True -v True
	* -k True will clear the database, do NOT use this after the first run of gaia; only use it for clearing test databases in dev or when you first run the gaia ingestion in a database
	* -v True will print any errors that the file throws when running db ingestion. It will not print duplicate star errors, which are the most common. The SQL DB will throw this error if you try to insert a file that has already been inserted



# 2MASS
Additional Requirements
============

	random 
	csv

How to Run the 2mass.py File
===============================

1. Edit the catalogs.conf file under [2MASS] to include the server host, port, user and password you wish to have the database created on.
2. Navigate to the command line and run the 2mass.py file by the 'python 2mass.py' command
3. Ensure that the appropriate file path is specified to reach the 2massCat folder

Additional GAIA Commands
===============================

| Command                   | Description                                                                          | Default                        |
| :-----------------------: | :----------------------------------------------------------------------------------  | :----------------------        |
| python 2mass.py -n        | Number of Dec files to insert into the database                                      | 180                            |
| python 2mass.py -r        | Randomly select files to insert?                                                     | False                          |
| python 2mass.py -m        | Manually insert a file or set of files                                               | None                           |
| python 2mass.py -k        | Drop current tables and restart DB ingestion?                                        | False                          |
| python 2mass.py -mr       | Manually insert a set of files (1,180--insert Dec files 0-179)                       | ""                             |
| python 2mass.py -v        | Print the number of duplicate/new stars to the command line                          | False                          |


* to run 2mass ingestion use python 2mass.py -d 2MASS -f *your local path to the 2mass data folder* -k True -v True
	* -k True will clear the database, do NOT use this after the first run of 2mass; only use it for clearing test databases in dev or when you first run the ingestion in a database
	* -v True will print any errors that the file throws when running db ingestion. It will not print duplicate star errors, which are the most common. The SQL DB will throw this error if you try to insert a file that has already been inserted



# HIP
Additional Requirements
==========================

	csv

How to Run the hip.py File
===============================

1. Edit the catalogs.conf file under [HIP] to include the server host, port, user and password you wish to have the database created on.
2. Navigate to the command line and run the hip.py file by the 'python hip.py' command
3. Ensure that the appropriate file path is specified to reach the 2massCat folder

Additional HIP Commands
===============================

| Command               | Description                                                      | Default                  |
| :---------------------:| :--------------------------------------------------------------- | :------------------------ |
| python hip.py -k       | Drop current tables and restart DB ingestion?                    | False                    |
| python hip.py -v       | Print number of duplicate/new stars to the command line          | False                    |


* to run hip ingestion use python hip.py -d HIP -f *your local path to the 2mass data folder* -k True -v True
	* -k True will clear the database, do NOT use this after the first run of hip; only use it for clearing test databases in dev or when you first run the ingestion in a database
	* -v True will print any errors that the file throws when running db ingestion. It will not print duplicate star errors, which are the most common. The SQL DB will throw this error if you try to insert a file that has already been inserted
