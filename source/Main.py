'''
Created on 06 Mar 2014

@author: Serdar ORMANLI
'''
import argparse
from PIL import Image
import RLE
from Detail import Detail

def encodeImage(path, scanningtype):
	img1 = Image.open(path)
	orgimg = list(img1.getdata(0))
	encodedimg = RLE.encodeImage(orgimg, img1.size[0], img1.size[1], img1.mode, scanningtype)
	tempimg = Detail(encodedimg, 1, img1.size[0], img1.size[1], img1.mode, scanningtype, img1.getpalette())
	compsize, filepath = RLE.saveCompressedToFile(tempimg, path)
	print("Encoded file saved to: " + filepath)

def decodeImage(path):
	compimg = RLE.openFileToCompressed(path)
	decodedimg = RLE.decodeImage(compimg.compressed, compimg.width, compimg.height, compimg.mode, compimg.scanning)
	newimage = Image.new(compimg.mode, (compimg.width, compimg.height))
	newimage.putdata(decodedimg)
	if compimg.mode == 'P':
		newimage.putpalette(compimg.palette)
	newfilepath = path[:len(path) - 9] + "-copy.bmp"
	newimage.save(newfilepath)
	print("Decoded file saved to: " + newfilepath)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'RLE Encoder. Serdar Ormanlı 2014')
	parser.add_argument('-e', '--encode', help = 'Image to encode.')
	parser.add_argument('-d', '--decode', help = 'Compressed file to decode.')
	parser.add_argument('-s', '--scanning', help = 'Works if encoding is set. Can be R, RR, ZZ, C, CR.')

	args = parser.parse_args()

	if not (args.encode or args.decode):
		parser.error('No action requested, add -e or -d')

	args = vars(args)

	if args['encode'] is not None and args['scanning'] is not None:
		scan = args['scanning']

		if scan not in ['R', 'RR', 'ZZ', 'C', 'CR']:
			scan = 'R'

		encodeImage(args['encode'], scan)
	elif args['decode'] is not None:
		decodeImage(args['decode'])
	else:
		print('Enter arguments correctly')
