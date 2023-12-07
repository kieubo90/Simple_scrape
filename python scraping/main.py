from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import csv
import requests

base_url = 'https://www.s-kaupat.fi/tuotteet/makeiset-ja-naposteltavat-1'
page_number = 1
fixed_width = 50
with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
	writer = csv.writer(file)
	writer.writerow(['Product Name', 'Product Price'])
	while True:
		url = f"{base_url}?page={page_number}"  # Modify this based on how the website's URL changes with each page
		page = requests.get(url)
		soup = bs(page.text, 'html.parser')

		product_container = soup.find_all("div", class_="sc-ddb02d9f-0 dHHZyS")  # Check if this class is correct
		if not product_container:
			break
		for container in product_container:
			product_name_tag = container.find("span", class_="sc-4dcde147-0 egffZb")
			product_name = product_name_tag.text if product_name_tag else "No Name"

			product_name = product_name.ljust(fixed_width)
		# Extracting the product price
			product_price_tag = container.find("span", class_="sc-68088102-0 jusdFT")
			product_price = product_price_tag.text if product_price_tag else "No Price"
			writer.writerow([product_name, product_price])
			#print(f"Product Name: {product_name}, Product Price: {product_price}")
		page_number += 1
