import os
import requests
from bs4 import BeautifulSoup

HEADER = "Blog\n\n\n\n\n\n\n\n\n\n\n\n\nMenu\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nBlog\n\n\n\n\n\n\n\n\n\n\n\n\nMenu\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
FOOTER = "The PyCon US 2024 conference in Pittsburgh, Pennsylvania, USA is a production of the Python Software Foundation"

url = "https://us.pycon.org/2024/schedule/talks/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

for link in soup.find_all('a'):
    href = link.attrs.get('href')

    if href is None or not href.startswith("/2024"):
        continue

    link_response = requests.get("https://us.pycon.org" + href)
    href = href.rstrip("/")

    if link_response.status_code >= 400:
        continue

    text_soup = BeautifulSoup(link_response.content, 'html.parser')

    text = text_soup.get_text()
    removed_menu = text.split(HEADER)[-1]
    actual_text = removed_menu.split(FOOTER)[0]
    final_text = actual_text.replace("\n", " ")

    filename = os.path.basename(href)
    with open(f"/workspaces/azure-search-openai-demo/data/{filename}.txt", 'w') as f:
        f.write(final_text)
