from bs4 import BeautifulSoup
import re


def loadconfig():
    # reads data from xml and returns them as dictionary for later use
    with open("./config/config.xml") as configfile:
        content = configfile.read()
    config = BeautifulSoup(content, "lxml")
    # reads content from configfile into bs4 format

    variablenames = ['kramlinks', 'errfile', "sysnopattern", "uuidpattern"]
    variablevalues = [config.inputfiles.kramlinks.string,
                      config.inputfiles.errfile.string,
                      config.patternmatch.sysno.string,
                      config.patternmatch.uuid.string
                      # TODO append other config values as they go
                      ]
    loadedconfig = dict(zip(variablenames, variablevalues))
    return loadedconfig


def verifyconfig(target):
    try:
        if 'errfile' in target is None:
            raise ValueError('Errfile not defined in config!')
        if 'kramlinks' in target is None:
            raise ValueError('Kramlink not defined in config!')

    except ValueError:
        print("Unable to continue... exiting")
        exit()

    # TODO finish verifyconfig()
    """
    try:
        my_abs_path = my_file.resolve()
    except FileNotFoundError:
    # doesn't exist
    else:
    # exists
    """


def fetchlinkdata(kramlinkfile, sysnopattern, uuidpattern):
    # compile patterns provided in config
    sysnoregex = re.compile(sysnopattern)
    uuidregex = re.compile(uuidpattern)

    with open(kramlinkfile, 'r') as f:
        read_data = f.readlines()

    linkdata = dict()
    allmatchescorrect = True

    for line in read_data:
        # for each line from provided file extracts sysno and uuid, builds pairs and returns linkdata list
        uuid = re.search(uuidregex, line)
        sysno = re.search(sysnoregex, line)

        if uuid and sysno is not None:
            linkdata.update({uuid.group(0): sysno.group(0)})

        else:
            # if either sysno or uuid is not matched with regex, generates message into output error file
            allmatchescorrect = False
            with open("./output/errlist.txt", "w+") as errlist:
                if sysno is None:
                    errlist.write("sysno not found for: " + uuid.group(0))
                if uuid is None:
                    errlist.write("uuid not found for: " + sysno.group(0))
                else:
                    errlist.write("Error on line: " + line)

    if allmatchescorrect is False:
        print("Some lines weren't processed succesfully, log generated...")

    return linkdata


def matchdata(catalogdata,uuidlist):
    generatedpairs = dict()

    for uuid in uuidlist:
        if uuid in catalogdata:
            '''
            if uuid from uuid list matches key in catalogdata dictionary,
            add new entry with uuid + matched sysno value from catalogdata
            '''
            assignedsysno = catalogdata[uuid]
            generatedpairs.update({uuid: assignedsysno})

        else:
            # if no match is found, raise exception
            print("This is wrong, fix me...")
            # TODO raise error and move file to update_failed

    return generatedpairs

"""
def processXML():



def zipdocs():
"""