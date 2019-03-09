from dateutil.parser import parse
#from datetime import datetime
# from sys import exit

news_input_list = list(open("Data/economic_news.csv", encoding="utf-8"))
news_input_list.reverse()
stock_list = open("Data/^DJI.csv")
stock_list.readline()
# stock_list.readline()

output = open("Data/combined_data_us.csv", "w", encoding="utf-8")
output.write("Date,Label,Headlines\n")

i = 1
for line in stock_list:
    data = line.split(',')
    if data[1] == 'null':
        continue
    date = data[0]
    diff = float(data[4]) - float(data[1])
    diff = 1 if diff > 0 else -1
    headlines = ""

    while True:
        news = news_input_list[i].split(',')
        if i == len(news_input_list) - 1:
            exit(0)
        news_date = parse(news[0])
        p_date = parse(date)
        if news_date < p_date:
            i += 1
        else:
            break

    if news_date > p_date:
        continue

    while True:
        news = news_input_list[i].split(',')
        if i == len(news_input_list) - 1:
            exit(0)
        news_date = parse(news[0])
        if news_date.strftime('%Y-%m-%d') == date:
            headline =  " ".join(news[1].split()) + ';'
            headlines += headline
            i += 1
        else:
            break

    output.write(date + ',' + str(diff) + ',' + headlines + '\n')
    

