LOGGING MODULE README

TABLE OF CONTENT:
I. Applying logging facility to new PathwayPackage's module.
II. Basics configure of logging.
III. Suplement.


I. Applying logging facility to new PathwayPackage's module.

1. Add 'import logging' on the beginning of a file.

2. Assign getting logger option to variable logger: 

  logger = logging.getLogger(__name__).

3. Add logging messages by formula:

  logger.logging_level("Message").
  
Possible logging levels (numeric value):
  - notset (0)
  - debug (10)
  - info (20)
  - warning (30)
  - error (40)
  - critical (50).
  

II. Basics configure of logging.

In PathwayPackage logs are setting up by logs_configuration module. The output file name (year_month_day_hour_minutes_seconds) and its path is determined by the lines:

    log_filename =  log_output_path + ((strftime("%Y_%m_%d_")  + "_" + strftime("%H_%M")) ) + ".log" # setup log filename
    logging.config.fileConfig('logging.conf', defaults={'logfilename': log_filename}, disable_existing_loggers=False).
    
The main configurations of logs are collected in logging config file (logging.conf).
If you won't specify the logger for your Pathway's module, program will follow the root_logger settings.

The basics classess defined by module are:
  - Loggers 
  - Handlers
  - Filters
  - Formatters.
For more information check out python logging module documentation.

III. Suplement.

Some phrases in config file may worry programmers, because of their less typical form. For example:

  logging.conf : 
  [formatter_primaryFormatter]
  format=%(asctime)s - %(name) - 8s - %(levelname) - 8s - %(message)s
  datefmt=" 

This phrase is correct for this type of file, for more information check out logging module documentation.