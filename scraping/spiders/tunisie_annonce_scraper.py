import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import json
import chardet 

num_page = 2
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/537.36"
]

headers = {
    'User-Agent' : random.choice (user_agents)
}
url = f"http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=TN&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num={num_page}"
page = requests.get (url, headers)

count = 1

def main (page) : 
    src = page.content  
    encoding_detected = chardet.detect(src)["encoding"]
    print(f"Encodage détecté : {encoding_detected}") 
    html_content = src.decode(encoding_detected, errors="replace")
    
    soup = BeautifulSoup (html_content, 'lxml')
    annonces = soup.find_all ("tr", {"class", "Tableau1"})
    
    try : 
        with open ("data/raw/annonce-urls.json", 'r', encoding = 'utf-8') as file : 
            ancienne_data = json.load (file)
    except FileNotFoundError : 
        ancienne_data = []
    
    def get_url_annonce (annonce) : 
        detail = {}
        cellules = annonce.find_all ("td") 
        url= f"http://www.tunisie-annonce.com/{cellules [7].contents[-2].get ("href")}"
        detail = {
            'site_web' : 'http://www.tunisie-annonce.com', 
            'url_annonce' : url, 
            'date_recup' : datetime.now().strftime("%Y-%m-%d")
        }
        
        return detail 
    
    
    for annonce in annonces : 
        ancienne_data.append (get_url_annonce (annonce))
        print (f"annonce {count} recuperer et ajouter avec succes !")
        count += 1
    
    with open ("data/raw/annonce-urls.json", 'w', encoding = 'utf-8') as file :
        json.dump (ancienne_data, file, indent = 4)

main (page)
    