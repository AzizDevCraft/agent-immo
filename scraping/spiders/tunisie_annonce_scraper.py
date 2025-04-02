import requests
from bs4 import BeautifulSoup
import time
import random
import json
import chardet 

num_page = 1
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
print (page.status_code)

def main (page) : 
    src = page.content  
    encoding_detected = chardet.detect(src)["encoding"]
    print(f"Encodage détecté : {encoding_detected}") 
    html_content = src.decode(encoding_detected, errors="replace")
    
    soup = BeautifulSoup (html_content, 'lxml')
    annonces = soup.find_all ("tr", {"class", "Tableau1"})
    
    def get_url_annonce (annonce) : 
        cellules = annonce.find_all ("td") 
        print (cellules [7])
        print ("------------------------------")
        print (cellules [9])
        
    
    get_url_annonce (annonces[0])
    
main (page)
    