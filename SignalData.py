class Signal(object):
	"""docstring for Signal"""
	def __init__(self, filename=None,filetype=None,filedata=None,Fsample=None,Fcentre=None):
		
		self.filename = filename
		self.filetype = filetype
		self.filedata = filedata
		self.Fsample = Fsample
		self.Fcentre = Fcentre

	def setvalues(self,filename,filetype,Fsample,Fcentre,filedata=None):

		self.filename = filename
		self.filetype = filetype
		self.filedata = filedata
		self.Fsample = Fsample
		self.Fcentre = Fcentre

	def setdatavalue(self,filedata):

		self.filedata = filedata

	def getvalues(self):

		return(self.filename,self.filetype,self.filedata,self.Fsample,self.Fcentre)