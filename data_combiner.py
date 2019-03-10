from dateutil.parser import parse
#from datetime import datetime
# from sys import exit

news_input_list = list(open("Data/business_news.csv", encoding="utf-8"))
news_input_list.reverse()
stock_list = open("Data/^DJI.csv")
stock_list.readline()
# stock_list.readline()

output = open("Data/combined_data_us2.csv", "w", encoding="utf-8")
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
        news_item = news_input_list[i].split(',')
        if i == len(news_input_list) - 1:
            exit(0)
        news_date = parse(news_item[0])
        p_date = parse(stock_date)
        if news_date < p_date:
            i += 1
        else:
            break

    if news_date > p_date:
        continue

    while True:
        news_item = news_input_list[i].split(',')
        if i == len(news_input_list) - 1:
            exit(0)
        news_date = parse(news_item[0])
        if news_date.strftime('%Y-%m-%d') == stock_date:
            headline =  " ".join(news_item[1].split()) + ';'
            headlines += headline
            i += 1
        else:
            break

    output.write(stock_date + ',' + str(diff) + ',' + headlines + '\n')
    

