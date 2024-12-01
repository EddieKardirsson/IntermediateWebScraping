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
# print(soup.title)

section_headings = soup.find_all('h2')
# print(section_headings)

section_headings = [h2.string for h2 in section_headings]
# print(section_headings)
# print(type(section_headings[0]))
# print(section_headings[0].parent)

taxonomy = {}
infobox = soup.find('table', attrs={'class': 'infobox biota'})
# print(infobox)

def taxonomy_filter(tag):
    return ':' in tag.text and tag.name == 'td'

filtered = infobox.find_all(taxonomy_filter)
# print(filtered)

for tag in filtered:
    sibling = tag.next_sibling.next_sibling

    taxonomy[tag.text.strip().replace(':', '')] = sibling.text.strip()

# print(taxonomy)

def another_taxonomy_filter(tag):
    return tag.name == 'tr' and len(list(tag.children)) == 4

# print('Second method: ', infobox.find_all(another_taxonomy_filter))

p_content = soup.find_all('p')
# print(p_content)

body_links = []
for p in p_content:
    body_links += p.find_all('a')

# print(body_links, '\n')

body_links = list(filter(lambda a: '#cite' not in a['href'], body_links))
# print(body_links, '\n')

links = {}
for a in body_links:
    links[a['title']] = a['href'] = 'https://en.wikipedia.org' + a['href']

# print(links, '\n')

imgs = soup.find_all('img')
# print(imgs)

# for i in imgs:
#     if 'class' in i.attrs:
#         print(i['class'])
#     else:
#         print(i)

imgs = list(filter(lambda img: 'class' in img.attrs, imgs))
imgs = list(filter(lambda img: img['class'][0] == 'mw-file-element', imgs))
for img in imgs:
    print(img['src'])

def download_image(url, path):
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)

img_path = "./html_docs/image.png"
if not os.path.exists(img_path):
    download_image('https:' + imgs[0]['src'], img_path)