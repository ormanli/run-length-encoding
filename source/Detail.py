'''
Created on 06 Mar 2014

@author: Serdar ORMANLI
'''

class Detail(object):
	'''
	classdocs
	'''


	def __init__(self, compressed, hist, width, height, mode, scanning , palette = None):
		'''
		Constructor
		'''
		self.compressed = compressed
		self.hist = hist
		self.height = height
		self.width = width
		self.mode = mode
		self.scanning = scanning
		self.palette = palette
