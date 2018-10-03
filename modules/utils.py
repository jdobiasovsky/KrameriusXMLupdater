import re
import os
import shutil


def yes_no(prompt):
    yes = ['yes', 'y', 'ye', '']
    no = ['no', 'n']

    while True:
        # will loop forever until value is returned
        choice = input(prompt).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'\n")


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
            with open("./output/error_log.txt", "w+") as errlist:
                if sysno is None:
                    errlist.write("sysno not found for: " + uuid.group(0))
                if uuid is None:
                    errlist.write("uuid not found for: " + sysno.group(0))
                else:
                    errlist.write("Unexpected error on line: " + line)

    if allmatchescorrect is False:
        print("Some lines in catalog data weren't processed succesfully, log generated...")

    return linkdata


def matchdata(catalogdata, uuidlist):
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
            print("Failed to match: " + uuid.group(0) + "with systemnumber")
            with open("./error_log.txt", "w+") as errlist:
                errlist.write("Failed to match: " + uuid.group(0))
            continue

    return generatedpairs


def backuporiginals(backupdirectory, fcrepo_export):
    for file in os.listdir(fcrepo_export):
        try:
            shutil.copy2(fcrepo_export + file, backupdirectory + file)
        except FileNotFoundError as err:
            print("File " + file + " not found! Unable to make backup, exiting for safety reasons")
            print(err)
