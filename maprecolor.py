import png
import colorsys

pop = png.Reader('population_map.png')
world = png.Reader('world.png')
bathy = png.Reader('bathymetry.png')

rgbpop = pop.asRGB()
rgbbath = bathy.asRGB()

#### DEFINE A COLOR PALETTE MAPPING
colors = set()
popcolors = set()
for n in range(1800):
    bline = next(rgbbath[2])
    pline = next(rgbpop[2])
    for i in range(3600):
        base = i*3
        cstring = str(bline[base]) + "," + str(bline[base+1]) + "," + str(bline[base+2])
        colors.add(cstring)
        pstring = str(pline[base]) + "," + str(pline[base+1]) + "," + str(pline[base+2])
        popcolors.add(pstring)

rgb = [[int(x) for x in color.split(",")] for color in colors]
hls = [colorsys.rgb_to_hls(*x) for x in rgb]
#hls = [colorsys.rgb_to_hls(*[x / 256 for x in elt]) for elt in rgb]
#hlsv = sorted(hls, key=lambda x: x[2])
#rgbv = [[int(y * 256) for y in colorsys.hls_to_rgb(*x)] for x in hlsv]
#
#for x in rgb:
#    if x not in rgbv:
#        print(x)
#
#for y in rgbv:
#    if y not in rgb:
#        print(y)
#
#exit()

hlsv = hls
hls2 = [(x[0],x[1] * .85, x[2])  for x in hlsv]
hls3 = [(x[0],x[1], x[2]) for x in hlsv]
rgb2 = [[int(y) for y in colorsys.hls_to_rgb(*x)] for x in hls2]
rgb3 = [[int(y) for y in colorsys.hls_to_rgb(*x)] for x in hls3]
shrink2 = {",".join([str(x) for x in rgb[i]]): ",".join([str(y) for y in rgb2[i]]) for i in range(len(rgb))}
shrink3 = {",".join([str(x) for x in rgb[i]]): ",".join([str(y) for y in rgb3[i]]) for i in range(len(rgb))}


### MERGE OCEAN INTO POPULATION MAP


pop = png.Reader('population_map.png').asRGB()[2]
bathy = png.Reader('bathymetry.png').asRGB()[2]
highlights = png.Reader('merged9f2.png').asRGB()[2]
world = png.Reader('world.png').asRGB()[2]

wblue = [27,66,121]
wdarkblue = [17,48,95]
pink = [255,0,220]
green = [0,255,33]
popwater = [197,204,224]
black = [0,0,0]

newmap = []
for n in range(1800):
    currline = []
    pline = next(pop)
    bline = next(bathy)
    hline = next(highlights)
    wline = next(world)
    for i in range(3600):
        base = i * 3
        ppixel = [pline[base], pline[base+1], pline[base+2]]
        bpixel = [bline[base], bline[base+1], bline[base+2]]
        hpixel = [hline[base], hline[base+1], hline[base+2]]
        wpixel = [wline[base], wline[base+1], wline[base+2]]
        if hpixel == green:  # specify color of lakes
            currline.extend(popwater)
#            currline.extend(wblue)
        elif ppixel == popwater:
#            currline.extend(wpixel)
            if bpixel == [0,0,0]:  # bathymetry map identifies this as land
                currline.extend([225,229,233])  # remapped lightest-er water color
            else:  # have bathymetry data, darken it
                idx = ",".join([str(x) for x in bpixel])
                mapped = [int(x) for x in shrink3[idx].split(",")]
                currline.extend(mapped)
        else: # use population data
            #if ppixel == [255,246,234]:
            #    currline.extend([242,238,238])  # darken the empty land a bit
            #    continue
            currline.extend(ppixel)
    newmap.append(currline)

png.from_array(newmap, 'RGB').save('merged9h.png')
