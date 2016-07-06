# PathwayPackage [draft, tbc]

PathwayPackage [PP] is an integration platform for instantaneous processing and analysis of confocal/fluorescent microscopy images software.

TABLE OF CONTENT:
I. Software requirments.
II. Command line usage.
III. PathwayPackage's modules.

I. Software requirments:
Minimal:
- python 3.5.1
- CellProfiler 2.2.0 [http://cellprofiler.org]
Optional (see destribtion below):
- rpy2 python's package 
To use some features (scripts) based on R programming language it is also needed to install rpy2 package and its dependencies (for more information check out tutorials/rpy2_installation.py).

II. Command line usage:
PathwayPackage is run from the command line as follows:
-s <settingspath>	// Specifies the path to file with input configuration settings.
  The input file should contain one or more sequences. Fastq format is required.

III. PathwayPackage's modules:
1. xml_parser
2. csv_managment
3. file_managment
4. logs_configuration
5. cellprofiler
6. map_plate
7. task
