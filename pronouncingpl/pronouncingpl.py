import requests
import re

url = "https://www.rymer.org/4.0.1/search1.php"
r = requests.session()
rs= r.get(url)
print(rs.text)
cut = re.search(r'<form.+?id="login-form".+?<\/form>', rs.text, re.S|re.I).group()
form_key = re.search(r'name="form_key".+?value="(.+?)"', cut).group(1)
data = {'wpisz_slowo': 'elo',
        'LNG': 'pl',
        'form_key': form_key,
        'slownik': 'P',
        'minsyl': 1,
        'maxsyl': 5,
        'czemow': 'A',
        'ileLIT': 'slowo',
        'zjakichliter': 'ALL',
        'mozliweLIT': ''

        }
r = requests.post(url, data=data)
print(r.text)
