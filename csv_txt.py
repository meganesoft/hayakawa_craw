import pandas as pd

df = pd.read_csv('data/book.csv')

for title in df['title']:
    for text in df['text']:
        with open('data/txt/'+title,'w') as file:
            file.write(str(text)+'.txt')
        
