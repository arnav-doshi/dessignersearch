import csv
import bs4
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from google.colab import drive

drive.mount("/content/drive", force_remount=True)

def transform_thumb_to_high_res(thumb_url):
    # Example transformation
    # Replace the URL pattern according to your requirement
    return thumb_url.replace('/c_scale,h_280/', '/')

# Open the input CSV file containing the list of URLs
input_csv_file_path = '/content/drive/MyDrive/SSenseProject/urls3.csv'
output_csv_file_path = '/content/drive/MyDrive/SSenseProject/high_res_urls3.csv'

# Open the output CSV file for writing
with open(input_csv_file_path, 'r') as input_file, open(output_csv_file_path, 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    for row in reader:
        url = row[0]  # Assuming URLs are in the first column
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        request = urllib.request.Request(url, headers=headers)
        page = urllib.request.urlopen(request)

        page_soup = BeautifulSoup(page, 'html.parser')

        img_items = page_soup.find('div',{'class':'plp-products__row'})
        img_div = img_items.find_all(class_='plp-products__product-tile')

        for img in img_div:
            img_tag = img.find('img')
            img_src = img_tag.get('data-srcset')
            high_res_url = transform_thumb_to_high_res(img_src)
            print(high_res_url)

            # Write the high-res URL to the output CSV file
            writer.writerow([high_res_url])

            # Introduce a delay of 1 second between requests
           # time.sleep(1)

print("High-res URLs saved to:", output_csv_file_path)
