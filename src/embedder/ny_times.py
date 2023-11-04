import requests

base_url = '''
https://api.nytimes.com/svc/archive/v1/[YEAR]/[MONTH].json?api-key=[KEY]
'''


class times_api:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_articles_of_date(self, year, month):
        url = base_url.replace('[YEAR]', str(year)).replace('[MONTH]', str(month)).replace('[KEY]', self.api_key) 
        r = requests.get(url)
        status = r.status_code
        articles = []
        if(status == 200):
            j = r.json()
            docs = j['response']['docs']
            for doc in docs:
                articles.append(doc)
        return articles
