from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
import csv
import requests
import time


# driver = webdriver.Safari()
NUMBER_OF_SCROLLS = 20
SCROLL_PAUSE_TIME = 4
SCROLL_INCREMENT = 500

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
k_product = 'k_product_kala.csv'
#############################################################################################################################################
page_number = 1
fixed_width = 50

options = Options()
options.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
driver = webdriver.Firefox(options=options)
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/12.246"} 
another_headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
# Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link. 
driver.get(k_url)
with open(k_product, mode='w', newline='', encoding='utf-8') as file:
	writer = csv.writer(file)
	scraped_products = set()

	for _ in range(NUMBER_OF_SCROLLS):
	# Scroll incrementally
		scroll_height = driver.execute_script("return document.body.scrollHeight;")
		
		for i in range(0, scroll_height, SCROLL_INCREMENT):
			driver.execute_script(f"window.scrollTo(0, {i});")
			time.sleep(SCROLL_PAUSE_TIME)
			soup = bs(driver.page_source, 'html.parser')
			product_container = soup.find_all(k_findAll_tag, class_=k_findAll_class)
			
			for container in product_container:
				product_name_tag = container.find(k_name_tag, class_=k_name_class)
				product_name = product_name_tag.text.strip() if product_name_tag else "No Name"
				product_price_tag = container.find(k_price_tag, class_=k_price_class)
				product_price = product_price_tag.text.strip() if product_price_tag else "No Price"
				
				#check if duplicate
				if (product_name, product_price) not in scraped_products:
					writer.writerow([product_name, product_price])
					scraped_products.add((product_name, product_price))
		new_scroll_height = driver.execute_script("return document.body.scrollHeight;")
		if new_scroll_height == scroll_height:
			break
		else:
			scroll_height = new_scroll_height

# 	driver.quit()