import sys
import pickle
import os

def encodeImage(imagePixels, width, height, imgType, scanning = "C"):
	convertedImagePixels = _convertEncodeScanning(list(imagePixels), width, height, scanning)
	if imgType == '1':
		return _encodeImageBW(convertedImagePixels, scanning, width, height)
	elif imgType == 'P':
		return _encodeImage4bit(convertedImagePixels, scanning, width, height)
	else:
		return _encodeImage8bit(convertedImagePixels, scanning, width, height)

def _encodeImage8bit(imagePixels, scanning, width, height):
	encodedImage = bytearray()

	count = 0

	prev = imagePixels[0]
	tempmap = ""

	for pixel in imagePixels:
		if count >= 255:
			encodedImage.append(255)
			encodedImage.append(prev)
			tempmap += "1"
			tempmap += "0"
			count = 0
			prev = pixel

		if pixel == prev:
			count += 1
		else:
			if count > 1:
				encodedImage.append(count)
				tempmap += "1"
			encodedImage.append(prev)
			tempmap += "0"
			count = 1
			prev = pixel

	if count > 1:
		encodedImage.append(count)
		tempmap += "1"

	encodedImage.append(prev)
	tempmap += "0"

	encodedImage.extend([0] * _remaining(len(encodedImage)))
	tempmap += "1"*_remaining(len(tempmap))

	encodedImage = _set8bitMap(tempmap, encodedImage)

	return encodedImage

def decodeImage(encodedImage, width, height, imgType, scanning = "C"):
	newEncodedImage = []
	if imgType == '1':
		newEncodedImage = _decodeImageBW(list(encodedImage), width, height, scanning)
	elif imgType == 'P':
		newEncodedImage = _decodeImage4bit(list(encodedImage), width, height, scanning)
	else:
		newEncodedImage = _decodeImage8bit(list(encodedImage), width, height, scanning)

	return _convertDecodeScanning(newEncodedImage, width, height, scanning)

def _decodeImage8bit(encodedImage, width, height, scanning):
	decodedImage = []

	imgMap, encImg = _get8bitMap(encodedImage)

	for index, i in enumerate(imgMap):
		if i == '1' and encImg[index] == 0:
			break

		if i == '1':
			decodedImage.extend([encImg[index + 1]] * encImg[index])
		elif imgMap[index - 1] != '1' or index == 0:
			decodedImage.append(encImg[index])

	return decodedImage

def soSizeOf(soObj):

	T = type(soObj)

	if T is list:
		return sys.getsizeof([]) + sum(map(soSizeOf, soObj))
	elif T is tuple:
		return sys.getsizeof(()) + sum(map(soSizeOf, soObj))
	else:
		return sys.getsizeof(soObj)

def _encodeImageBW(imagePixels, scanning, width, height):
	encodedImage = bytearray()

	count = 0

	prev = 255

	for pixel in imagePixels:
		if count >= 255:
			encodedImage.append(255)
			encodedImage.append(0)
			count = 0

		if pixel == prev:
			count += 1
		else:
			encodedImage.append(count)
			count = 1
			prev = pixel

	encodedImage.append(count)

	return encodedImage

def _decodeImageBW(encodedImage, width, height, scanning):
	decodedImage = []

	for index, count in enumerate(encodedImage):
		pixel = 0
		if index % 2 == 0:
			pixel = 255
		decodedImage += [pixel] * count

	return decodedImage

def _get8bitMap(encodedImage):
	imgMap = ""
	newEncodedImage = list(encodedImage)

	I = range(0, len(newEncodedImage), 9)

	for i in I:
		imgMap += '{0:08b}'.format(newEncodedImage[i])

	for i in sorted(list(I), reverse = True):
		del newEncodedImage[i]

	return (imgMap, newEncodedImage)

def _set8bitMap(imgMap, encodedImage):
	newImgMap = _divideByRow(imgMap, 8)
	tempImg = _divideByRow(list(encodedImage), 8)

	return bytearray(_flattenListOfList(_mergeMap(tempImg, newImgMap)))

_divideByRow = lambda flat, size: [flat[i:i + size] for i in range(0, len(flat), size)]
_divideByColumn = lambda flat, size:[[row[i] for row in flat] for i in range(size)]
_flattenListOfList = lambda flat:[item for sublist in flat for item in sublist]
_singleRowToContinuosRow = lambda flat:[i if index % 2 == 0 else list(reversed(i))  for index, i in enumerate(flat)]
_remaining = lambda x, y = 8: 0 if x % y == 0 else y - (x % y)
_mergeMap = lambda z, x:[[int(x[index], 2)] + i for index, i in enumerate(z)]
_divideZigZag = lambda flat, width, heigth:[ flat[i] for i in _getZigZagIndex(width, heigth)]
_getParts = lambda a, b: _flattenListOfList([[int(a / b)] * (b - 1), [int(a / b) + a % b]])
_getIndex = lambda a, b:[(int(x / a), x % a) for x in list(range(0, a * b))]

def _getZigZagIndex(X, Y):
	zigzagindex = []
	for a in sorted((p % X + int(p / X), (p % X, int(p / X))[(p % X - int(p / X)) % 2], p) for p in range(X * Y)):
		zigzagindex.append(a[2])

	return zigzagindex

def saveCompressedToFile(img, filename):
	compfile = open(filename + ".comp", "wb")
	pickle.dump(img, compfile)
	compath = os.path.abspath(filename + ".comp")
	statinfo = os.stat(filename + ".comp")
	return (statinfo.st_size, compath)

def openFileToCompressed(path):
	compfile = open(path, "rb")
	return pickle.load(compfile)

def _convertEncodeScanning(img, width, height, scanning = "C"):
	if(scanning == "RR"):
		return _flattenListOfList(_singleRowToContinuosRow(_divideByRow(img, width)))
	elif(scanning == "R"):
		return _flattenListOfList(_divideByRow(img, width))
	elif(scanning == "C"):
		return _flattenListOfList(_divideByColumn(_divideByRow(img, width), width))
	elif(scanning == "CR"):
		return _flattenListOfList(_singleRowToContinuosRow(_divideByColumn(_divideByRow(img, width), width)))
	else:
		return [img[i] for i in _getZigZagIndex(width, height)]

def _convertDecodeScanning(img, width, height, scanning = "C"):
	if(scanning == "ZZ"):
		lst = [0] * width * height

		newindex = _getZigZagIndex(width, height)

		for index in range(0, width * height):
			lst[newindex[index]] = img[index]

		return lst
	elif(scanning == "CR"):
		return _flattenListOfList(_divideByColumn(_singleRowToContinuosRow(_divideByRow(img, height)), height))
	elif(scanning == "C"):
		return _flattenListOfList(_divideByColumn(_divideByRow(img, height), height))
	else:
		return _convertEncodeScanning(img, width, height, scanning)

def _generateZigZagIndex(x, y):
	listx = x[:]
	listy = y[:]
	listx.insert(0, 0)
	listy.insert(0, 0)

	resultlist = []

	for i in range(1, len(listy)):
		for k in range(1, len(listx)):
			resultlist.append([sum(listx[:k]), sum(listx[:k + 1]), sum(listy[:i]), sum(listy[:i + 1]) ])

	return resultlist

def _split8bitTo4bit(eightbit):
	leftmask = 240
	rightmask = 15
	left = (eightbit & leftmask) >> 4
	right = eightbit & rightmask

	return (left, right)

def _merge4bitTo8bit(left, right):
	return (left << 4) | right

def _encodeImage4bit(imagePixels, scanning, width, height):
	encodedImage = bytearray()

	count = 0

	prev = imagePixels[0]
	tempmap = ""

	for pixel in imagePixels:
		if count >= 15:
			encodedImage.append(15)
			encodedImage.append(prev)
			tempmap += "1"
			tempmap += "0"
			count = 0
			prev = pixel

		if pixel == prev:
			count += 1
		else:
			if count > 1:
				encodedImage.append(count)
				tempmap += "1"
			encodedImage.append(prev)
			tempmap += "0"
			count = 1
			prev = pixel

	if count > 1:
		encodedImage.append(count)
		tempmap += "1"

	encodedImage.append(prev)
	tempmap += "0"

	encodedImage.extend([0] * _remaining(len(encodedImage)))
	tempmap += "1"*_remaining(len(tempmap))

	encodedImage = _set4bitMap(tempmap, encodedImage)

	return encodedImage

def _set4bitMap(imgMap, encodedImage):
	newImgMap = _divideByRow(imgMap, 8)

	tempImg = [_merge4bitTo8bit(encodedImage[i], encodedImage[i + 1]) for i in range(0, len(encodedImage), 2)]
	tempImg = _divideByRow(list(tempImg), 4)

	return bytearray(_flattenListOfList(_mergeMap(tempImg, newImgMap)))

def _decodeImage4bit(encodedImage, width, height, scanning):
	decodedImage = []

	imgMap, encImg = _get4bitMap(encodedImage)

	for index, i in enumerate(imgMap):
		if i == '1' and encImg[index] == 0:
			break

		if i == '1':
			decodedImage.extend([encImg[index + 1]] * encImg[index])
		elif imgMap[index - 1] != '1' or index == 0:
			decodedImage.append(encImg[index])

	return decodedImage

def _get4bitMap(encodedImage):
	imgMap = ""

	newEncodedImage = list(encodedImage)

	I = range(0, len(newEncodedImage), 5)

	for i in I:
		imgMap += '{0:08b}'.format(newEncodedImage[i])

	for i in sorted(list(I), reverse = True):
		del newEncodedImage[i]

	newEncodedImage = _flattenListOfList([_split8bitTo4bit(i) for i in newEncodedImage])

	return (imgMap, newEncodedImage)
