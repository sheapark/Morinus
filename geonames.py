import json
import urllib.parse
import urllib.request

class Geonames:
    NAME, LON, LAT, COUNTRYCODE, COUNTRYNAME, ALTITUDE, GMTOFFS = range(0, 7)
    username = 'bibliotecaastrologia'
    langs = ("en", "hu", "it", "fr", "ru", "es")

    def __init__(self, city, maxnum, langid):
        if isinstance(city, bytes):
            city = city.decode("utf-8")
        self.city = city
        self.maxnum = maxnum
        self.langid = langid
        self.li = None

    def fetch_values_from_page(self, url, params, key):
        try:
            url = url % urllib.parse.urlencode(params)
            with urllib.request.urlopen(url, timeout=15) as page:
                doc = json.loads(page.read().decode("utf-8"))
            values = doc.get(key, None)
        except Exception as e:
            print("GeoNames error:", e)
            values = None
        return values

    def get_basic_info(self, city):
        url = "http://api.geonames.org/searchJSON?%s"
        lang = Geonames.langs[self.langid] if 0 <= self.langid < len(Geonames.langs) else "en"
        params = {"username": self.username, "lang": lang, "q": city,
                  "featureClass": "P", "maxRows": self.maxnum}
        return self.fetch_values_from_page(url, params, "geonames")

    def get_gmt_offset(self, longitude, latitude):
        url = "http://api.geonames.org/timezoneJSON?%s"
        params = {"username": self.username, "lng": longitude, "lat": latitude}
        return self.fetch_values_from_page(url, params, "rawOffset")

    def get_elevation(self, longitude, latitude):
        url = "http://api.geonames.org/astergdemJSON?%s"
        params = {"username": self.username, "lng": longitude, "lat": latitude}
        return self.fetch_values_from_page(url, params, "astergdem")

    def get_location_info(self):
        info = self.get_basic_info(self.city)
        if not info:
            return False
        self.li = []
        for it in info:
            longitude = it.get("lng", 0)
            latitude = it.get("lat", 0)
            gmt_offset = self.get_gmt_offset(longitude, latitude)
            if gmt_offset is None:
                gmt_offset = 0.0
            elevation = self.get_elevation(longitude, latitude)
            if elevation is None or elevation < 0:
                elevation = 0
            self.li.append((it.get("name", ""), float(longitude), float(latitude),
                            it.get("countryCode", ""), it.get("countryName", ""),
                            elevation, float(gmt_offset)))
        return True
