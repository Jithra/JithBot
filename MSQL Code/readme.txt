Database structure for this code is:

Database Name: db_discord
Table Name: tblAggregateDiscordLogs
SQL Driver: ODBC Driver 13 for SQL Server
Python Module: pymssql

The Username and Password can be set manually, but until I actually code in a config file, this will have to be manually modified in the plugins SQLTransact.py and sqlservlog.py files.
The DB user will also need adequate read/write permissions based on the functions that are used. 

All necessary stored procedures and functions can be found in their respective folders. These need to be run from the Microsoft SQL Database that is being used. I'm working on creating a database image to be used for this project, however for the time being this will all have to be done manually. 