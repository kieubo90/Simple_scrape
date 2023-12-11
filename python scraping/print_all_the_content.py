import requests
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
tag_counter = Counter()
def add_count(number):
    tag_counter[number] += 1
def find_common_attributes(url):
    # Fetch the content from the URL
    try:
        response = requests.get(url)
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

    # Identify and print the most common attributes
    for attr, counts in attribute_counts.items():
        print(f"\nMost common {attr}:")
        for tag_info, count in counts.most_common():
            print(f"Tag: {tag_info[0]}, {attr}: {tag_info[2]} - Count: {count}")
            add_count(count)

# Example usage
url = "https://www.s-kaupat.fi/tuotteet/makeiset-ja-naposteltavat-1/sesonki-ja-lahjamakeiset/sokerimakeiset"
find_common_attributes(url)

print(tag_counter)