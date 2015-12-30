import math

filename = "24bit.bmp"

f = open(filename, "rb")

f.read(2)
size = int.from_bytes(f.read(4),byteorder='little')
print('size', size)
f.read(4)
starting_address = f.read(4)

offset = int.from_bytes(starting_address, byteorder='little')

f.read(4)
width = int.from_bytes(f.read(4), byteorder='little')
height = int.from_bytes(f.read(4), byteorder='little')
print('width', width)
print('height', height)

pixelByteSize = 3 #only treats 24-bit depth images

f.seek(0)
allData = f.read()

print('total data', len(allData))
print('offset', offset)
print('image data', len(allData) - offset)

f.seek(0)
header = f.read(offset)#+b''.join(b'\x00' for i in range(size-(height*width*pixelByteSize+offset)))

print(offset + (height)*width*pixelByteSize)#(width)*pixelByteSize + 

f.close()

def getPixel(imgData, x, y):
	pos = offset + x*pixelByteSize + y*width*pixelByteSize
	rgbPixel = []
	for i in range(0, pixelByteSize):
		rgbPixel.append(imgData[pos:pos+3][2-i])
	return rgbPixel

pixelArray = []

for j in range(height):
	pixelArray.append([])
	#i = 0
	for i in range(width):
		pixelArray[-1].append(getPixel(allData, i, j))

def getBrightness(rgbPixel):
	return (rgbPixel[0]+rgbPixel[1]+rgbPixel[2])/3 #average conversion

brightnessArray = []

for j in range(height):
	brightnessArray.append([])
	i = 0
	for i in range(width):
		val = getBrightness(pixelArray[j][i])
		brightnessArray[-1].append(val)


def extendArray(array):
	array.insert(0, [])
	array.append([])
	array[0] = array[1][:]
	array[-1] = array[-2][:]
	for line in array:
		line.insert(0, line[0])
		line.append(line[-1])

extendArray(brightnessArray)

postArray = []

def transformation(array, x, y):
	lines = array[y-1:y+2]
	a = 0
	b = 0
	xTotal = 0
	yTotal = 0
	lines = map(lambda l: l[x-1:x+2], lines)
	for line in lines:
		a = 0
		for n in line:
			xTotal += ((a-1)*((b%2)+1))*n
			yTotal += ((b-1)*((a%2)+1))*n
			a += 1
		b += 1
	return math.sqrt(xTotal**2+yTotal**2)

def tranformArray(pre, post, height, width):
	for y in range(1, height + 1):
		post.append([])
		x = 0
		for x in range(1, width + 1):
			if(transformation(pre, x, y) > 100):
				post[-1].append(1)
			else:
				post[-1].append(0)

tranformArray(brightnessArray, postArray, height, width)

final = []

def binaryToRGB(pre, final):
	for y in range(0, height):
		final.append([])
		x = 0
		for x in range(0, width):
			if(pre[y][x] == 1):
				final[-1].append(b'\xff\xff\xff')
			else:
				final[-1].append(b'\x00\x00\x00')

binaryToRGB(postArray, final)

final = list(map(lambda x: b''.join(x), final))

final = b''.join(final)+b''.join(b'\x00' for i in range(size-(height*width*pixelByteSize+offset)))

final = header+final

output = open("edges_"+filename, 'wb')
output.write(final)
output.close()
