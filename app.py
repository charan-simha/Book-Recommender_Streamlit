#import all important files

import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.set_page_config(layout="wide")

st.header("Book Recommender System")

st.markdown('''
               #### The site using collaborative filtering to suggest books from our catalogue
               ###  We also suggest top 50 books for all our readers
               ''')

#import our models

popular=pickle.load(open('popular.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))

#top 50 books

st.sidebar.title('Top 50 Books')

if st.sidebar.button('SHOW',key='show_top_books'):
    cols_per_row = 5  # Define 5 columns per row
    num_books = len(popular)  # Total books available
    num_rows = min(10, num_books // cols_per_row)  # Ensure correct row count

    for row in range(num_rows):
        cols = st.columns(cols_per_row)  # ✅ Creates 5 columns per row
        for col in range(cols_per_row):
            book_idx = row * cols_per_row + col  # ✅ Corrected index calculation
            if book_idx < num_books:  # ✅ Ensure index is within bounds
                with cols[col]:  # ✅ Ensures correct column placement
                    st.image(popular.iloc[book_idx]['Image-URL-M'])
                    st.text(popular.iloc[book_idx]['Book-Title'])  
                    st.text(popular.iloc[book_idx]['Book-Author'])  

                    
                    
                    
# function to recommend books

def recommend(book_name):
    index=np.where(pt.index==book_name)[0][0]
    similar_items=sorted(list(enumerate(similarity_scores[index])),key=lambda x: x[1],reverse=True)[1:6]
    data=[]
    for i in similar_items:
        item=[]
        df_temp=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(df_temp.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(df_temp.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(df_temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data

#Names list of books
book_list=pt.index.values

st.sidebar.title('Similar book Suggestions')
selected_book=st.sidebar.selectbox('Select a book from the dropdown',book_list)
if st.sidebar.button('SHOW',key='show_similar_books'):
    book_recommended=recommend(selected_book)
    cols=st.columns(5)
    for col_idx in range(5):
        with cols[col_idx]:
            if col_idx < len(book_recommended):
                st.image(book_recommended[col_idx][2])
                st.text(book_recommended[col_idx][0])
                st.text(book_recommended[col_idx][1])
    
    
books=pd.read_csv('Books.csv')
users=pd.read_csv('Users.csv')
ratings=pd.read_csv('Ratings.csv')

st.sidebar.title('Data Used')
if st.sidebar.button('Show'):
    st.subheader('This is the books data we used in our model')
    st.dataframe(books)
    st.subheader('This is the Users data we used in our model')
    st.dataframe(users)
    st.subheader('This is the Ratings data we used in our model')
    st.dataframe(ratings)
    
    