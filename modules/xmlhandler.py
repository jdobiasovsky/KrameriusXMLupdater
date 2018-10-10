import os
import xml.dom.minidom
from modules import termcolor
from modules.utils import yes_no
import shutil


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


def xml_remove_empty_lines(filename):
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)


def xmledit(fcrepo_export, uuid, sysno, checkforexistingsysno):
    # opens file, parses documents and makes necessary edits
    print("Editing " + fcrepo_export + "uuid_" + uuid + ".xml")
    print("Opening file...")
    if os.stat(fcrepo_export + "uuid_" + uuid + ".xml").st_size == 0:
        print("File is empty!")
        status("fail")
        if os.path.exists("./failed") is False:
            os.mkdir("./failed")
        shutil.copy2(fcrepo_export + "uuid_" + uuid + ".xml", "failed/uuid_" + uuid + ".xml")
        print("---------------------------------------------------------------------")
        raise RuntimeError

    with open(fcrepo_export + "uuid_" + uuid + ".xml") as datasource:
        doc = xml.dom.minidom.parse(datasource)

        if checkforexistingsysno == "yes":
            print("System number check...")
            if xmlcheck(lookfortag="mods:recordIdentifier",
                        attribute="source",
                        attrvalue="CZ PrSTK",
                        parseddoc=doc) is True:

                if sysno == returnattrval(lookfortag="mods:recordIdentifier",
                                          attribute="source",
                                          attrvalue="CZ PrSTK",
                                          parseddoc=doc):
                    print("Document has already matching sysno assigned, will not update...")
                    status("skip")
                    documentroot = doc.documentElement
                    with open("./output/uuid_" + uuid + ".xml", "w") as outfile:
                        # writes document as is into output
                        outfile.write(documentroot.toprettyxml())
                        xml_remove_empty_lines("./output/uuid_" + uuid + ".xml")
                    print("---------------------------------------------------------------------")
                    return

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

                # if not skipped, execute below
                recordidentifiers = doc.getElementsByTagName('mods:recordIdentifier')

                for identifier in recordidentifiers:
                    if identifier.getAttribute("source") == "CZ PrSTK":
                        identifier.removeChild(identifier.firstChild)
                        identifiertext = doc.createTextNode(sysno)
                        identifier.appendChild(identifiertext)
                        print("Assigning: ", identifier.firstChild.nodeValue)

                        documentroot = doc.documentElement
                        with open("./output/uuid_" + uuid + ".xml", "w") as outfile:
                            outfile.write(documentroot.toprettyxml())
                        status("ok")
                        print("---------------------------------------------------------------------")
                    return

        # if the check above doesn't trigger, write system number
        print("Writing system number...")
        try:
            if not doc.getElementsByTagName("mods:recordInfo"):
                    # "if not"  = list is empty
                    # find <mods:mods>, create <mods:recordInfo>, append to the end of child tags
                    modsroot = doc.getElementsByTagName("mods:mods")[0]
                    infonode = doc.createElement("mods:recordInfo")
                    modsroot.appendChild(infonode)

            # same thing as above, without creating <mods:recordInfo>
            infonode = doc.getElementsByTagName('mods:recordInfo')[0]
            recordidentifier = doc.createElement('mods:recordIdentifier')
            recordidentifier.setAttribute("source", "CZ PrSTK")
            infonode.appendChild(recordidentifier)
            identifiertext = doc.createTextNode(sysno)
            recordidentifier.appendChild(identifiertext)

        except IndexError:
            print("Unable to find <mods:mods> element, please verify the file.")
            status("fail")
            if os.path.exists("./failed") is False:
                    os.mkdir("./failed")
            shutil.copy2(fcrepo_export + "uuid_" + uuid + ".xml", "failed/uuid_" + uuid + ".xml")
            print("---------------------------------------------------------------------")
            raise RuntimeError

        documentroot = doc.documentElement
        with open("./output/uuid_" + uuid + ".xml", "w") as outfile:
            outfile.write(documentroot.toprettyxml())
            xml_remove_empty_lines("./output/uuid_" + uuid + ".xml")
        status("ok")
        print("---------------------------------------------------------------------")
