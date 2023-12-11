from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import csv
import requests
import time

max_pages = 1  # Example limit for number of pages
current_page = 1

ica_url = 'https://handlaprivatkund.ica.se/stores/1015001/categories/Glass-Godis-Snacks/Choklad/abfad4ad-011b-49cf-af79-9c3d120ab0a3?source=navigation'
ica_findAll_tag = "div"
ica_findAll_class = "base__Body-sc-1mnb0pd-34 gRNUPx"
ica_name_tag = "a"
ica_name_class = "link__Link-sc-14ymsi2-0 dSyqLR link__Link-sc-14ymsi2-0 base__Title-sc-1mnb0pd-27 base__FixedHeightTitle-sc-1mnb0pd-43 dSyqLR ctGnCh cCRJZx"
ica_price_tag = "div"
ica_price_class = "base__PriceWrapper-sc-1mnb0pd-28 dDLLyP"
ica_product = 'ica_product.csv'
#############################################################################################################################################
k_url = "https://www.k-ruoka.fi/kauppa/tuotehaku/kala-ja-merenelavat"
k_findAll_tag = "li"
k_findAll_class = "HoverCard-sc-17t78cx-0 ProductCard__Container-sc-12u3k8m-0 gzzviz cXoBjH"
k_name_tag = "div"
k_name_class = "ProductCard__Name-sc-12u3k8m-6 bWiPwy"
k_price_tag = "div"
k_price_class = "ProductPrice__PriceGrid-sc-u2ag1v-3 xCfNc"
#############################################################################################################################################
page_number = 1
fixed_width = 50

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/12.246"} 
another_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}
# Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link. 
try:
	with open(ica_product, mode='w', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		session = requests.Session()
		session.headers.update(another_headers)
		while current_page <= max_pages:
			try:
				page = session.get(url=ica_url, timeout=5)
				page.raise_for_status()
				soup = bs(page.text, 'html.parser')
				product_container = soup.find_all(ica_findAll_tag, class_=ica_findAll_class)
				for container in product_container:
					product_name_tag = container.find(ica_name_tag, class_=ica_name_class)
					product_name = product_name_tag.text.strip() if product_name_tag else "No Name"

					product_price_tag = container.find(ica_price_tag, class_=ica_price_class)
					product_price = product_price_tag.text.strip() if product_price_tag else "No Price"
					writer.writerow([product_name, product_price])
				current_page += 1  # Move to the next page
				time.sleep(1)
			except requests.exceptions.HTTPError as e:
				print(f"HTTP Error: {e}")
				break
			except requests.exceptions.ConnectionError as e:
				print(f"Connection Error: {e}")
				break
			except requests.exceptions.Timeout as e:
				print(f"Timeout Error: {e}")
				break
			except requests.exceptions.RequestException as e:
				print(f"Request Exception: {e}")
				break

except KeyboardInterrupt:
	print("Script interrupted by user.")