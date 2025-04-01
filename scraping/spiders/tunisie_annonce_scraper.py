import requests
from bs4 import BeautifulSoup
import time

valid_codes = []
 
for num_annonce in range (3302000, 3303001) : 
    time.sleep (0.1)
    page =  requests.get (f"http://www.tunisie-annonce.com/DetailsAnnonceImmobilier.asp?cod_ann={num_annonce}")
    src = page.content
    soup = BeautifulSoup (src, "lxml")
    if "Cette annonce est inexistante" not in soup.title.string :
        valid_codes.append (num_annonce)  
            
print (f"annonce trouve : {len(valid_codes)}") # 28
print ("-------------------------------------")
print (valid_codes)

with open ("temporaire.txt", 'w') as file : 
    for code in valid_codes : 
        file.write (f"{code} \n")

# valid_codes = [[3302198, 3302296, 3302311, 3302332, 3302336, 3302339, 3302342, 3302366, 3302370, 3302381, 3302424, 3302510, 3302552, 3302570, 3302572, 3302604, 3302628, 3302694, 3302707, 3302709, 3302735, 3302751, 3302764, 3302923, 3302926, 3302931, 3302938, 3303000]]