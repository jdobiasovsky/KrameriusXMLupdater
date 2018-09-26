import os
from modules.utils import yes_no
from bs4 import BeautifulSoup


def verifyconfig(config):
    print("Verifying configuration...")
    for key, val in config.items():
        if val is None:
            print("Required configuration value: " + key + " is not defined! Check your config file.")
            print("Unable to fully verify configuration file, exiting...")
            exit()

    if config["makebackup"] == "yes":
        dirlist = (os.path.isdir(config["fcrepo_export"]),
                   os.path.isdir(config["backupdir"]),
                   os.path.isdir(config["outputdir"]))

        if all(dirlist) is False:
            print("It seems that this is the first time you're running the program.\n"
                  "Checking for necessary directories before validating input files")

            if os.path.isdir(config["fcrepo_export"]) is False:
                if yes_no("Required fcrepo_export directory is missing. "
                                "Create folder (y) or stop (n)?:\n") is True:
                    os.mkdir(config["fcrepo_export"])
                else:
                    print("Exiting...")
                    exit()

            if os.path.isdir(config["outputdir"]) is False:
                if yes_no("Required output directory is missing. "
                                "Create folder (y) or stop (n)?:\n") is True:
                    os.mkdir(config["outputdir"])
                else:
                    print("Exiting...")
                    exit()

            if os.path.isdir(config["backupdir"]) is False:
                if yes_no("Required backup directory is missing. "
                                "Create folder (y) or stop (n)?:\n") is True:
                    os.mkdir(config["backupdir"])
                else:
                    print("Exiting...")
                    exit()

    if config["makebackup"] == "no":
        dirlist = (os.path.isdir(config["fcrepo_export"]),
                   os.path.isdir(config["outputdir"]))

        if all(dirlist) is False:
            print("It seems that this is the first time you're running the program.\n"
                  "Checking for necessary directories before validating input files")

            if os.path.isdir(config["fcrepo_export"]) is False:
                if yes_no("Required fcrepo_export directory is missing. Create folder (y) or stop (n)?:\n") is True:
                    os.mkdir(config["fcrepo_export"])
                else:
                    print("Exiting...")
                    exit()

            if os.path.isdir(config["outputdir"]) is False:
                if yes_no("Required output directory is missing. Create folder (y) or stop (n)?:\n") is True:
                    os.mkdir(config["outputdir"])
                else:
                    print("Exiting...")
                    exit()
    direval = True

    if config["makebackup"] == "yes":
        dirlist = (os.path.isdir(config["fcrepo_export"]),
                   os.path.isdir(config["backupdir"]),
                   os.path.isdir(config["outputdir"]))
        if all(dirlist) is False:
            direval = False

    if config["makebackup"] == "no":
        dirlist = (os.path.isdir(config["fcrepo_export"]),
                   os.path.isdir(config["outputdir"]))
        if all(dirlist) is False:
            direval = False
    print("Finished directory check...")

    fileeval = True
    if os.path.exists(config["kramlinks"]) is False:
        print(config["kramlinks"], " not found!")
        fileeval = False

    if os.path.exists(config["errfile"]) is False:
        print(config["errfile"], " not found!")
        fileeval = False
    print("Finished input files check...")

    return direval, fileeval


def loadconfig():
    # reads data from xml and returns them as dictionary for later use
    with open("./config/config.xml") as configfile:
        content = configfile.read()
    config = BeautifulSoup(content, "lxml")
    # reads content from configfile into bs4 format

    variablenames = ["kramlinks", "errfile", "fcrepo_export",
                     "sysnopattern", "uuidpattern",
                     "makebackup", "backupdir", "checksysno",
                     "outputdir"
                     ]

    variablevalues = [config.inputfiles.kramlinks.string,
                      config.inputfiles.errfile.string,
                      config.inputfiles.fcrepo_export.string,
                      config.patternmatch.sysno.string,
                      config.patternmatch.uuid.string,
                      config.safetynets.backup.makebackup.string,
                      config.safetynets.backup.backupdir.string,
                      config.safetynets.checksysno.string,
                      config.output.outputdir.string,
                      # TODO append other config values as they go
                      ]

    loadedconfig = dict(zip(variablenames, variablevalues))
    return loadedconfig

