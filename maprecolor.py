import png
import colorsys

bathyrgb = png.Reader('bathymetry.png').asRGB()[2]

#### DEFINE A COLOR PALETTE MAPPING
colors = set()
for n in range(1800):
    bline = next(bathyrgb)
    for i in range(3600):
        base = i*3
        cstring = str(bline[base]) + "," + str(bline[base+1]) + "," + str(bline[base+2])
        cstring = str(bline[base]).zfill(3) + "," + str(bline[base+1]).zfill(3) + "," + str(bline[base+2]).zfill(3)
        colors.add(cstring)
colors = [",".join([str(int(y)) for y in x.split(",")]) for x in sorted(list(colors))]

shrink4 = {}
colormap = []
for color in colors:
    rgb = [int(x) for x in color.split(",")]
    hls = list(colorsys.rgb_to_hls(*[x / 256 for x in rgb]))
    hls_dark_old = [hls[0], hls[1] * 0.85, hls[2]]
    hls_dark = [hls[0], hls[1] * 0.8, hls[2] if hls[1] < .5 else hls[2] * .75]
    rgb_dark = [int(x * 256) for x in colorsys.hls_to_rgb(*hls_dark)]
    colormap.append([color, hls[2], ",".join([str(x) for x in rgb_dark])])
    shrink4[color] = ",".join([str(x) for x in rgb_dark])

#sorted_colormap = sorted(colormap, key=lambda x: x[1])
sorted_colormap = colors

def line(start, stop, i):
        return start + (stop - start) * i / 256

def para(top, bottom, i):
    a = (top - bottom) / 127.5**2
    return a * (i - 127.5) + bottom


c = [0.55, 0.67, 0.1, 0.5, 0.9, 1]
c = [0.57, 0.63, 0.2, 0.7, 0.8, 0.9]
c = [0.56, 0.59, 0.0, 0.7, 0.5, 0.8]
new_palette = [[int(x * 256) for x in colorsys.hls_to_rgb(para(c[0],c[1],i), line(c[2],c[3],i), para(c[4],c[5],i))] for i in range(256)]
new_palette = list(new_palette)

palmap = {}
for i in range(len(sorted_colormap)):
    palmap[sorted_colormap[i]] = ",".join([str(x) for x in new_palette[i]])

### MERGE OCEAN INTO POPULATION MAP


pop = png.Reader('population_map.png').asRGB()[2]
bathy = png.Reader('bathymetry.png').asRGB()[2]
highlights = png.Reader('highlight-lakes-caspian.png').asRGB()[2]
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
                mapped = [int(x) for x in shrink4[idx].split(",")]
                mapped = [int(x) for x in palmap[idx].split(",")]
                currline.extend(mapped)
        else: # use population data
            if ppixel == [255,246,234]:
                currline.extend([242,238,238])  # darken the empty land a bit
                continue
            currline.extend(ppixel)
    newmap.append(currline)

png.from_array(newmap, 'RGB').save('merged9p0.png')
