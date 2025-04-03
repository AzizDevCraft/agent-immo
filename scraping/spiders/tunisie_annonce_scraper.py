import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import json
import chardet 

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
def main (page, count) : 
    src = page.content  
    
    encoding_detected = chardet.detect(src)["encoding"]
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
        print (f"annonce {count} recuperer avec succes !")
        count += 1
    
    with open ("data/raw/annonce-urls.json", 'w', encoding = 'utf-8') as file :
        json.dump (ancienne_data, file, indent = 4)

def extract_data (url, headers) : 
    page = requests.get (url, headers)
    src = page.content
    
    encoding_detected = chardet.detect(src)["encoding"]
    html_content = src.decode(encoding_detected, errors="replace")   
    
    soup = BeautifulSoup (html_content, 'lxml')
    if "Cette annonce est inexistante" not in soup.title.string :
        importent_sections = soup.find_all ("table", {"class" : "da_rub_cadre"})
        table_info = importent_sections [1].find_all ("tr")
        titre = table_info [1].contents[0].text # à ajouter dans le fichier json
        categorie = table_info [3].find_all ('a')[1:]
        nature_bien, type_bien = [_.text for _ in categorie] # à ajouter dans le fichier json
        localisation =  table_info [5].find_all ('a') [1:] 
        gouvernerat, municipalite, quartier = [_.text for _ in localisation] # à ajouter dans le fichier json
        data = {
            'titre' : titre, 
            'nature du bien' : nature_bien,
            'type de bien' : type_bien,
            'gouvernerat' : gouvernerat, 
            'municipalite' : municipalite, 
            'quartier' : quartier            
        }
        if table_info [7].contents[1].text == 'Adresse' :
            data [table_info [7].contents[1].text] = table_info [7].contents[3].text
            del table_info[7]
            del table_info[7]
        
        for _ in range (7, 12, 2) : 
            data [table_info [_].contents[1].text] = table_info [_].contents[3].text
        
        for _ in range (0, 3, 2) : 
            data [table_info [-2].find_all ('td') [_].text] = table_info [-2].find_all ('td') [_ + 1].text
            
        return data 
        
    
    else : 
        print ("cette annonce n'existe plus !")    
    section_photos = importent_sections [3]


       

if __name__ == "__main__" :
    count = -24
    # for num_page in range (1, 1032) :
    #     url = f"http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=TN&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num={num_page}"
    #     page = requests.get (url, headers)
    #     count += 25
    #     main (page, count)
    #     time.sleep(random.uniform (0.2, 1.8))
    #     tour = time.time ()
    #     print ("----------------------------------------------------")
    #     print ("Serie de 25 été ajouter avec succee ! ")
    #     print (f"temps passé {tour - debut}")
    #     print ("----------------------------------------------------")
    
    extract_data ("http://www.tunisie-annonce.com/DetailsAnnonceImmobilier.asp?cod_ann=3371741", headers)
    extract_data ("http://www.tunisie-annonce.com/DetailsAnnonceImmobilier.asp?cod_ann=3387860", headers)
    


