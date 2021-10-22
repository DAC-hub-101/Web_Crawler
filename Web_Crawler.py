from bs4 import BeautifulSoup
import requests
import re

# Ask the user what gpu are they locking for
search_term = input("What product do you want to search for? ")

# Sending a request to www.newegg.ca
url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"
page = requests.get(url).text

# Read with BeautifulSoup
doc = BeautifulSoup(page, "html.parser")

# Locking for the number of pagination the web page haves in <div class = "list-tool-pagination">
# <span class = list-tool-pagination-text"> , strong tag <strong>
page_text = doc.find(class_="list-tool-pagination-text").strong

# Stringing the page_text to avoid error from comments in <strong> tag, splitting the string to find whats on the
# right side of the slash, then splitting the string again to get the second last element.
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])  # splitting at > and removing it

# Putting items from "for item in items:" Loop
items_found = {}

# Looping through all of the pages and getting the elements in them
for page in range(1, pages + 1):
    # Sending another request looking for the specific page
    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    # Div that haves the table in it, and looking for text only in the table
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    # Getting all of the specified items from each page
    items = div.find_all(text=re.compile(search_term))  # matching any text that contains them, that's why im using
    # Regular expressions

    # Looping through all the items
    for item in items:
        parent = item.parent
        # Checking if parent is <a> tag
        if parent.name != "a":
            continue

        # Grabbing the link from the href
        link = parent['href']
        next_parent = item.find_parent(class_="item-container")  # Locking for any ancestor in the tree and finding the
        # First parent having this class name


        try:
            # Finding the price
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
        except:
            pass

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])  # Sorting by the price in the dictionary

for item in sorted_items:
    print(item[0])  # The key
    print(f"${item[1]['price']}")  # The value
    print(item[1]['link'])  # Printing the Link
    print("-------------------------------")

print('Finish')
