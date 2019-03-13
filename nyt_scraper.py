import requests
import time


key = 'fPBRdiPMKv8E4lUH4knZ0EhzxzpuB3J8'

output = open('Data/nyt_2000-2018.csv', 'w', encoding='utf-8')
output.write('Date;Headline;Abstract;News Desk;Doc Type;Material Type;Lead Paragraph')

for year in range(2000, 2008):
    for month in range(1, 13):
        response = requests.get('https://api.nytimes.com/svc/archive/v1/' + str(year) + '/' + str(month) + '.json?api-key=' + key)
        json = response.json()

        docs = json['response']['docs']
        
        for article in docs:
            if 'main' in article['headline']:
                headline = article['headline']['main']
            else:
                headline = 'None'
            output.write(article['pub_date'] + ';' + headline + ';' + str(article['abstract']) + ';' + str(article['news_desk']) + ';' + article['document_type'] + ';' + article['type_of_material'] + ';' + str(article['lead_paragraph']) + '\n')

        print('done ' + str(month) + '/' + str(year))

        time.sleep(6)