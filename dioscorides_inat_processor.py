import requests
import time
import re

default_photo_pattern = re.compile(r'"default_photo":\s*\{[^}]*\}', re.DOTALL)

def extract_default_photos_raw(content):
    matches = default_photo_pattern.findall(content)
    return matches

def process_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()	
        content = response.text
        default_photos_raw = extract_default_photos_raw(content)

        if default_photos_raw:
	    # get the taxon from the end of the URL
            primary_key = url.split('/')[-1]

            # save default_photos data in, e.g., 123456_default_photos_raw.txt
            with open(f'{primary_key}_default_photos_raw.txt', 'w') as file:
                for photo in default_photos_raw:
                    file.write(photo + "\n\n")

	    # maybe succeeed quietly and fail loudly ... 
            print(f"{primary_key} image data => {primary_key}_default_photos_raw.txt")
        else:
            print(f"Failed: No default_photos at {url}")

    except requests.RequestException as e:
        print(f"request to {url} failed: {e}")

with open('inat_url_list.txt', 'r') as file:
    urls = file.readlines()

for url in urls:
    url = url.strip()
    if url:
        process_url(url)
        time.sleep(3)	# NOTE: this is a 3-second delay to prevent hammering inat

