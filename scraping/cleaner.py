import json 
import re 

count = 1
with open ("data/raw/annonces-data.ndjson", "r", encoding='utf-8') as file : 
    lines = file.readlines ()

buffer = ""
fixed_data = []

for line in lines : 
    buffer += line.strip ()
    try : 
        obj = json.loads (buffer)
        fixed_data.append (obj)
        buffer = ""
    except json.JSONDecodeError : 
        continue 
    
with open ("data/raw/annonces-data.ndjson", "w", encoding='utf-8') as file : 
    for _ in fixed_data : 
        file.write (json.dumps (_) + '\n')