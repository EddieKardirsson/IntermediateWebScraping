from bs4 import BeautifulSoup
import requests
import re
import os

# GET the URL content and store it into a local file as an html-file
def get_html(url, path):
    response = requests.get(url)
    with open(path, 'w', encoding="utf-8") as f:
        f.write(response.text)

print(' ')

path = "./html_docs/bristlecone.html"
url = "https://en.wikipedia.org/wiki/Bristlecone_pine"

if not os.path.exists(path):
    get_html(url, path)

with open(path, 'r', encoding="utf-8") as f:
    html = f.read()


soup = BeautifulSoup(html, 'html.parser')
print(soup.title, '\n')

section_headings = soup.find_all('h2')
print(section_headings, '\n')

section_headings = [h2.string for h2 in section_headings]
print(section_headings, '\n')
print(type(section_headings[0]), '\n')
print(section_headings[0].parent, '\n')

taxonomy = {}
infobox = soup.find('table', attrs={'class': 'infobox biota'})
print(infobox, '\n')

def taxonomy_filter(tag):
    return ':' in tag.text and tag.name == 'td'

filtered = infobox.find_all(taxonomy_filter)
print(filtered, '\n')

for tag in filtered:
    sibling = tag.next_sibling.next_sibling

    taxonomy[tag.text.strip().replace(':', '')] = sibling.text.strip()

print(taxonomy, '\n')

def another_taxonomy_filter(tag):
    return tag.name == 'tr' and len(list(tag.children)) == 4

print('Second method: ', infobox.find_all(another_taxonomy_filter))

p_content = soup.find_all('p')
print(p_content)

body_links = []
for p in p_content:
    body_links += p.find_all('a')

print(body_links, '\n')

body_links = list(filter(lambda a: '#cite' not in a['href'], body_links))
print(body_links, '\n')

links = {}
for a in body_links:
    links[a['title']] = a['href'] = 'https://en.wikipedia.org' + a['href']

print(links, '\n')

imgs = soup.find_all('img')
print(imgs, '\n')

for i in imgs:
    if 'class' in i.attrs:
        print(i['class'])
    else:
        print(i)

imgs = list(filter(lambda img: 'class' in img.attrs, imgs))
imgs = list(filter(lambda img: img['class'][0] == 'mw-file-element', imgs))
for img in imgs:
    print(img['src'], '\n')

def download_image(url, path):
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)

img_path = "./html_docs/image.png"
if not os.path.exists(img_path):
    download_image('https:' + imgs[0]['src'], img_path)


citations = soup.find('ol', attrs={'class': 'references'})
print(citations, '\n')

cite_tags = citations.find_all('cite')
print(cite_tags, '\n')
print(cite_tags[0].text, '\n')

isbn_doi = [c.text for c in cite_tags if 'ISBN' in c.text or 'doi' in c.text]
print(isbn_doi, '\n')
