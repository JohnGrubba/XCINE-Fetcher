import requests
import json
from requests.structures import CaseInsensitiveDict
from time import time

# Everything was done without bs4 because it was easier this way, since many variables hide in scripts.

url = "https://xcine.me/filme-minions-2015-26may-149-stream/deutsch"

start = time()
print("Initializing Request...")
r = requests.get(url)

episode_id = r.text[r.text.find(url, r.text.find('<a class="current"')):]
episode_id = episode_id[:episode_id.find(' title=')] \
                        .replace('" data-name="" data-episode-id="', '') \
                        .replace(url, "").replace('"', '')
if episode_id == "":
    print("Trying second method...")
    episode_id = r.text[r.text.find('data-episode-id="'):]
    episode_id = episode_id[:episode_id.find('" title=')]
    episode_id = episode_id.replace('data-episode-id="', '').replace('"', "")
episode_id = int(episode_id)
print("Extracted Episode ID: " + str(episode_id))
mov_id = r.text[r.text.find("var mov_id = "):]
mov_id = mov_id[:mov_id.find(";")]
mov_id = mov_id.replace("var mov_id = ", "").replace("'", '')
mov_id = int(mov_id)
print("Extracted Movie ID: " + str(mov_id))
dta = r.text[r.text.find('$( "#player-holder" ).load( "/movie/load-stream/" + movieData.id + "/" + episode_id + "?" + loadStreamSV, {'):r.text.find("}, function() {")].replace('$( "#player-holder" ).load( "/movie/load-stream/" + movieData.id + "/" + episode_id + "?" + loadStreamSV, {', "").strip()
dta = dta.replace(":", "=").replace(" ", "")
print("Extracted Payload: " + dta)

urlu = f"https://xcine.me/movie/load-stream/{mov_id}/{episode_id}?"
print("New Request URL: " + urlu)

headers = CaseInsensitiveDict()
headers["origin"] = "https://xcine.me"
headers["referer"] = url
headers["user-agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
headers["cookie"] = "PHPSESSID=292d28923a5d30fa0e92b6d780045fc4; SERVERID=s2; _ga=GA1.2.1624527310.1657262266; _gid=GA1.2.347900200.1657262266; __gads=ID=bbc2e18b5934d714-22dd94ddc6cd0005:T=1657262268:RT=1657262268:S=ALNI_MYahsW6BTHh6H3Lby_sf4qOC9t6Xw; _pop=1; dom3ic8zudi28v8lr6fgphwffqoz0j6c=c6f26fd6-afb2-4f61-8606-4d9e20e44371%3A1%3A1; _bRqwI=_0xc90"
headers["Content-Type"] = "application/x-www-form-urlencoded"

print("Fetching Streaming Links...")
resp = requests.post(urlu, headers=headers, data=dta)
jss = resp.text[resp.text.find("var vip_source = "):]
jss = jss[:jss.find(";")].replace("var vip_source = ", "")
jss = json.loads(jss)
print("Received JSON Response")
best = jss[0]["file"]
end = time()
for format in jss:
    if format["label"] == "1080p":
        best = format["file"]
        break
print("Validating Streaming URL...")
if requests.get(best, allow_redirects=False).status_code == 307:
    print("Successful gathering of Streaming URL")
    print("Took " + str(round(end - start, 2)) + " seconds")
    print(best)
else:
    print("Failed to gather Streaming URL")
    print("Failed in " + str(round(end - start, 2)) + " seconds")
    print(best)
