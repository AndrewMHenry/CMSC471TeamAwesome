import csv
import sys

csv.field_size_limit(sys.maxsize)

movieSet = {}
imdbMovieSet = {}

# Parse csv file into movieSet format
with open('movies.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    for row in reader:
        movieSet[row[0]] = row[1] 

with open('imdbmovie.csv', 'r') as imdb:
    imdbreader = csv.reader(imdb, delimiter=',')
    for row in imdbreader:
        if(len(row) == 1) :
            imdbMovieSet[row[0]] = ""
        else:
            imdbMovieSet[row[0]] = row[0]

print(movieSet)
print(imdbMovieSet)

