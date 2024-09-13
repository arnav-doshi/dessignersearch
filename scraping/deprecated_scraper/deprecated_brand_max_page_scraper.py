## WORKS BUT ERROR 403
import requests
from bs4 import BeautifulSoup

def check_page(url, target_class):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.find(class_=target_class):
                return True
            else:
                return False
        else:
            print(f"Error: {url} returned status code {response.status_code}")
            return False
    except requests.RequestException as e:
        print("Error:", e)
        return False

# List of URLs to check
urls = [
    'https://www.ssense.com/en-us/men/designers/reebok-classics?page=3000',
'https://www.ssense.com/en-us/men/designers/reese-cooper?page=2',
'https://www.ssense.com/en-us/men/designers/reigning-champ?page=2',
'https://www.ssense.com/en-us/men/designers/represent?page=2',
'https://www.ssense.com/en-us/men/designers/super?page=2',
'https://www.ssense.com/en-us/men/designers/rhude?page=2',
'https://www.ssense.com/en-us/men/designers/rick-owens?page=2',
'https://www.ssense.com/en-us/men/designers/rick-owens-drkshdw?page=2',
'https://www.ssense.com/en-us/men/designers/rier?page=2',
'https://www.ssense.com/en-us/men/designers/rigards?page=2',
]

target_class = "plp-product-listing-info__title"

for url in urls:
    if not check_page(url, target_class):
        print(url, "False")
