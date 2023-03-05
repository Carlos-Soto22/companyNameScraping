import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

#if you get 88640 code turn on VPN

start = time.time()
df = pd.read_csv("data.csv") #csv with company data must be named 'data.csv'
outdf = pd.DataFrame(columns=["Business Name", "URL"])
filterout = ["dnb", "facebook", "linkedin", "bbb", "buildzoom"] #list of websites/keywords to filter out

results = 1 #can select how many google search results to return / not working 100%
lower = 0 #lower index from data.csv to search
upper = 1000 #upper index

headers = { #Finder better / test for 429
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82",
}

for i in range(lower, upper):
    tdf = df.iloc[i, [4, 5, 6, 7, 8]]
    busName = tdf[0] #Additional info of company
    Addy = tdf[1]
    City = tdf[2]
    State = tdf[3]
    Zipcode = tdf[4]
    if str(City) == "nan":
        query = str(busName)
    else:
        query = str(busName) + " " + str(City)
    search = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={search}&num={results}"
    try:
        requests_results = requests.get(url)
        soup_link = BeautifulSoup(requests_results.content, "html.parser")
        up = False
        links = soup_link.find_all("a")
        for link in links:
            if up == False:
                link_href = link.get("href")
                if "url?q=" in link_href and not "webcache" in link_href:
                    title = link.find_all("h3")
                    if len(title) > 0:
                        s = link.get("href").split("?q=")[1].split("&sa=U")[0]
                        rem = False
                        up = False
                        if '86640' in s: #google too many request code
                            print('86640' + str(i))
                        for j in filterout:
                            if j in s:
                                rem = True
                        if rem == False:
                            if "https://www." in str(s):
                                s = s.replace("https://www.", "")
                            elif "http://www." in str(s):
                                s = s.replace("http://www.", "")
                            elif "https://" in str(s):
                                s = s.replace("https://", "")
                            else:
                                s = s.replace("http://", "")
                            up = True
                            outdf.loc[len(outdf.index)] = [busName, s.replace("/", "")]
        if up == False:
            s = "x"
            outdf.loc[len(outdf.index)] = [busName, s]
    except requests.exceptions.Timeout:
        print("Timeout occurred")
        print('Final:' + str(i))
    print(i)

outdf.to_csv("websitesv5.csv") #name of export csv is 'websitecsv5.csv'
print("done")
print(time.time() - start)
