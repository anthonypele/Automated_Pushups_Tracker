import requests
#import json
import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator

Link = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(Link)

data = response.json()

db = pd.DataFrame(data)
db["t_len"] = db["title"].str.len()
db["num"] = np.random.randint(0, 11, size=100)

#print(response.status_code)

#print(db.columns)
#print(db.describe)
##print(db.iloc[5:10, 4:])

group = db.groupby("num")
#print(group.size()) 
#print(group["title"].count())

# как получить title  строки, где самое длинное body?
max_body_idx = db["body"].str.len().idxmax()
max_body = db["body"].str.len().max()
print(f"Самое длинное тело в строке номер {max_body_idx}, где {max_body} символов")

orig = db.loc[11, "title"]
translated = GoogleTranslator(source='auto', target='en').translate(orig)

db["tit_eng"] = db["title"].apply(lambda x: GoogleTranslator(source='auto', target='en').translate(x) if isinstance(x, str) else x)
print(db["tit_eng"])

##print(orig)
print(translated)
# что значит series и зачем он и почему я не использую - прям докопаться
# чем отличается loc & iloc