import gzip
import json
import sys
from collections import OrderedDict
import time

def progress_bar(count, total, status=''):
    # Copyright (c) 2016 Vladimir Ignatev
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def create_days(TIMEFRAME, days_to_search):
    """Creates a list of dates that can be used to create filenames that can be searched"""

    days_to_search.append(TIMEFRAME[0])

    while days_to_search[-1] != TIMEFRAME[1]:
        if ((days_to_search[-1][4:6] == '01' or
            days_to_search[-1][4:6] == '03' or
            days_to_search[-1][4:6] == '05' or
            days_to_search[-1][4:6] == '07' or
            days_to_search[-1][4:6] == '08' or
            days_to_search[-1][4:6] == '10') and
            days_to_search[-1][6:] == '31'):
                days_to_search.append(
                    days_to_search[-1][:4] + str(int(days_to_search[-1][4:6])+1).zfill(2) + '01' 
                    )

        elif ((days_to_search[-1][4:6] == '04' or
            days_to_search[-1][4:6] == '06' or
            days_to_search[-1][4:6] == '09' or
            days_to_search[-1][4:6] == '11') and
            days_to_search[-1][6:] == '30'):
                days_to_search.append(
                    days_to_search[-1][:4] + str(int(days_to_search[-1][4:6])+1).zfill(2) + '01' 
                    )

        elif (days_to_search[-1][4:6] == '02' and
            days_to_search[-1][6:] == '28'):
            if (int(days_to_search[-1][:4]) / 4).is_integer():
                days_to_search.append(
                    days_to_search[-1][:6] + str(int(days_to_search[-1][6:])+1).zfill(2)
                    )
            else:
                 days_to_search.append(
                    days_to_search[-1][:4] + str(int(days_to_search[-1][4:6])+1).zfill(2) + '01' 
                    )

        elif (days_to_search[-1][4:6] == '02' and
            days_to_search[-1][6:] == '29'):
                days_to_search.append(
                    days_to_search[-1][:4] + str(int(days_to_search[-1][4:6])+1).zfill(2) + '01' 
                    )
        
        elif (days_to_search[-1][4:6] == '12' and
            days_to_search[-1][6:] == '31'):
                days_to_search.append(
                    str(int(days_to_search[-1][:4])+1).zfill(2) + '0101' 
                    )

        else:
            days_to_search.append(
                days_to_search[-1][:6] + str(int(days_to_search[-1][6:])+1).zfill(2)
            )

    return days_to_search

def main():

    start_time = time.time()

    #EDIT THESE 2 VARIABLES (adding or removing words is very much possible :) 
    WORDS = ['word1', 'word2', 'word3']
    TIMEFRAME = ['20200506','20211215']

    HOURS = [str(day).zfill(2) for day in range(24)]

    if TIMEFRAME[0] > TIMEFRAME [1]:
        print("TIMEFRAME error")
        exit(-1)

    DAYS_TO_SEARCH = create_days(TIMEFRAME, [])

    counter = OrderedDict()

    counter['total_tweets'] = OrderedDict()

    counter['errors'] = {}
    counter['errors']['incorrect_JSON'] = 0
    counter['errors']['file_not_found'] = 0

    progress = 0
    total_files = len(DAYS_TO_SEARCH) * len(WORDS) * len(HOURS)

    for word in WORDS:
        counter[word] = OrderedDict()
        for date in DAYS_TO_SEARCH:
            counter[word][date] = 0
            counter['total_tweets'][date] = 0
            for hour in HOURS:
                progress +=1
                progress_bar(progress, total_files, status=word + ', ' + date + ':' + hour)
                filename = '/net/corpora/twitter2/Tweets/' + date[:4] + '/' + date[4:6] + '/' + date + ':' + hour + '.out.gz'
                try:
                    with gzip.open(filename, 'rt', encoding='utf8') as inp:
                        for tweet in inp.readlines():
                            if word == WORDS[-1]:
                                counter['total_tweets'][date] += 1
                            try:
                                tweet_json = json.loads(tweet)
                                if word in tweet_json["text"]:
                                    counter[word][date] += 1
                            except:
                                counter['errors']['incorrect_JSON'] += 1
                except:
                    counter['errors']['file_not_found'] += 1

    output_filename = 'output_' + time.strftime("%Y-%m-%d_%H:%M:%S") + '.txt'
    with open(output_filename, 'w') as output:
        output.write(json.dumps(counter, indent=4) + '\n')

    print('\nThis all took {0:.2f} minutes...\n'.format((time.time() - start_time) / 60))

if __name__ == '__main__':
    main()