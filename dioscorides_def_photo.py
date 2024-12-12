import os
import re
import csv

# hello again; maybe just collapse all this stuff into one package
default_photo_pattern = re.compile(
    r'"default_photo":\s*\{.*?"id":(\d+),.*?"license_code":"(.*?)",.*?"attribution":"(.*?)",.*?"url":"(.*?)",.*?\}',
    re.DOTALL
)

output_file = 'default_photos_data.csv'

# set up the CSV file for the data -- columns for taxon, photo id, license, attribution, and URL
with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['taxon', 'photo_id', 'license_code', 'attribution', 'url'])

    for filename in os.listdir('.'):
        if filename.endswith('_default_photos_raw.txt'):
            taxon = filename.split('_')[0]

            with open(filename, 'r') as file:
                content = file.read()
            matches = default_photo_pattern.findall(content)

            for match in matches:
                photo_id, license_code, attribution, url = match
                csvwriter.writerow([taxon, photo_id, license_code, attribution, url])

# lol we actually have no idea whether this was successful or not; FIXME error handling 
print(f"writing to {output_file} complete")


