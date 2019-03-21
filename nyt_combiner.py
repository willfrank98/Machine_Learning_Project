#from nltk.stem.snowball import SnowballStemmer
from textblob import TextBlob


years = range(2000, 2016)

output = open('Data/nyt_busfin_' + str(years[0]) + '-' + str(years[-1]) + '.csv', 'w', encoding='utf-8')
output.write('Date;Headline;Polarity;Subjectivity\n')

for year in years:
    in_year = open('Data/NYT/nyt_' + str(year) + '.csv', encoding='utf-8')
    in_year.readline()
    for line in in_year:
        split_line = line.split(';')
        if len(split_line) < 7:
            continue
        if split_line[1] == 'None':
            continue
        if split_line[3] != 'business/financial desk':
            continue
        if split_line[1] == 'year-end stock tables':
            continue
        if split_line[1] == 'key rates':
            continue
        if split_line[1] == 'dividend meetings':
            continue
        if split_line[1] == 'economic calendar':
            continue

        lead = split_line[6].strip()

        leadBlob = TextBlob(lead)

        polarity = leadBlob.sentiment.polarity
        subjectivity = leadBlob.sentiment.subjectivity

        output.write(split_line[0] + ';' + lead + ';' + str(polarity) + ';' + str(subjectivity) + '\n')
    print("done " + str(year))