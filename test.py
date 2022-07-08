from xcine import xcineAPI

api = xcineAPI(cookie="_ga=GA1.2.1429829834.1657132748; _gid=GA1.2.10807337.1657132748; PHPSESSID=cc46b5f5fab9cf477c2705c614a4f869; SERVERID=s2; _pop=1; _SdrT5=_0xc76; _gat_gtag_UA_144665518_1=1", debug=False)
print(api.search("Phineas and Ferb"))
print(api.get_stream("https://xcine.me/serien-disney-phineas-und-ferb-8450-stream/folge-9"))