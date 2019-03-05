import pandas as pd
from dateutil.parser import parse

business = open("business_news.csv")
business.readline()
economic = list(open("economic_news.csv", encoding="utf-8"))
economic.reverse()
#economic.readline()
DJIA = open("^DJI.csv")
DJIA.readline()

output = open("combined_data.csv", "w", encoding="utf-8")
output.write("Date,DJIAChange,Headlines\n")

i = 0
for line in DJIA:
    data = line.split(',')
    date = data[0]
    diff = float(data[4]) - float(data[1])
    diff = 1 if diff > 0 else -1
    headlines = ""

    while True:
        news = economic[i].split(',')
        if news[0] == 'Timestamp':
            break
        news_date = parse(news[0])
        if news_date.strftime('%Y-%m-%d') != date:
            i += 1
        else:
            break

    if news[0] == 'Timestamp':
            break

    while True:
        news = economic[i].split(',')
        news_date = parse(news[0])
        if news_date.strftime('%Y-%m-%d') == date:
            headlines += news[1] + ';'
            i += 1
        else:
            break

    output.write(date + ',' + str(diff) + ',' + headlines + '\n')
    

