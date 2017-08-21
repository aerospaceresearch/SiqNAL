"""
    **Author :** *Jay Krishna*

    This module defines class to pass meta data about the file source 
    and signal in structured manner.
    
    Note
    -----------------------
    Three file extensions are supported in this project, namely

    #. .dat
    #. .wav
    
"""


class Signal(object):

    def __init__(self, filename=None, filetype=None, filedata=None, Fsample=None, Fcentre=None):
        """
            This function initializes the class object used to pass meta data across functions and classes 
            about the file source and signal.

            Parameters
            ---------------------------------
                filename : string
                    Absolute path to the file from which data will be read, optional.
                filetype : string
                    Extension of the file, optional.
                filedata : file object
                    Memory mapped file object of the file, optional.
                Fsample : float
                    Sampling frequency of the signal, optional.
                Fcentre : float
                    Centre frequency of the signal, optional.
        """

        self.filename = filename
        self.filetype = filetype
        self.filedata = filedata
        self.Fsample = Fsample
        self.Fcentre = Fcentre

    def setvalues(self, filename, filetype, Fsample, Fcentre, filedata=None):
        """
            This is a setter function to initialize the member variables of the class object except for filedata variable.

            Parameters
            ---------------------------------
                filename : string
                    Absolute path to the file from which data will be read.
                filetype : string
                    Extension of the file.
                Fsample : float
                    Sampling frequency of the signal.
                Fcentre : float
                    Centre frequency of the signal.
                filedata : file object
                    Memory mapped file object of the file, optional.
        """

        self.filename = filename
        self.filetype = filetype
        self.filedata = filedata
        self.Fsample = Fsample
        self.Fcentre = Fcentre

    def setdatavalue(self, filedata):
        """
            This is a setter function to initialize the filedata variable of the class object.

            Parameters
            ---------------------------------
                filedata : file object
                    Memory mapped file object of the file.
        """

        self.filedata = filedata

    def getvalues(self):
        """
            This is a getter function to retrieve member variables of the class object.

            Returns
            ---------------------------------
                values : tuple
                    Tuple containing all the member variables of class SignalData.
        """

        values = (self.filename, self.filetype,
                  self.filedata, self.Fsample, self.Fcentre)
        return values
