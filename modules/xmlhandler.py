import os
from xml import dom

def loadfilelist():
    # loads files present in fcrepo directory
    # probably would be better to directly download and push them in the future
    filelist = list()
    for file in os.listdir("./input/fcrepo_export"):
        filelist.append("./input/fcrepo_export/" + file)

    return filelist

def loaduuidlist():
    # based on file names loads list of uuid's for matching with catalog data
    uuidlist = list()
    for file in os.listdir("./input/fcrepo_export"):
        uuidlist.append(file[5:-4])

    return uuidlist

# TODO xml read, compare, write