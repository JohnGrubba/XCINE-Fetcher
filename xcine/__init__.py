import requests
import json
from requests.structures import CaseInsensitiveDict
from time import time

class xcineAPI:
    def __init__(self, debug=True, cookie=None) -> None:
        self.debug = debug
        self.cookie = cookie

    def search(self, query: str) -> dict:
        """Searches xcine and returns a list of films

        Args:
            query (str): Search Query

        Returns:
            dict: JSON Response from xcine
        """
        r = requests.post("https://xcine.me/search", data=f"key={query}&getInfo=1", headers={"Content-Type": "application/x-www-form-urlencoded"}).json()
        return r

    def get_stream(self, url: str) -> None:
        """
        Gets a Download Link for your Movie
        """
        start = time()
        if self.debug: print("Initializing Request...")
        r = requests.get(url)

        episode_id = r.text[r.text.find(url, r.text.find('<a class="current"')):]
        episode_id = episode_id[:episode_id.find(' title=')] \
                                .replace('" data-name="" data-episode-id="', '') \
                                .replace(url, "").replace('"', '')
        if episode_id == "":
            if self.debug: print("Trying second method...")
            episode_id = r.text[r.text.find('data-episode-id="'):]
            episode_id = episode_id[:episode_id.find('" title=')]
            episode_id = episode_id.replace('data-episode-id="', '').replace('"', "")
        episode_id = int(episode_id)
        if self.debug: print("Extracted Episode ID: " + str(episode_id))
        mov_id = r.text[r.text.find("var mov_id = "):]
        mov_id = mov_id[:mov_id.find(";")]
        mov_id = mov_id.replace("var mov_id = ", "").replace("'", '')
        mov_id = int(mov_id)
        if self.debug: print("Extracted Movie ID: " + str(mov_id))
        dta = r.text[r.text.find('$( "#player-holder" ).load( "/movie/load-stream/" + movieData.id + "/" + episode_id + "?" + loadStreamSV, {'):r.text.find("}, function() {")].replace('$( "#player-holder" ).load( "/movie/load-stream/" + movieData.id + "/" + episode_id + "?" + loadStreamSV, {', "").strip()
        dta = dta.replace(":", "=").replace(" ", "")
        if self.debug: print("Extracted Payload: " + dta)

        urlu = f"https://xcine.me/movie/load-stream/{mov_id}/{episode_id}?"
        if self.debug: print("New Request URL: " + urlu)

        headers = CaseInsensitiveDict()
        headers["origin"] = "https://xcine.me"
        headers["referer"] = url
        headers["user-agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
        headers["cookie"] = self.cookie
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        if self.debug: print("Fetching Streaming Links...")
        resp = requests.post(urlu, headers=headers, data=dta)
        jss = resp.text[resp.text.find("var vip_source = "):]
        jss = jss[:jss.find(";")].replace("var vip_source = ", "")
        jss = json.loads(jss)
        if self.debug: print("Received JSON Response")
        best = jss[0]["file"]
        end = time()
        for format in jss:
            if format["label"] == "1080p":
                best = format["file"]
                break
        if self.debug: print("Validating Streaming URL...")
        if requests.get(best, allow_redirects=False).status_code == 307:
            if self.debug: print("Successful gathering of Streaming URL")
            if self.debug: print("Took " + str(round(end - start, 2)) + " seconds")
            if self.debug: print(best)
            return best
        else:
            if self.debug: print("Failed to gather Streaming URL")
            if self.debug: print("Failed in " + str(round(end - start, 2)) + " seconds")
            return None
