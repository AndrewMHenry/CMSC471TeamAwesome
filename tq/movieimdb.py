#!/usr/bin/env python3

# Import the imdb package.
import imdb
import csv

ia = imdb.IMDb()

# Dictionary where the movie name is the key and the corresponding
# values are the list
movieSet = {}

# Search for a movie (get a list of Movie objects).

with open('links.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    for row in reader:
        s_result =  ia.get_movie(row[1])

        movieSet[row[0]] = s_result 

print(len(movieSet))
