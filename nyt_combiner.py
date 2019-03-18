output = open('Data/nyt_2000-2015.csv', 'w', encoding='utf-8')
output.write('Date;Headline;Abstract;News Desk;Doc Type;Material Type;Lead Paragraph\n')

for year in range(2000, 2016):
    in_year = open('Data/NYT/nyt_' + str(year) + '.csv', encoding='utf-8')
    in_year.readline()
    for line in in_year:
        split_line = line.split(';')
        if len(split_line) < 7:
            continue
        if split_line[1] == 'None':
            continue
        output.write(line)