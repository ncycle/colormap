from urllib import request

images = {
        'population_map.png': '875430',
        'bathymetry.png': '189313',
        'world.png': '526311',
        }

url = 'http://neo.sci.gsfc.nasa.gov/servlet/RenderData?si={map_id}&cs=rgb&format=PNG&width=3600&height=1800'

print("fetching source images...")
for image_name, image_id in images.items():
    print(url.format(map_id=image_id))
    image = request.urlopen(url.format(map_id=image_id))
    with open(image_name, 'b+w') as f:
        f.write(image.read())
