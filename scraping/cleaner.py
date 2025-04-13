import json 
import re 
import time 
from typing import Union


def detect_erreur (obj) :
    if 'erreur' in obj.keys () or 'Surface' not in obj.keys () or "n.d" in obj ['Prix'].strip () :
        return False 
    elif surface (obj) < 10 :
        return False  
    return True

def extract_id (obj) : 
    id_position = re.search (r"\d+", obj ['titre']).span ()
    id = int(obj ['titre'][id_position[0] : id_position[1]])
    obj ['titre'] = obj ['titre'][id_position[1]+2 :]
    return id

def surface (obj) :
    space = re.search (r"[\d+\s*]*", obj ['Surface']).group ()
    convert_surface = int (''.join (space.split (' ')))
    return convert_surface

def prix (obj) :
    prx = re.search (r'[\d+\s*]+', obj ['Prix']).group ()
    prix_final = int (''.join (prx.split (' '))) 
    return prix_final

def nb_chambres (obj) :
    recherche =  re.search (r"s\s*\+?\s*\d{1}", obj ['titre'], re.IGNORECASE)
    if recherche : 
        return int (recherche.group () [-1])
    elif re.search (r"s\s*\+*\s*\d{1}", obj ['Texte'], re.IGNORECASE) : 
        recherche2 = re.search (r"s\s*\+*\s*\d{1}", obj ['Texte'], re.IGNORECASE).group ()
        return int (recherche2 [-1])
    else : 
        if re.search (r"\d", obj ['type de bien']) : 
            return re.search (r"\d", obj ['type de bien']).group ()
        return None 

def is_meuble (obj) : 
    recherche = re.search (r'(non|pas)[-\s]?meubl[eé]', obj ['titre'], re.IGNORECASE)
    if recherche or re.search (r'(non|pas)[-\s]?meubl[eé]', obj ['Texte'], re.IGNORECASE): 
        return False
    elif re.search (r'meubl[eé]', obj ['Texte'], re.IGNORECASE) or re.search (r'meubl[eé]', obj ['titre'], re.IGNORECASE) :
        return True 
    else : 
        return None

def contact (obj : dict) -> list : 

    contact_list = []
    
    def uni_forme (numero : str) -> int : 
        try : 
            if 10 < len (numero) <= 15 : 
                return int ("".join (numero[4:].split (' ')))
            elif  len (numero) < 10: 
                return int ("".join (numero.split (' ')))
        except ValueError : 
            return None
    
    def none_eliminator (l): 
        _ = 0
        while _ < len (l) :  
            if l [_] == None : 
                del l[_]
            _ += 1
        return l   
        
    if 'Tél : ' in obj.keys () : 
        contact_list.append (uni_forme (obj['Tél : ']))
        del obj['Tél : ']
        
    if 'Mob : ' in obj.keys () : 
        contact_list.append (uni_forme (obj ['Mob : ']))
        del obj ['Mob : ']
        
    if 'Fax : ' in obj.keys () :  
        contact_list.append (uni_forme (obj ['Fax : ']))
        del obj ['Fax : ']
    
    list_final = none_eliminator (list(set(contact_list)))
    return list_final
        
def update (obj : dict, id : int, surface : int, prix : int, contact : list, nb_chambres : int, is_meuble : Union [bool | None]) : 
    obj ['id'] = id 
    obj ['surface'] = surface
    obj ['prix'] = prix
    obj ['list_contact'] = contact
    obj ['nb_chambres'] = nb_chambres
    obj ['meuble'] = is_meuble
    
    del obj ['Prix']
    del obj ['Surface']
    del obj ["Mail : "]
        
    return obj           

if __name__ == "__main__" : 
    debut = time.time ()
    compteur_erreur = 0
    ct = 0
    valide = []
    with open ("data/raw/annonces-data.ndjson", 'r', encoding='utf-8') as file : 
        for line in file :
            obj = json.loads (line)
            print (f"-------------------- annonce n°{ct} ------------------------------")
            if detect_erreur (obj) :
                new_obj = update (obj, extract_id (obj), surface (obj), prix (obj), contact (obj), nb_chambres (obj), is_meuble (obj))
                if len (new_obj ["list_contact"]) != 0 : 
                    valide.append (new_obj)
                else : 
                    compteur_erreur += 1
            else : 
                print ("erreur")
                compteur_erreur += 1
            ct += 1

            
    with open ("data/processed/valid-version-1.json", "w", encoding='utf-8') as file : 
        json.dump (valide, file, indent=4)
        
    

    print (f'compteur_erreur : {compteur_erreur}')
    print (f'objet ajouter {len (valide)}')
    print (f'temps ecoulé : {str (time.time () - debut)[:4]}s')

