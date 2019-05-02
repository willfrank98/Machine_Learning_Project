from dateutil.parser import parse
from pytz import UTC
import queue
from textblob import TextBlob

years = '2010-2018'
desk = 'busfin' # business/financial desk
news_input_list = list(open('Data/nyt_' + desk + '_' + years + '.csv'))
DJI_list = list(open("Data/^DJI.csv"))[1:]

output = open('Data/combined_' + desk + '_' + years + '.csv', "w")
output.write("Date;Label;prev1Day;prev2Day;prev3Day;prev4Day;prev5Day;prev6Day;prev7Day;prev8Day;prev9Day;prev10Day;prevVolume;PrevHigh;PrevLow;MCD;WBA;MRK;AAPL;MMM;BA;JNJ;MSFT;IBM;CVX;UTX;TRV;JPM;CSCO;GS;NKE;KO;PFE;V;VZ;HD;AXP;WMT;DIS;XOM;CAT;PG;UNH;INTC;Text\n")

ticker_list = ['MCD', 'WBA', 'MRK', 'AAPL', 'MMM', 'BA', 'JNJ', 'MSFT', 'IBM', 'CVX', 'UTX', 'TRV', 'JPM', 'CSCO', 'GS', 'NKE', 'KO', 'PFE', 'V', 'VZ', 'HD', 'AXP', 'WMT', 'DIS', 'XOM', 'CAT', 'PG', 'UNH', 'INTC']
stocks_list = []
for ticker in ticker_list:
    stocks_list.append(list(open('Data/Stocks/' + ticker + '.csv'))[1:])

prevDayLine = queue.Queue()

djiPrevDays = [queue.Queue() for _ in range(10)]

stocksPrevDays = [queue.Queue() for _ in range(len(ticker_list))]
stockLineTrackers = dict(zip(ticker_list, [0 for _ in range(len(stocks_list))]))

news_line_counter = 1
# iterates based on stock market days
for line in range(len(DJI_list)):
    stock_day = DJI_list[line].split(',')
    if stock_day[1] == 'null':
        continue
    stock_date = stock_day[0]
    diff = float(stock_day[4]) - float(stock_day[1])
    diffCat = 1 if diff >= 0 else 0

    # iterates through news articles until they catch up to next stock market day date
    while True:
        news_item = news_input_list[news_line_counter].split(';')
        if news_line_counter == len(news_input_list) - 1:
            print('done!')
            exit(0)
        news_date = parse(news_item[0][:10]).replace(tzinfo=UTC)
        p_date = parse(stock_date).replace(tzinfo=UTC)
        if news_date < p_date:
            news_line_counter += 1
        else:
            break

    # gathers information about performance over the past x days
    prevDays = ''
    for i in range(len(djiPrevDays)):
        if djiPrevDays[i].qsize() > i:
            prevDays += str((float(stock_day[1]) - float(djiPrevDays[i].get()))/float(stock_day[1])) + ';'
        else:
            prevDays += 'None' + ';'

    for i in range(len(djiPrevDays)):
        djiPrevDays[i].put(stock_day[1])

    # stores info about previous day's high, low, and trade volume
    if prevDayLine.qsize() > 0:
        prevLine = prevDayLine.get()
        prevHighAdj = str(float(prevLine[2])/float(prevLine[1]))
        prevLowAdj = str(float(prevLine[2])/float(prevLine[1]))
        prevLine = prevLine[6].strip() + ';' + prevHighAdj + ';' + prevLowAdj + ';'
    else:
        prevLine = 'None' + ';'

    prevDayLine.put(stock_day)

    # previous 10 day's performance of the 29 stocks (excluding DOW) that make up DJIA
    stocks = ''
    for i in range(len(stocksPrevDays)):
        if stocksPrevDays[i].qsize() > 9:
            stocks += str((float(stocks_list[i][stockLineTrackers[ticker_list[i]]][1]) - float(stocksPrevDays[i].get()))/float(stock_day[1])) + ';'
        else:
            stocks += 'None' + ';'

    for i in range(len(stocksPrevDays)):
        ticker_split = stocks_list[i][stockLineTrackers[ticker_list[i]]].split(',')
        ticker_date = parse(ticker_split[0]).replace(tzinfo=UTC)
        while ticker_date < p_date:
            stockLineTrackers[ticker_list[i]] += 1
            ticker_split = stocks_list[i][stockLineTrackers[ticker_list[i]]].split(',')
            ticker_date = parse(ticker_split[0]).replace(tzinfo=UTC)
        if ticker_date == p_date:
            stocksPrevDays[i].put(ticker_split[1])
            stockLineTrackers[ticker_list[i]] += 1

    # skips stock day lines until they catch up to next news day
    if news_date > p_date:
        continue

    # iterates every news article in one day
    headlines = ""
    while True:
        if news_line_counter == len(news_input_list) - 1:
            print('done!')
            exit(0)
        news_item = news_input_list[news_line_counter].split(';')
        news_date = parse(news_item[0])
        if news_date.strftime('%Y-%m-%d') == stock_date:
            headline =  " ".join(news_item[1].split()) + '. '
            headlines += headline
            news_line_counter += 1
        else:
            break

    string_to_print = stock_date + ';' + str(diffCat) + ';' + prevDays + prevLine + stocks + headlines + '\n'

    if 'None' not in string_to_print:
        output.write(string_to_print)

    # for debugging purposes
    # if stock_date == '2016-08-02':
    #     print('wait')
    