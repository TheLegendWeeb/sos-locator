import requests
from bs4 import BeautifulSoup
import shutil
import os
import time
import string

def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

def download_img(url,file_name,folder_name):
    r=requests.get(url,stream=True)
    folder_name=format_filename(folder_name)
    if r.status_code==200:
        os.makedirs(os.path.dirname("downloads/{}/".format(folder_name)), exist_ok=True)
        while not os.path.exists("downloads/{}/".format(folder_name)):
            pass
        with open("downloads/{}/{}.jpg".format(folder_name,file_name),"wb") as f:
            f.raw.decode_content= True
            shutil.copyfileobj(r.raw,f)

code=str(input("Sauce? "))
link="https://nhentai.net/g/{}".format(code)
first_page_link="https://nhentai.net/g/{}/1/".format(code)


response= requests.get(link)
if response.status_code == 200:
    print("Sauce located")
elif response.status_code == 404:
    print("Not found")

soup=BeautifulSoup(response.text,'html.parser')

title=soup.title.string.replace(" » nhentai: hentai doujinshi and manga","")
tags=[]

for tag in soup.find_all("meta"):
    try:
        if tag["name"]=="twitter:description":
            tags = tag["content"].split(",")
    except KeyError:
        pass

print("Title: "+title)
print("Tags: "+", ".join(tags))

response=requests.get(first_page_link)
soup=BeautifulSoup(response.text,'html.parser')

pages=0
for tag in soup.find_all("span"):
    try:
        if tag["class"][0]=="num-pages":
            pages=int(tag.string)
            break
    except KeyError:
        pass

print("Nr pages: " + str(pages))

query=str(input("Do you want to download (n/Y)"))
if query in ["y","yes","Y","YES",""]:
    print("Starting download...")
    for page_nr in range(1,pages+1):
        response=requests.get("https://nhentai.net/g/{}/{}/".format(code,page_nr))
        soup=BeautifulSoup(response.text,'html.parser')
        for tag in soup.find_all("img"):
            try:
                if tag["src"].startswith("https://i.nhentai.net/galleries/"):
                    download_img(tag["src"],page_nr,title)
                    print(page_nr)
            except KeyError:
                pass
else:
    print("Canceled download...")