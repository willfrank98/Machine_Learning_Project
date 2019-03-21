from dateutil.parser import parse
import pytz
import queue
#from datetime import datetime
# from sys import exit

utc = pytz.UTC
years = '2000-2015'
desk = 'busfin' # business/financial desk
news_input_list = list(open('Data/nyt_' + desk + '_' + years + '.csv', encoding="utf-8"))
# news_input_list.reverse()
stock_list = open("Data/^DJI.csv")
stock_list.readline()
# stock_list.readline()

output = open('Data/combined_' + desk + '_' + years + '.csv', "w", encoding="utf-8")
output.write("Date;LabelCategorical;LabelRegression;PrevDay;Prev5Day;Prev10Day;Text;Polarity;Subjectivity")

prevDayQueue = queue.Queue()
prev5DayQueue = queue.Queue()
prev10DayQueue = queue.Queue()

i = 1
for line in stock_list:
    stock_day = line.split(',')
    if stock_day[1] == 'null':
        continue
    stock_date = stock_day[0]
    diff = float(stock_day[4]) - float(stock_day[1])
    diffCat = 1 if diff >= 0 else -1
    headlines = ""

    while True:
        news_item = news_input_list[i].split(';')
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
        news_date = parse(news_item[0])
        if news_date.strftime('%Y-%m-%d') == stock_date:
            headline =  " ".join(news_item[1].split()) + '. '
            headlines += headline
            i += 1
        else:
            break

    if not prevDayQueue.empty():
        prevDay = float(stock_day[1]) - float(prevDayQueue.get())
    else:
        prevDay = None

    if prev5DayQueue.qsize() > 4:
        prev5Day = float(stock_day[1]) - float(prev5DayQueue.get())
    else:
        prev5Day = None

    if prev10DayQueue.qsize() > 9:
        prev10Day = float(stock_day[1]) - float(prev10DayQueue.get())
    else:
        prev10Day = None

    output.write(stock_date + ';' + str(diffCat) + ';' + str(prevDay) + ';' + str(prev5Day) + ';' + str(prev10Day) + ';' + headlines + '\n')

    prevDayQueue.put(stock_day[1])
    prev5DayQueue.put(stock_day[1])
    prev10DayQueue.put(stock_day[1])
    
print('done!')