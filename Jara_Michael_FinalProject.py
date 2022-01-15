import csv, statistics, requests, argparse, logging
import numpy as np
import matplotlib.pyplot as plt


def main():

    """" This project is about exploring the data set for basketball, and finding correlations between various stats and winning games"""

    #Set logging levels

    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    line_count = 0

    logging.debug('Processing data')

    logging.info('Prase data about basketball, choose yes or no for plot and writing a file if you use those optional commands')

    logging.warning('Warning(ignored some lines when read)')

    #logging.error('Error')

    #logging.critical('Its critical')



    #Set up parsering arguments(just a plot)
    parser = argparse.ArgumentParser(description='This file is about comparing various stats in basketball, trying to find the correlation between winning and things like three pointers attempts and plus minus')


    parser.add_argument('-p', '--plot', help = 'Plot the information, input yes for plot', choices= ['yes', 'no'], dest = 'plot')

    parser.add_argument('-w', '--write', help = 'Write a file Comparing plus minus and 3P%', choices= ['yes', 'no'], dest = 'write')
    args = parser.parse_args()

    three_point_attempts = []
    three_point_made = []

    plus_minus = []
    three_point_perc = []
    try :
    #Try to open file, if not, get the file from the internet
        with open('games_details.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter = ',')

            for line in csv_reader:
                if  line['FG3A'] == '' or line['FG3A'] == '':
                    line_count += 1
                    continue

                elif float(line['FG3A']) == 0 or float(line['FG3M']) == 0:
                    line_count +=1
                    continue

                else:
                    #I just need these lines from the file for analysis, so I append them to my own list as a float
                    try:
                        three_point_perc.append(100*float(line['FG3_PCT'])) #Convert to something more readable, scale of 0-100
                        three_point_attempts.append(float(line['FG3A']))
                        three_point_made.append(float(line['FG3M']))
                        plus_minus.append(float(line['PLUS_MINUS']))
                        line_count += 1
                    except ValueError:
                     line_count += 1
                     logger.setLevel(30)
                     continue

    except FileNotFoundError:
        response = requests.get('https://www.kaggle.com/nathanlauga/nba-games?select=games_details.csv')

        if response:
            # write text of requests to auto-mpg.data.txt
            main()

        else:
            print('No response')
            logger.setLevel(ERROR)
            # Set logging to fail

    #Convert lists to numpy arrays to calculate correlation coefficient later
    three_point_made = np.array(three_point_made)

    three_point_attempts = np.array(three_point_attempts)
    plus_minus = np.array(plus_minus)



    three_point_avg = sum(three_point_made)/sum(three_point_attempts)

    #Checks if plot was asked for from the command line
    if args.plot == 'yes':
        # Here im going to truncate the arrays so they are the same size
        three_point_attempts = three_point_attempts[:180000]
        plus_minus = plus_minus[:180000]
        plt.scatter(plus_minus,
                    three_point_attempts)  # Compare three point attempts to the percent made to see if there is a correlation
        print(np.corrcoef(three_point_attempts, plus_minus))  # Calculate Correlation using numpy
        plt.ylabel('Three point attempts')
        plt.xlabel('Plus Minus')
        plt.title('3PA vs Plus Minus\n Correlation: 0.06')

        plt.show()

    else:
        print('No plot was asked for')


    if args.write == 'yes':
        with open('clean-game_details.txt', 'w') as wfile:
            header = ['Plus Minus', 'Three Point Percentage']
            csv_writer = csv.DictWriter(wfile, fieldnames = header)

            csv_writer.writeheader()
            for i in range(0, len(plus_minus)):
                csv_writer.writerow({'Plus Minus' :plus_minus[i], 'Three Point Percentage':three_point_perc[i]})

    else:
        print('No file was written ')



    return line_count

def count_lines():
    count = 0
    with open('games_details.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for line in csv_reader:
            count +=1
    return count


if __name__ == '__main__':
    main()



