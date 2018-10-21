import csv
import random
import parser2
from prettytable import PrettyTable


movieSet = {}
movieList = []

'''
populating movieSet(title: genres) and movieList(titles)
'''
with open('test0_for.csv') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)
    for row in reader:
        title = ''.join(row[1]).split('(')[0]
        title = ''.join(title).strip()
        genres = row[2]
        movieSet[title] = genres.split('|')
        movieList.append(title)


file.close()
# randomly choosing 2 movies from the List and print them
try:
    random_movies = random.sample(movieList, 1)
except ValueError:
    print('sample size exceeded size of movieList')

print
print('Below are 1 random generated movies out of 25 movies: ')
printer = PrettyTable()
printer.field_names = ['title', 'genres']
for i in range(1):
    printer.add_row([random_movies[i], '|'.join(movieSet[random_movies[i]])])

print(printer)

print
print('*********** Start Test **************')


'''
Ideally, each movie has a genre's counter.
When the counter for a movie hits ZERO, then stop test
failed because algorightm is taking too much time guessing
for the right answer.
Each tume algortihm guess right genre, reduce counter by 1
'''

'''
In this case we just let the algortihm guess the right movies
on a multiple attemps scenario
'''
attemps = 1
failures = 0
successes = 0
rounds = 2

# totalMovies = parser2.get_length_movieSet(parser2.get_movieSet())

# Each movie has 3 attemps
for i in range(1):

    firstPass = True
    curr_attempts = 1
    curr_successes = 0
    curr_failures = 0
    got_success = False
    totalMovies = parser2.get_length_movieSet(parser2.get_movieSet())

    while curr_attempts <= rounds:
        if firstPass:
            print('Current Attemps: ' + str(curr_attempts))
            print('Our guess movie is: ' + random_movies[i])
            firstPass = False
        else:
            print('Current Attemps: ' + str(curr_attempts))

        output_str = parser2.get_questions(totalMovies, 0.1, 0, 20, 'none')
        if 'Found movie' in output_str:
            curr_successes += 1
            successes += 1
            got_success = True
            break

        else:
            curr_failures += 1
            failures += 1

        curr_attempts += 1
        attemps += 1

    if got_success:
        print(random_movies[i] + ' current statistics: ')
        print('[Current Attemps: ' + str(curr_attempts) + ', ' +
              'current failures: ' + str(curr_failures) + ', ' +
              'current successes: ' + str(curr_successes) + ']')
    else:
        print(random_movies[i] + ' Current statistics: ')
        print('[Current Attemps: ' + str(curr_attempts - 1) + ', ' +
              'curent failures: ' + str(curr_failures) + ', ' +
              'current successes: ' + str(curr_successes) + ']')

        attemps -= 1

print
print('General statistics: ')
print('[Attemps: ' + str(attemps) + ', ' +
      'Failure: ' + str(failures) + ', ' +
      'Success: ' + str(successes) + ']')
