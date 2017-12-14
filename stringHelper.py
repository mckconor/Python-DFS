def getFileName(string):
	return string.split(".")[0]

def getFileExtension(string):
	return string.split(".")[1]

def getFormattedFileName(string):
	return getFileName(string) + "\u2024" + getFileExtension(string)