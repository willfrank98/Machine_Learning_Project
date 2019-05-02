import requests
import time
import re
from unidecode import unidecode


def cleanse(string):
    string = str(string)
    if '&#' in string:
        matches = regex.findall(string)
        new_matches = []
        for i in range(len(matches)):
            if matches[i][0] != 'x':
                new_matches.append(chr(int(matches[i])))
            else:
                new_matches.append(chr(int(matches[i][1:], 16)))
            matches[i] = '&#' + matches[i] + ';'

        for i in range(len(matches)):
            string = string.replace(matches[i], new_matches[i])

        string = unidecode(string)

    stripped = ''.join([c for c in string if 0 < ord(c) < 127])
    return ' '.join(stripped.split()).replace(';', ',').lower()


key = 'API_KEY_HERE'
regex = re.compile(r'&#(?!\s)((?:(?!;).)*)(?<!\s);')
regex2 = re.compile(r'&#.{1,4},')

t0 = time.time() - 6
for year in range(2005, 2019):
    output = open('Data/NYT/nyt_' + str(year) + '.csv', 'w')
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
                headline = cleanse(article['headline']['main'])
            else:
                headline = 'None'
            date = article['pub_date']
            if 'abstract' in article:
                abstract = cleanse(article['abstract'])
            else:
                abstract = 'None'
            if 'news_desk' in article:
                news_desk = cleanse(article['news_desk'])
            else:
                news_desk = 'None'
            doc_type = cleanse(article['document_type'])
            if 'type_of_material' in article:
                mat_type = cleanse(article['type_of_material'])
            else:
                mat_type = 'None'
            if 'lead_paragraph' in article:
                lead_paragraph = cleanse(article['lead_paragraph'])
            else:
                lead_paragraph = cleanse(article['snippet'])

            output.write(date + ';' + headline + ';' + abstract + ';' + news_desk + ';' + doc_type + ';' + mat_type + ';' + lead_paragraph + '\n')

        print('done ' + str(month) + '/' + str(year))