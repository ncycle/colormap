import png
import colorsys

row = []
for b in range(0,256):
    row.extend([0,0,b])


def line(start, stop, i):
    return start + (stop - start) * i / 256

def para(top, bottom, i):
    a = (top - bottom) / 127.5**2
    b = bottom
    return a * (i - 127.5) + bottom

c = [0.58, 0.68, 0.3, 0.5, 0.9, 0.6]
colors = [
#        [0,1,0.4,.4,1,1],
#        [0,1,0,1,0,1],
#        [0.57, 0.63, 0.2, 0.9, 0.8, 0.9],
#        [0.57, 0.63, 0.2, 0.7, 0.8, 0.9],
#        [0.57, 0.67, 0.3, 0.4, 0.9, 0.7],
#        [0.5, 0.7, 0.5, 0.5, 0.9, 0.9],
#        [0.55, 0.7, 0.2, 0.5, 0.9, 1],
#        [0.55, 0.67, 0.1, 0.5, 0.9, 1],
#        [0.55, 0.67, 0.4, 0.7, 0.6, .7],
#        [0.4, 0.8, 0.4, 0.7, 0.6, .7],
        [0.55, 0.65, 0.4, 0.1, 0.4, 0.8],
        [0.59, 0.59, 0.02, 0.98, 0.5, 0.8],
        [0.56, 0.59, 0.02, 0.6, 0.5, 0.8],
        [0.56, 0.59, 0.02, 0.7, 0.5, 0.8],
        [0.56, 0.59, 0.1, 0.7, 0.5, 0.8],
]

image = []
for c in colors:
    row = []
    row2 = []
    row3 = []
    for i in range(0,256):
        pixel = [int(x * 256) for x in colorsys.hls_to_rgb(line(c[0],c[1],i), line(c[2],c[3],i), para(c[4],c[5],i))]
        row.extend(pixel)
        pixel2 = [int(x * 256) for x in colorsys.hls_to_rgb(para(c[0],c[1],i), line(c[2],c[3],i), para(c[4],c[5],i))]
        row2.extend(pixel2)
        pixel3 = [int(x * 256) for x in colorsys.hls_to_rgb(line(c[0],c[1],i), line(c[2],c[3],i), line(c[4],c[5],i))]
        row3.extend(pixel3)
    image.extend([row for i in range(25)])
    image.extend([row2 for i in range(25)])
    image.extend([row3 for i in range(25)])

#image = [row for i in range(10)]

png.from_array(image, 'RGB').save('palette.png')
