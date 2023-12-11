import requests
import http
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import random

user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
]
headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.k-ruoka.fi',
    'Referer': 'https://www.k-ruoka.fi/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'content-type': 'text/plain',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

data = '{"xhr":[{"params":{"method":"POST","hostname":"bam.nr-data.net","port":"443","protocol":"https","host":"bam.nr-data.net:443","pathname":"/jserrors/1/3bdb5ef4c2","status":200},"metrics":{"count":1,"txSize":{"t":295},"rxSize":{"t":24},"duration":{"t":1625},"cbTime":{"t":0},"time":{"t":592884}}}]}'

tag_counter = Counter()
def add_count(number):
    tag_counter[number] += 1
def find_common_attributes(url, min_count):
    # Fetch the content from the URL
    try:
        response = requests.get(url,headers={'User-Agent': random.choice(user_agents_list)})
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Dictionary to hold counts of tags with their attributes
    attribute_counts = defaultdict(Counter)

    # Iterate over all tags and count their attributes
    for tag in soup.find_all():
        for attr, value in tag.attrs.items():
            # Convert list attributes to a string
            if isinstance(value, list):
                value = ' '.join(value)
            
            attribute_key = (tag.name, attr, value)
            attribute_counts[attr][attribute_key] += 1

    # Identify and print the most common attributes with more than min_count occurrences
    for attr, counts in attribute_counts.items():
        common_attributes = {tag_info: count for tag_info, count in counts.items() if count >= min_count}
        if common_attributes:
            print(f"\nMost common {attr}:")
            for tag_info, count in sorted(common_attributes.items(), key=lambda x: x[1], reverse=True):
                print(f"Tag: {tag_info[0]}, {attr}: {tag_info[2]} - Count: {count}")
                add_count(count)

############################################################################################
def find_common_attributes_by_file(url, min_count):
    # Fetch the content from the URL
	try:
		with open(url, 'r', encoding='utf-8') as html_file:
			content = html_file.read()
	except:
		print(f"Error open the file\n")
		return

	# Parse the HTML content
	soup = BeautifulSoup(content, 'lxml')

	# Dictionary to hold counts of tags with their attributes
	attribute_counts = defaultdict(Counter)

	# Iterate over all tags and count their attributes
	for tag in soup.find_all():
		for attr, value in tag.attrs.items():
		# Convert list attributes to a string
			if isinstance(value, list):
				value = ' '.join(value)
	
			attribute_key = (tag.name, attr, value)
			attribute_counts[attr][attribute_key] += 1

	# Identify and print the most common attributes with more than min_count occurrences
	for attr, counts in attribute_counts.items():
		common_attributes = {tag_info: count for tag_info, count in counts.items() if count >= min_count}
		if common_attributes:
			print(f"\nMost common {attr}:")
			for tag_info, count in sorted(common_attributes.items(), key=lambda x: x[1], reverse=True):
				print(f"Tag: {tag_info[0]}, {attr}: {tag_info[2]} - Count: {count}")
				add_count(count)


# Example usage
url = "https://www.s-kaupat.fi/tuotteet/makeiset-ja-naposteltavat-1/sesonki-ja-lahjamakeiset/sokerimakeiset"
ica_url = "https://handlaprivatkund.ica.se/stores/1015001/categories/Glass-Godis-Snacks/Choklad/abfad4ad-011b-49cf-af79-9c3d120ab0a3?source=navigation"
amazon_url = "https://www.amazon.de/s?k=mechanische+tastatur&crid=3B6JVNPU954TI&sprefix=mecha%2Caps%2C93&ref=nb_sb_ss_ts-doa-p_1_5"
s_market_url = "https://www.s-kaupat.fi/tuotteet/makeiset-ja-naposteltavat-1"
s_market_liha_url = "https://www.s-kaupat.fi/tuotteet/ruokatori/liha/nauta"
k_market_kala_url = "https://www.k-ruoka.fi/kauppa/tuotehaku/kala-ja-merenelavat"
k_market_url = "https://www.k-ruoka.fi/kauppa/tuotehaku/kala-ja-merenelavat/tuorekala/kirjolohi"
k_market_kala_file = 'k_market_kala.html'
#find_common_attributes(ica_url, 10)
find_common_attributes_by_file(k_market_kala_file, 10)
print(tag_counter)
