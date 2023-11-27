
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
