import png
import os
import colorsys


### DETERMINE FILENAME
def get_max_increment(basename):
    required_length = len(basename + '000' + '.txt')
    matching_files = [f for f in os.listdir('.') if basename in f and len(f) == required_length]
    if len(matching_files) == 0:
        return 0
    maximum = max(matching_files)[len(basename):-4]
    return int(maximum) + 1


#### DEFINE A NEW COLOR PALETTE FOR THE OCEANS
#### The original bathymetry map uses white for shallow water
#### and the original population map uses white for unpopulated
#### which means that unpopulated land and shallow water blend together
#### especially along the coast of Nambia and northwestern Australia

def source_ocean_colorset(bathyrgb):
    # find all unique colors defined in the original image
    colors = set()
    for n in range(1800):
        bline = next(bathyrgb)
        for i in range(3600):
            base = i*3
            cstring = ",".join([str(bline[idx]).zfill(3) for idx in [base, base + 1, base + 2]])
            colors.add(cstring)
    colors = [",".join([str(int(y)) for y in x.split(",")]) for x in sorted(list(colors))]
    return colors


def hls_transform(old_color, hls_func):
    rgb = [int(x) for x in old_color.split(",")]
    hls = list(colorsys.rgb_to_hls(*[x / 256 for x in rgb]))
    hls_new = hls_func(*hls)  # params taken: hue, light, saturation
    rgb_new = [int(x * 256) for x in colorsys.hls_to_rgb(*hls_new)]
    return ",".join([str(x) for x in rgb_new])

def map_colors_with_hls(source_colors, hls_func):
    return {color: hls_transform(color, hls_func) for color in source_colors}


def line(start, stop, i):
    return start + (stop - start) * i / 256

def para(top, bottom, i):
    a = (top - bottom) / 127.5**2
    return a * (i - 127.5) + bottom

def generate_palette(hue_func, light_func, sat_func):
    new_palette = [[int(x * 256) for x in colorsys.hls_to_rgb(hue_func(i), light_func(i), sat_func(i))] for i in range(256)]
    return list(new_palette)

def generate_colormap(source_map, new_palette):
    palmap = {}
    for i in range(len(source_map)):
        palmap[source_map[i]] = ",".join([str(x) for x in new_palette[i]])
    return palmap



### MERGE OCEAN INTO POPULATION MAP

def stitch_maps(bathymetry_colormap, lake_color, glacial_color):
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
                currline.extend(lake_color)
            elif ppixel == popwater:
                if bpixel == black:  
                    # bathymetry map identifies this as land, therefore must be lake or glacier
                    currline.extend( glacial_color if n > 1436 else lake_color )
                else:  
                    # have bathymetry data, color it using transformed colormap
                    idx = ",".join([str(x) for x in bpixel])
                    mapped = [int(x) for x in bathymetry_colormap[idx].split(",")]
                    currline.extend(mapped)
            else: # use population data
                if ppixel == [255,246,234]:
                    currline.extend([242,238,238])  # darken the empty land a bit
                else:
                    currline.extend(ppixel)
        newmap.append(currline)
    return newmap



#### PROCEDURAL BLOCK
bathyrgb = png.Reader('bathymetry.png').asRGB()[2]
imagebase = 'merged_'
specbase = 'mapspec_'
iteration = str(max(get_max_increment(imagebase), get_max_increment(specbase))).zfill(3)
imagename = imagebase + iteration + '.png'
specname = specbase + iteration + '.txt'

print("Generating new image " + imagename)  # + " with specification " + specname)

source_colors = source_ocean_colorset(bathyrgb)

def darken_and_desaturate(hue, light, sat):
    return [hue, light * 0.8, sat if light < 0.5 else sat * 0.75]

shrink4 = map_colors_with_hls(source_colors, darken_and_desaturate)

# spec = [hue_min, hue_max, light_min, light_max, sat_min, sat_max]
#c = [0.55, 0.67, 0.1, 0.5, 0.9, 1]
#c = [0.57, 0.63, 0.2, 0.7, 0.8, 0.9]
c = [0.56, 0.59, 0.0, 0.75, 0.5, 0.8]
new_palette = generate_palette(lambda i: para(c[0],c[1], i), lambda i: line(c[2],c[3], i), lambda i: para(c[4],c[5],i))
palmap = generate_colormap(source_colors, new_palette)

# I guess lake color is one step lighter than the lightest ocean color?
#print(new_palette[-1])
#print(palmap["246,251,255"])

lake = new_palette[-1]
glacier = [223, 227, 235]
lake_color = new_palette[-1]
newmap = stitch_maps(palmap, lake_color, glacier)

png.from_array(newmap, 'RGB').save(imagename)
#with open(specname, 'w') as f:
#    f.write("using SPEC")

# [225, 229, 233]
# [138, 186, 242]
# [182, 207, 237]
