from modules import utils, xmlhandler
from modules import termcolor
from modules import configuration


termcolor.cprint("\n=======================Init=======================", 'green')

# load configuration, print it for user and store it for futher use in config{} dictionary
config = configuration.loadconfig()

# verify loaded configuration in variable using configuration.verifyconfig()
if all(configuration.verifyconfig(config)) is False:
    print("Configuration verification failed, exiting...")
    exit()
elif all(configuration.verifyconfig(config)) is True:
    print("Configuration verified...")


termcolor.cprint("\n=======================Check configuration=======================", 'green')
print("Catalog file: ", config["kramlinks"])
print("Error file: ", config["errfile"])
print("Fedora export directory: ", config["fcrepo_export"])
print("Output directory: ", config["outputdir"])
print("System number match pattern: ", config["sysnopattern"])
print("Document ID match pattern: ", config["uuidpattern"])
print("Make backup?: ", config["makebackup"])
if config["makebackup"] == "yes":
    print("Catalog file: ", config["backupdir"])
print("Check for existing system numbers?: ", config["checksysno"])

termcolor.cprint('\nContinue?', 'red', attrs=['blink'])
if utils.yes_no("Yes / No") is False:
    exit()


termcolor.cprint("\n=======================Preparing data=======================", 'green')
print("Reading catalog data and uuid list")
# loads provided data from provided kramlink file
catalog_data = utils.fetchlinkdata(config["kramlinks"], config["sysnopattern"], config["uuidpattern"])


print("Checking input folder for fedora exported files...")
# uses xmlhandler.generateexportlist() function to check if there are data in input. If not, generates list for use
if xmlhandler.generateexportlist(catalogdict=catalog_data, fcrepo_export=config["fcrepo_export"]) is True:
    print("Export list generated, please export the files and put them into fcrepo_export dir before continuing")
    termcolor.cprint('\nPress enter when ready', 'red', attrs=['blink'])
    input()

else:
    print("Proceeding with xml matching...")

# loads list of files from fcrepo_export
uuid_list = xmlhandler.loaduuidlist(fcrepo_export=config["fcrepo_export"])
data_pairs = utils.matchdata(catalog_data, uuid_list)


utils.sysnocheck(sysno_configval=config["checksysno"], uuid_list=uuid_list, fcrepo_export=config["fcrepo_export"])


if config["makebackup"] == "yes":
    print("Backing files into ./backup/")
    utils.backuporiginals(backupdirectory=config["backupdir"], fcrepo_export=config["fcrepo_export"])


termcolor.cprint("\n=======================Editing=======================", 'green')
