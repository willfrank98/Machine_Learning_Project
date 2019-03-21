import requests
import time


key = 'fPBRdiPMKv8E4lUH4knZ0EhzxzpuB3J8'

t0 = time.time() - 6
for year in range(1990, 2000):
    output = open('Data/NYT/nyt_' + str(year) + '.csv', 'w', encoding='utf-8')
    output.write('Date;Headline;Abstract;News Desk;Doc Type;Material Type;Lead Paragraph\n')
    for month in range(1, 13):
        # restricts calls to once every 6 seconds
        while time.time() - 6.01 < t0:
            pass
        response = requests.get('https://api.nytimes.com/svc/archive/v1/' + str(year) + '/' + str(month) + '.json?api-key=' + key)
        t0 = time.time()
        json = response.json()

        docs = json['response']['docs']
        
        for article in docs:
            if 'main' in article['headline']:
                headline = article['headline']['main']
            else:
                headline = 'None'
            date = article['pub_date']
            headline = ' '.join(headline.split()).replace(';', ',').lower()
            if 'abstract' in article:
                abstract = ' '.join(str(article['abstract']).split()).replace(';', ',').lower()
            else:
                abstract = 'None'
            if 'news_desk' in article:
                news_desk = ' '.join(str(article['news_desk']).split()).replace(';', ',').lower()
            else:
                news_desk = 'None'
            doc_type = ' '.join(str(article['document_type']).split()).replace(';', ',').lower()
            if 'type_of_material' in article:
                mat_type = ' '.join(str(article['type_of_material']).split()).replace(';', ',').lower()
            else:
                mat_type = 'None'
            if 'lead_paragraph' in article:
                lead_paragraph = ' '.join(str(article['lead_paragraph']).split()).replace(';', ',').lower()
            else:
                lead_paragraph = ' '.join(str(article['snippet']).split()).replace(';', ',').lower()
            output.write(date + ';' + headline + ';' + abstract + ';' + news_desk + ';' + doc_type + ';' + mat_type + ';' + lead_paragraph + '\n')

        print('done ' + str(month) + '/' + str(year))