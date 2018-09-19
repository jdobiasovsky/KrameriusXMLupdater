from modules import utils, xmlhandler

config = utils.loadconfig()
# TODO call verifyconfig() on config once it's finished


catalog_data = utils.fetchlinkdata(config["kramlinks"], config["sysnopattern"], config["uuidpattern"])
uuid_list = xmlhandler.loaduuidlist()

# TODO hide code below into specific function for processing xml files
data_pairs = utils.matchdata(catalog_data, uuid_list)
for uuid in data_pairs:
    print("Matched file: " + uuid + " with sysno: " + data_pairs[uuid])
