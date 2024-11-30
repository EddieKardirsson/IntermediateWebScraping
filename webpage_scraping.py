from bs4 import BeautifulSoup
import requests
import re

# GET the URL content and store it into a local file as an html-file
def get_html(url, path):
    response = requests.get(url)
    with open(path, 'w', encoding="utf-8") as f:
        f.write(response.text)

path = "./html_docs/bristlecone.html"
url = "https://en.wikipedia.org/wiki/Bristlecone_pine"
# get_html(url, path)

with open(path, 'r', encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
# print(soup.title)

section_headings = soup.find_all('h2')
# print(section_headings)

section_headings = [h2.string for h2 in section_headings]
print(section_headings)
print(type(section_headings[0]))
print(section_headings[0].parent)