# -*-coding:UTF-8-*-
import urllib.request
import json
from bs4 import BeautifulSoup

html_json = urllib.request.urlopen(
    "http://127.0.0.1:25000/api/news/11").read().decode('utf-8')
json_html = json.loads(html_json)
soup = BeautifulSoup(json_html['content'], 'lxml')
print(soup.string)
content_array = soup.find_all('p')
image_arrar = []
index = 0
content = ''
for element in content_array:
    if element.string:
        content += element.string + "\\n\\t"
    elif element.img:
        content += '[IMG-' + str(index) + "]\\n\\t"
        index = index + 1
        # image_arrar.append(element.img['src'])
        print(element.img['src'])

# print(content)
# print(image_arrar)
