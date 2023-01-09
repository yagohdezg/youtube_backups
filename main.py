import re
import os
import html
import json
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import OrderedDict

def parseForm(text):
    soup = BeautifulSoup(text, "html.parser")
    form = soup.find_all("form")[1]
    
    action = form.attrs["action"]
    
    inputs = {x.attrs["name"]: x.attrs["value"] for x in form.find_all("input")[:-1]}
    
    return action, inputs

def unescape(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), s)

def get_segment(text, key_string, limiter0, limiter1):
    results = []
    key_string_in_text = True
    
    while key_string_in_text:  
        if key_string not in text:
            key_string_in_text = False
            
        else:
            index0 = len(text) - text.find(key_string)
            index0 = len(text) - text[::-1].find(limiter0, index0)
            
            index1 = text.find(key_string)
            index1 = text.find(limiter1, index1 + 1)
        
            results.append(text[index0:index1])
            
            text = text[index1 + 1:]
    
    return results
    

session = requests.session()
# r = session.get("https://www.youtube.com/@miguel11mom/videos", cookies={"CONSENT": "YES+1"})

# First we get past cookies
cookies = session.get("https://www.youtube.com/@SuicideSheeep/featured")
url, data = parseForm(cookies.text)
featured_videos = session.post(url, data=data, headers={"Accept-Language": "en-US,en;q=0.5"})

# Now we get all the videos
play_all_url = get_segment(featured_videos.text, "\\u0026list=", '"', '"')
play_all_url = [urljoin("https://www.youtube.com", unescape(x)) for x in play_all_url]

play_all_playlist = session.get(play_all_url[0])

videos = get_segment(play_all_playlist.text, "/watch?v=", '"', '"')
videos = list(OrderedDict.fromkeys(videos))
videos = [x for x in videos if re.search("index=\d+$", x)]
videos = [unescape(x) for x in videos]

for i in videos:
    print(i)


with open("test.html", "w+") as file:
    file.write(play_all_playlist.text)

