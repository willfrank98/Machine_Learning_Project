import pandas as pd
from re import findall

#defines the years to combine
years = range(2005, 2019)

output = open('Data/nyt_busfin_' + str(years[0]) + '-' + str(years[-1]) + '.csv', 'w')
output.write('Date;Headline;\n')

in_desks = {}
out_desks = {}

# iterates through each year
for year in years:
    # loads data into dataframe and sorts by date
    # the NYT api sometimes returns articles imperfectly ordered by date
    in_year = pd.read_csv('Data/NYT/nyt_' + str(year) + '.csv', sep=';', error_bad_lines=False).sort_values('Date')
    in_year = in_year.values.tolist()
    for article in in_year:
        # re-evaluate this tree if choosing non-healines #
        # throws out empty/incomplete articles
        if len(article) < 7:
            continue
        if article[1] == 'None' or type(article[1]) is not str:
            continue
        if type(article[3]) is not str:
            continue
        if type(article[6]) is not str:
            continue
        # makes sure article is from certain 'news desks'
        skip_article = True
        for word in ['business', 'commerce', 'career', 'invest', 'real estate', 'financ', 'job', 'foreign', 'national']:
            if word in article[3]:
                skip_article = False
                break
        if skip_article:
            out_desks[article[3]] = True
            continue
        # These headline'd articles contain no useful information
        if article[1] == 'year-end stock tables':
            continue
        if article[1] == 'key rates':
            continue
        if article[1] == 'dividend meetings':
            continue
        if article[1] == 'economic calendar':
            continue
        if article[1] == 'corrections':
            continue
        if len(findall(' ', article[1])) < 2 and article[2] == 'none': # remove for non-headlines
            continue

        in_desks[article[3]] = True

        text = article[1].strip() # headline

        output.write(article[0][:10] + ';' + text + ';' + '\n')
    print("done " + str(year))
print('done done')