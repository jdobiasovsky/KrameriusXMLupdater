import os
import xml.dom.minidom
from modules import termcolor
from modules.utils import yes_no

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


def xmlcheck(lookfortag, attribute, attrvalue, parseddoc):
    # checks whether given metadata element is present in provided parseddoc

    # print("Scanning: ", doc.firstChild.tagName, doc.firstChild.getAttribute("PID"))

    for elem in parseddoc.getElementsByTagName(lookfortag):
        # find element with tag name "lookfortag", if there is one, check whether it's value fits "attrvalue".
        # If they both fit the passed parameters, function returns True. In all other cases False
        # Method getElementsByTagName returns a list. Attribute value is represented as attribute's child in DOM

        if elem.getAttribute(attribute) == attrvalue:
            return True

    return False


def returnattrval(lookfortag, attribute, attrvalue, parseddoc):
        for elem in parseddoc.getElementsByTagName(lookfortag):
            if elem.getAttribute(attribute) == attrvalue:
                elemval = elem.firstChild.nodeValue
                return elemval

        return False


def status(code):
    if code == "ok":
        termcolor.cprint("Sucess!", 'green')
    if code == "skip":
        termcolor.cprint("Skipped...", 'yellow')
    if code == "fail":
        termcolor.cprint("Failed!", 'red')


def xmledit(fcrepo_export, uuid, sysno, checkforexistingsysno):
    # opens file, parses documents and makes necessary edits
    print("Editing " + fcrepo_export + "uuid_" + uuid + ".xml")
    datasource = open(fcrepo_export + "uuid_" + uuid + ".xml", "r")
    doc = xml.dom.minidom.parse(datasource)
    documentroot = doc.getElementsByTagName("<mods:modsCollection>")[0]

    if checkforexistingsysno == "yes":
        if xmlcheck(lookfortag="mods:recordIdentifier",
                    attribute="source",
                    attrvalue="CZ PrSTK",
                    parseddoc=doc) is True:

            print("Document " + uuid + " already has sysno assigned...")

            print("Current sysno:             ", returnattrval(lookfortag="mods:recordIdentifier",
                                                               attribute="source",
                                                               attrvalue="CZ PrSTK",
                                                               parseddoc=doc))

            print("Sysno about to be assigned: " + sysno)
            print("\nSkip?")
            if yes_no("Yes / No\n") is True:
                status("skip")
                print("---------------------------------------------------------------------")
                return

    print("Writing system number.")
    recordinfo = doc.getElementsByTagName("<mods:recordInfo>")[0]
    if recordinfo is None:
        root = doc.getElementsByTagName("<mods:mods>")[0]
        infonode = doc.createElement("<mods:recordInfo>")
        root.appendChild(infonode)

    # create new node object and set attributes
    identifiernode = doc.createElement('<mods:recordIdentifier>')
    identifiernode.setAttribute("source", "CZ PrSTK")

    # create new node with text containing sysno
    nodetext = doc.createTextNode(sysno)

    # append child node with text to identifierinfo
    identifiernode.appendChild(nodetext)

    # add newline after new child
    newline = doc.createTextNode('\n')
    identifiernode.insertBefore(newline)

    # create new document in output directory and write contents of xml file into it
    outputdocument = open("./output/uuid_" + uuid + ".xml", "w")
    documentroot.writexml(outputdocument)

    status("ok")
    print("---------------------------------------------------------------------")
