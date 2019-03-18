from dateutil.parser import parse
import pytz
#from datetime import datetime
# from sys import exit

utc = pytz.UTC

news_input_list = list(open("Data/nyt_2000-2010.csv", encoding="utf-8"))
news_input_list.reverse()
stock_list = open("Data/^DJI.csv")
stock_list.readline()
# stock_list.readline()

output = open("Data/nyt_combined_headlines_2000-2010.csv", "w", encoding="utf-8")
output.write("Date,Label,Headlines\n")

i = 1
for line in stock_list:
    stock_day = line.split(',')
    if stock_day[1] == 'null':
        continue
    stock_date = stock_day[0]
    diff = float(stock_day[4]) - float(stock_day[1])
    diff = 1 if diff >= 0 else -1
    headlines = ""

    while True:
        news_item = news_input_list[i].split(';')
        if news_item[0] == '\n':
            i += 1
            continue
        if i == len(news_input_list) - 1:
            exit(0)
        news_date = parse(news_item[0]).replace(tzinfo=utc)
        p_date = parse(stock_date).replace(tzinfo=utc)
        if news_date < p_date:
            i += 1
        else:
            break

    if news_date > p_date:
        continue

    while True:
        if i == len(news_input_list) - 1:
            exit(0)
        news_item = news_input_list[i].split(';')
        if len(news_item) < 7:
            i += 1
            continue
        elif news_item[3] != 'business/financial desk':
            i += 1
            continue
        news_date = parse(news_item[0])
        if news_date.strftime('%Y-%m-%d') == stock_date:
            headline =  " ".join(news_item[1].split()) + ';'
            if headline == 'None':
                i += 1
                continue
            headlines += headline
            i += 1
        else:
            break

    output.write(stock_date + ',' + str(diff) + ',' + headlines + '\n')
    

