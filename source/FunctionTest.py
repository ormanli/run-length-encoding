'''
Created on 11 Mar 2014

@author: Serdar ORMANLI
'''
import unittest
from PIL import Image
import os
from Detail import Detail
import glob
from FunctionTimer import timewith
import pprint
import math
import RLE

class Test(unittest.TestCase):

	results = {}
	scanningtypes = ['C', 'CR', 'R', 'RR', 'ZZ']

	def addNameToDictionary(self, depth, scanning, image, result, value):
		if depth not in self.results:
			self.results[depth] = {}
		if scanning not in self.results[depth]:
			self.results[depth][scanning] = {}
		if image not in self.results[depth][scanning]:
			self.results[depth][scanning][image] = {}
		if result not in self.results[depth][scanning][image]:
			self.results[depth][scanning][image][result] = {}
		self.results[depth][scanning][image][result] = value

	def testBW(self):
		imgdirname = "../images/black&white"

		filelist = glob.glob(imgdirname + "/*.bmp")
		for file in filelist:
			img1 = Image.open(file)

			orgimg = list(img1.getdata(0))

			for scanningmethod in self.scanningtypes:
				with timewith('Black&White Number ' + scanningmethod) as timer:
					encodedimg = RLE.encodeImage(orgimg, img1.size[0], img1.size[1], img1.mode, scanningmethod)
					self.addNameToDictionary('BW', scanningmethod, file, 'Encode', timer.checkpoint('Encode Image Mode ' + scanningmethod + " " + file))

					tempimg = Detail(encodedimg, 1, img1.size[0], img1.size[1], img1.mode, scanningmethod)
					compsize, filepath = RLE.saveCompressedToFile(tempimg, file)
					statinfo = os.stat(file)
					compimg = RLE.openFileToCompressed(file + ".comp")
					self.addNameToDictionary('BW', scanningmethod, file, 'Compression Ratio', math.ceil((compsize / statinfo.st_size) * 1000) / 1000)
					timer.checkpoint('Compression Ratio ' + scanningmethod + " " + file)

					decodedimg = RLE.decodeImage(compimg.compressed, compimg.width, compimg.height, compimg.mode, scanningmethod)
					self.addNameToDictionary('BW', scanningmethod, file, 'Decode', timer.checkpoint('Decode Image Mode ' + scanningmethod + " " + file))
					self.addNameToDictionary('BW', scanningmethod, file, 'Equality', str(orgimg == decodedimg))

	def testGRY4BIT(self):
		imgdirname = "../images/4bit"

		filelist = glob.glob(imgdirname + "/*.bmp")
		for file in filelist:
			img1 = Image.open(file)

			orgimg = list(img1.getdata(0))
			print(file)
			for scanningmethod in self.scanningtypes:
				with timewith('4bit Number ' + scanningmethod) as timer:
					encodedimg = RLE.encodeImage(orgimg, img1.size[0], img1.size[1], img1.mode, scanningmethod)
					self.addNameToDictionary('4bit', scanningmethod, file, 'Encode', timer.checkpoint('Encode Image Mode ' + scanningmethod + " " + file))

					tempimg = Detail(encodedimg, 1, img1.size[0], img1.size[1], img1.mode, scanningmethod, img1.getpalette())
					compsize, filepath = RLE.saveCompressedToFile(tempimg, file)
					statinfo = os.stat(file)
					compimg = RLE.openFileToCompressed(file + ".comp")
					self.addNameToDictionary('4bit', scanningmethod, file, 'Compression Ratio', math.ceil((compsize / statinfo.st_size) * 1000) / 1000)
					timer.checkpoint('Compression Ratio ' + scanningmethod + " " + file)

					decodedimg = RLE.decodeImage(compimg.compressed, compimg.width, compimg.height, compimg.mode, scanningmethod)
					self.addNameToDictionary('4bit', scanningmethod, file, 'Decode', timer.checkpoint('Decode Image Mode ' + scanningmethod + " " + file))
					self.addNameToDictionary('4bit', scanningmethod, file, 'Equality', str(orgimg == decodedimg))

	def testGRY8BIT(self):
		imgdirname = "../images/8bit"

		filelist = glob.glob(imgdirname + "/*.bmp")
		for file in filelist:
			img1 = Image.open(file)

			orgimg = list(img1.getdata(0))

			for scanningmethod in self.scanningtypes:
				with timewith('8bit Number ' + scanningmethod) as timer:
					encodedimg = RLE.encodeImage(orgimg, img1.size[0], img1.size[1], img1.mode, scanningmethod)
					self.addNameToDictionary('8bit', scanningmethod, file, 'Encode', timer.checkpoint('Encode Image Mode ' + scanningmethod + " " + file))

					tempimg = Detail(encodedimg, 1, img1.size[0], img1.size[1], img1.mode, scanningmethod)
					compsize, filepath = RLE.saveCompressedToFile(tempimg, file)
					statinfo = os.stat(file)
					compimg = RLE.openFileToCompressed(file + ".comp")
					self.addNameToDictionary('8bit', scanningmethod, file, 'Compression Ratio', math.ceil((compsize / statinfo.st_size) * 1000) / 1000)
					timer.checkpoint('Compression Ratio ' + scanningmethod + " " + file)

					decodedimg = RLE.decodeImage(compimg.compressed, compimg.width, compimg.height, compimg.mode, scanningmethod)
					self.addNameToDictionary('8bit', scanningmethod, file, 'Decode', timer.checkpoint('Decode Image Mode ' + scanningmethod + " " + file))
					self.addNameToDictionary('8bit', scanningmethod, file, 'Equality', str(orgimg == decodedimg))

	def testResult(self):
		pprint.pprint(self.results)

if __name__ == "__main__":
# 	import sys;sys.argv = ['', 'Test.testEncode']
	unittest.main()
