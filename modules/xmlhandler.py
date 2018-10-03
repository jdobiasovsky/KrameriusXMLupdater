import os
from xml import dom
import xml.dom.minidom


def loadfilelist(fcrepo_export):
    # loads files present in fcrepo directory
    # probably would be better to directly download and push them in the future
    filelist = list()
    for file in os.listdir(fcrepo_export):
        filelist.append(fcrepo_export + file)

    return filelist


def loaduuidlist(fcrepo_export):
    # based on file names loads list of uuid's for matching with catalog data
    uuidlist = list()
    for file in os.listdir(fcrepo_export):
        uuidlist.append(file[5:-4])

    return uuidlist


def generateexportlist(catalogdict, fcrepo_export):
    # if fcrepo_export dir in ./input is empty, generate list of files that need to be exported before continuing
    keylist = list(catalogdict.keys())

    if not os.listdir(path=fcrepo_export):
        print("Generating list for fedora export...")
        with open("./export_list.txt", 'w') as f:
            for key in keylist:
                f.write("uuid:" + key + "\n")
        return True

    else:
        print("Folder not empty, skipping export list generation...")
        return False


def xmlcheck(fcrepo_export, lookfortag, lookforattribute, lookforattrvalue, uuid):
    # reads xml and checks whether given metadata element is present

    datasource = open(fcrepo_export + "uuid_" + uuid + ".xml", "r")

    doc = xml.dom.minidom.parse(datasource)
    # print("Scanning: ", doc.firstChild.tagName, doc.firstChild.getAttribute("PID"))

    for elem in doc.getElementsByTagName(lookfortag):
        '''
        Method getElementsByTagName returns a list. The string held between the open and closing
        tags is a child node that is accessed with element method childNodes.
        (tl;dr node value is represented as child of element in DOM)
        '''
        if elem.getAttribute(lookforattribute) == lookforattrvalue:
            return True

    return False


def xmledit(fcrepo_export, uuid, sysno):
    # TODO open file based on inputdir and uuid
    datasource = open(fcrepo_export + "uuid_" + uuid + ".xml", "r")
    doc = xml.dom.minidom.parse(datasource)
    # TODO check if the tag already exists, if so check value and overwrite / don't
    if xmlcheck(fcrepo_export=fcrepo_export,
                        lookfortag="mods:recordIdentifier",
                        lookforattribute="source",
                        lookforattrvalue="CZ PrSTK",
                        uuid=uuid) is True:
        print("System number already present, review document or skip?")
        '''
        Method getElementsByTagName returns a list. The string held between the open and closing
        tags is a child node that is accessed with element method childNodes.
        (tl;dr node value is represented as child of element in DOM)
        '''

    # TODO find proper position for new tag to be appended
    # TODO write into file, save and copy to output






