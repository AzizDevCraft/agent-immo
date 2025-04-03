from spiders.tunisie_annonce_scraper import extract_data 
import json 
import random
import time

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/537.36"
]

headers = {
    'User-Agent' : random.choice (user_agents)
}

debut = time.time ()

with open ('data/raw/annonces-url.json', 'r') as file : 
    data = json.load (file)

data_list = []
for _ in range (500) : 
    data_list.append (extract_data (data [_]["url_annonce"], headers))
    print (f"annonce {_ + 1} cb scrape !")

with open ('data/raw/annonces-data.json', 'w') as file : 
    json.dump (data_list, file, indent=4)   
 
print (f'temps ecoule : {(time.time () - debut)/60} min')
