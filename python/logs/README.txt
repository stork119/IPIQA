LOGGING MODULE README



I. Applying logging facility to new PathwayPackage's module.



1. Add 'import logging' on the beginning of a file.

2. Assign getting logger option to variable logger (logger = logging.getLogger(__name__)).

3. Add logging messages by 'logger.logging_level("Message")' formula.
  
Possible logging levels (numeric value):
  
	- notset (0)
  
	- debug (10)
  
	- info (20)
  
	- warning (30)
  
	- error (40)
  
	- critical (50).
  


II. Basics configure of logging.



In PathwayPackage logging module is configured by logging config file (logging.conf).

If you won't specify the logger for your Pathway's module, program will follow the root_logger settings.

The basics classess defined by module are:
  
- Loggers 
  
- Handlers
  
- Filters
  
- Formatters.
For more information check out python logging module documentation.

III. Suplement.

Some phrases in config file may worry programmers, because of their less typical form. For example:
"logging.conf : 
[formatter_primaryFormatter]
format=%(asctime)s - %(name) - 8s - %(levelname) - 8s - %(message)s
datefmt=" 
This phrase is correct for this type of file, for more information check out logging module documentation.