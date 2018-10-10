# KrameriusXMLupdater
Updates fedora repository foxml datastreams with National Library of Technology sysno identifier based on export from library catalogue containing links and said system numbers.

Work in progress / for testing purposes only, don't use on production systems yet

Current functionality:
1) read input files and generate a dictionary of uuid:sysno pairs
2) load foxml document, verify whether there is a required element present
3) append required xml element, format and save
4) create batch ready for fedora repository import


Requirements: 
1) Python 3.5 
2) Python beautifulSoup module (use "pip install beautifulsoup4" if needed)

External libraries used:
1) termcolor 
https://pypi.org/project/termcolor/
