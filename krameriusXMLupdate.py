from modules import utils, xmlhandler
from modules import termcolor

termcolor.cprint("\n=======================Configuration=======================", 'green')
config = utils.loadconfig()
# TODO call verifyconfig() on config once it's finished
for key, val in config.items():
    print(key, val)

termcolor.cprint('\nPress enter when ready', 'red', attrs=['blink'])
input()


termcolor.cprint("\n=======================Preparing data=======================", 'green')
print("Reading catalog data and uuid list")
catalog_data = utils.fetchlinkdata(config["kramlinks"], config["sysnopattern"], config["uuidpattern"])


print("Checking input folder for fedora exported files...")
if xmlhandler.generateexportlist(catalogdict=catalog_data) is True:
    print("Export list generated, please export the files and put them into fcrepo_export dir before continuing")
    termcolor.cprint('\nPress enter when ready', 'red', attrs=['blink'])
    input()

else:
    print("Proceeding with xml matching...")

uuid_list = xmlhandler.loaduuidlist()

termcolor.cprint("\n=======================Editing=======================", 'green')
data_pairs = utils.matchdata(catalog_data, uuid_list)
for doc_id in uuid_list:
    try:
        xmlhandler.xmlcheck(lookfortag="title", uuid=doc_id)
        # TODO finish this properly!

    except FileNotFoundError:
        with open("./output/error_log.txt", "w+") as errorlog:
            errorlog.write("File: uuid:" + doc_id + " was not found...")
        continue
