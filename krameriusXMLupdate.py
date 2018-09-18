from bs4 import BeautifulSoup


def loadconfig():
    # reads data from xml and returns them as dictionary for later use
    with open("./config/config.xml") as configfile:
        content = configfile.read()
    config = BeautifulSoup(content, "lxml")
    # reads content from configfile into bs4 format

    variablenames = ['kramlinks', 'errfile']
    variablevalues = [config.inputfiles.kramlinks.string,
                      config.inputfiles.errfile.string
                      # TODO append other config values as they go
                      ]
    loadedconfig = dict(zip(variablenames, variablevalues))
    return loadedconfig


def verifyconfig():
    config = loadconfig()
    try:
        if 'errfile' in config is None:
            raise ValueError('Errfile not defined in config!')
        if 'kramlinks' in config is None:
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
