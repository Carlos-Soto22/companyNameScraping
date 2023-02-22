from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


start = time.perf_counter()
df = pd.read_csv('data.csv')

headers = {
	'Accept' : '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
}

outdf = pd.DataFrame(columns=['Business Name', 'URL'])

for i in range(100):
    tdf = df.iloc[i, [4,5,6,7,8]]
    busName = tdf[0]
    Addy = tdf[1]
    City = tdf[2]
    State = tdf[3]
    Zipcode = tdf[4]
    if str(City) == 'nan':
        query = str(busName)
    else:
        query = str(busName) + ' ' + str(City)
    url = 'https://www.google.com/search?q='
    req = requests.get(url, headers = headers, params = {'q': query})
    content = req.text
    soup = BeautifulSoup(content, 'html.parser')
    search = soup.find(id = 'search')
    url = search.find('a')['href']
    outdf.loc[len(outdf.index)] = [busName, url]


'''
if dnb, linkedin, facebook in links
remove
'''

outdf.to_csv('OutputBusinessURLs.csv')
end = time.perf_counter()
print('done')
print(end-start)
