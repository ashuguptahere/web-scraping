import csv
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

# row_names = ['movie_id', 'movie_title']
# row_names = ['movie_id', 'movie_title', 'genre', 'movie_logo', 'movie_url']

row_names = ['movie_id', 'movie_title']
with open('u.item3.txt', 'r', encoding = "ISO-8859-1") as f:
    reader = csv.DictReader(f, fieldnames=row_names, delimiter='|')
    for row in tqdm(reader):
        movie_id = row['movie_id']
        movie_title = row['movie_title']
        domain = 'http://www.imdb.com'
        search_url = domain + '/find?q=' + urllib.parse.quote_plus(movie_title)
        with urllib.request.urlopen(search_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # Get url of 1st search result
            try:
                title = soup.find('table', class_='findList').tr.a['href']
                genre = ''
 
                movie_url = domain + title
                with open('movie_url_new.csv', 'a', newline='') as out_csv:
                    writer = csv.writer(out_csv, delimiter=',')
                    writer.writerow([movie_id, movie_title, genre, movie_title + '.jpeg', movie_url])
            # Ignore cases where search returns no results
            except AttributeError:
                pass

p = '*|\/<>":?'
def remove_punctuation(txt):
    txt_output = "".join([c if c not in p else "  -" for c in txt])
    return txt_output

row_names = ['movie_id', 'movie_title', 'movie_genre', 'movie_logo', 'movie_url']
with open('movie_url_new.csv', 'r', newline='', encoding = "ISO-8859-1") as in_csv:
    reader = csv.DictReader(in_csv, fieldnames=row_names, delimiter=',')
    for row in tqdm(reader):
        movie_id = row['movie_id']
        movie_url = row['movie_url']
        movie_title = row['movie_title']
        movie_title = remove_punctuation(movie_title)
        # if movie_title[-12:-8] == ', The':
        #     print("Y")
        domain = 'http://www.imdb.com'
        with urllib.request.urlopen(movie_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # Get url of poster image
            try:
                image_url = soup.find('div', class_='poster').a.img['src']
                
                movie_genre = soup.find('div', class_='subtext').text.split('\n')
                movie_genre = ''.join(movie_genre)
                movie_genre = movie_genre.split('\n')
                movie_genre = ''.join(movie_genre)
                movie_genre = movie_genre.split('|')[-2]
                
                movie_description = soup.find('div', class_='summary_text').text
                movie_description = movie_description[21:]
                movie_description = movie_description[:-13]
                
                movie_logo = movie_title + '.jpg'
                
                # TODO: Replace hardcoded extension with extension from string itself
                extension = '.jpg'
                image_url = ''.join(image_url.partition('_')[0]) + extension
                filename = 'img/' + movie_title + extension
                with urllib.request.urlopen(image_url) as response:
                    # with open(filename, 'wb') as out_image:
                    #     out_image.write(response.read())
                    with open('movie_poster_new.csv', 'a', newline='') as out_csv:
                        writer = csv.writer(out_csv, delimiter=',')
                        writer.writerow([movie_id, movie_title, movie_genre, movie_description, movie_logo, movie_url, image_url])
            # Ignore cases where no poster image is present
            except:
                pass



df1 = pd.read_csv("web_movie.csv")
df2 = pd.read_csv("web_movie2.csv")

a = []
num = 0
for i in df2["title"]:
    num+=1
    for j in df1["title"]:
        if(i == j):
            print(num, j)
            a.append([num, j])



dataset = pd.read_csv("all.csv")

movie_title = "Net, The (1994)"

movies = []
for movie_title in dataset["movie_title"]:
    if movie_title[-12:-7] == ", The":
        movie_title = movie_title.replace(movie_title[-12:-7], '')
        movie_title = "The " + movie_title
    movies.append(movie_title)



movie = "Net, The Google (123)"
# movie.find(", The")
movie.replace(movie[movie.find(", The"):movie.find(", The")+5], '')
