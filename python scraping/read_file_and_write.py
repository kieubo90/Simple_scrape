from bs4 import BeautifulSoup
import csv


amazon_findAll_tag = "div"
amazon_findAll_class = "puisg-col-inner"
amazon_name_tag = "span"
amazon_name_class = "a-size-medium a-color-base a-text-normal"
amazon_price_tag = "span"
amazon_price_class = "a-price-whole"
###############
k_findAll_tag = "li"
k_findAll_class = "HoverCard-sc-17t78cx-0 ProductCard__Container-sc-12u3k8m-0 gzzviz cXoBjH"
k_name_tag = "div"
k_name_class = "ProductCard__Name-sc-12u3k8m-6 bWiPwy"
k_price_tag = "div"
k_price_class = "ProductPrice__PriceGrid-sc-u2ag1v-3 xCfNc"
###############
ica_findAll_tag = "div"
ica_findAll_class = "base__Body-sc-1mnb0pd-34 gRNUPx"
ica_name_tag = "a"
ica_name_class = "link__Link-sc-14ymsi2-0 dSyqLR link__Link-sc-14ymsi2-0 base__Title-sc-1mnb0pd-27 base__FixedHeightTitle-sc-1mnb0pd-43 dSyqLR ctGnCh cCRJZx"
ica_price_tag = "div"
ica_price_class = "base__PriceWrapper-sc-1mnb0pd-28 dDLLyP"
# Open and read the HTML file
with open('amazon_keyboard.html', 'r', encoding='utf-8') as html_file:
    content = html_file.read()

# Parse the HTML content
soup = BeautifulSoup(content, 'lxml')

# Open the CSV file where you want to store the data
with open('amazon_keyboard.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Loop through the product containers
    product_container = soup.find_all(amazon_findAll_tag, class_=amazon_findAll_class)
    if not product_container:
        print("No product containers found.")
    else:
        for container in product_container:
            # Extract the product name
            product_name_tag = container.find(amazon_name_tag, class_=amazon_name_class)
            product_name = product_name_tag.text if product_name_tag else "No Name"

            # Extract the product price
            product_price_tag = container.find(amazon_price_tag, class_=amazon_price_class)
            product_price = product_price_tag.text if product_price_tag else "No Price"

            # Write the product name and price to the CSV file
            writer.writerow([product_name, product_price])
