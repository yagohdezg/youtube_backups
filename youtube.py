import re
import requests
from queue import Queue, Empty
from workers import Worker
from threading import Thread
from bs4 import BeautifulSoup
from collections import OrderedDict
from urllib.parse import urlparse, urljoin
import time

class Extractor(object):
    def __init__(self, channel: str) -> None:
        # Constructor variables
        self.channel = channel
        
        # Other variables
        self.worker_queue = []
        self.work_scheme = lambda url, function: {
            "url": url,
            "function": function
        }
        self.workers = [Worker.start(self.worker_queue, self.videos)]
        self.videos = {}
        
    def verify_video(self, video_html: str) -> bool:
        channel = self.__get_segment(video_html, "ownerChannelName", ",", ",")
        channel = channel[0].replace('"ownerChannelName"', '')
        channel = re.search('(?<=")(.*?)(?=")', channel).group()
        
        return self.channel == channel
    
    def download_video(self, url: str):
        pass
        
    def __get_segment(self, text, key_string, limiter0, limiter1):
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
        
    def get_all_playlists():
        pass
    


ext = Extractor("Ryscu")
q = Queue()
data = {
        'url': 'https://www.youtube.com/watch?v=WmSxRUFDvcU',
        'function': ext.verify_video
        
    }
t = []
q.put(data)
worke = Worker(q, t)
worke.start()

print(1)
