import os
from xml import dom
import xml.dom.minidom


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


def generateexportlist(catalogdict):
    # if fcrepo_export dir in ./input is empty, generate list of files that need to be exported before continuing
    keylist = list(catalogdict.keys())

    if not os.listdir(path='./input/fcrepo_export'):
        print("Generating list for fedora export...")
        with open("./output/export_list.txt", 'w') as f:
            for key in keylist:
                f.write("uuid:" + key + "\n")
        return True

    else:
        print("Folder not empty, skipping export list generation...")
        return False


def xmlcheck(lookfortag, uuid):
    # reads xml and checks whether given metadata element is present

    datasource = open("./input/fcrepo_export/uuid_" + uuid + ".xml", "r")

    doc = xml.dom.minidom.parse(datasource)
    print("Scanning: ", doc.firstChild.tagName, doc.firstChild.getAttribute("PID"))

    for elem in doc.getElementsByTagName(lookfortag):
        '''
        Method getElementsByTagName returns a list. The string held between the open and closing
        tags is a child node that is accessed with element method childNodes.
        (tl;dr node value is represented as child of element in DOM)
        '''
        print(elem.firstChild.nodeValue)




