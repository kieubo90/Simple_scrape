import requests
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
from collections import Counter

tag_counter = Counter()
def add_count(number):
    tag_counter[number] += 1
def find_most_frequent_tags(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Count occurrences of tag-attribute-value combinations
    tag_attr_counts = Counter()
    print(tag_attr_counts)
    for tag in soup.find_all('div'):
        for attr, value in tag.attrs.items():
            # Handling list attributes by joining them into a string
            if isinstance(value, list):
                value = ' '.join(value)
            tag_attr_counts[(tag.name, attr, value)] += 1

    # Find the tag-attribute combinations with the highest frequency
    most_frequent = tag_attr_counts.most_common(1)
    if not most_frequent:
        print("No frequently repeating tag-attribute combinations found.")
        return

    # Assuming the most common count is significant, filter and print those combinations
    most_common_count = most_frequent[0][1]
    for tag_attr, count in tag_attr_counts.items():
        if count == most_common_count:
            print(f"Tag: {tag_attr[0]}, {tag_attr[1]}: {tag_attr[2]} - Count: {count}")
            add_count(count)

# Example usage
url = "https://www.s-kaupat.fi/tuotteet/makeiset-ja-naposteltavat-1/sesonki-ja-lahjamakeiset/sokerimakeiset"
find_most_frequent_tags(url)
print(tag_counter)