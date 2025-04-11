import json 
import re 
import time 

def detect_erreur (obj) :
    if 'erreur' in obj.keys () or 'Surface' not in obj.keys () or "n.d" in obj ['Prix'].strip () :
        return False 
    elif surface (obj) < 10 :
        return False  
    return True

def extract_id (obj) : 
    id = int (re.search (r"\d+", obj ['titre']).group ())
    return id

def surface (obj) :
    space = re.search (r"[\d+\s*]*", obj ['Surface']).group ()
    convert_surface = int (''.join (space.split (' ')))
    return convert_surface

def prix (obj) :
    prx = re.search (r'[\d+\s*]+', obj ['Prix']).group ()
    prix_final = int (''.join (prx.split (' '))) 
    return prix_final

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
        
def update (obj : dict, id : int, surface : int, prix : int, contact : list) : 
    obj ['id'] = id 
    obj ['surface'] = surface
    obj ['prix'] = prix
    obj ['list_contact'] = contact
    
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
                new_obj = update (obj, extract_id (obj), surface (obj), prix (obj), contact (obj))
                if len (new_obj ["list_contact"]) != 0 : 
                    valide.append (new_obj)
                    print (f'id : {extract_id (obj)}')
            else : 
                print ("erreur")
                compteur_erreur += 1
            ct += 1

            
    with open ("data/processed/valid-version-1.json", "w", encoding='utf-8') as file : 
        json.dump (valide, file, indent=4)
        
    

    print (f'compteur_erreur : {compteur_erreur}')
    print (f'objet ajouter {len (valide)}')
    print (f'temps ecoulé : {str (time.time () - debut)[:5]}s')
    

