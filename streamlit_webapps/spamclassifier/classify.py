#import packages
import numpy as np
import pandas as pd
import nltk
import re
import string
import streamlit as st
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix

nltk.download('stopwords')
from nltk.corpus import stopwords

#nlp model
df=pd.read_csv('spam.csv')
df2=df[['v1','v2']]
df2.rename(columns={'v1':'labels','v2':'msg'},inplace=True)
df2.drop_duplicates(inplace=True)
df2['labels']=df2['labels'].map({'ham':0,'spam':1})


def cleandata(message):
    msg_without_punc=[word for word in message if word not in string.punctuation]
    msg_without_punc=''.join(msg_without_punc)
    separator=' '
    return separator.join([word for word in msg_without_punc.split() if word.lower() not in stopwords.words('english')])

df2['msg']=df2['msg'].apply(cleandata)
print(df2)

x=df2['msg']
y=df2['labels']

#feature extraction
cv=CountVectorizer()
x=cv.fit_transform(x)

#build model
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)
model=MultinomialNB().fit(x_train,y_train)
predictions=model.predict(x_test)
print(accuracy_score(y_test,predictions))
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))


def predict(text):
    labels=['Not Spam','Spam']
    x=cv.transform(text).toarray()
    p=model.predict(x)
    index=int(p[0])
    return str('The message is: '+labels[index])
    

#streamlit webapp
st.title('SPAM CLASSIFIER')
st.image('spam_img.jpg')
user_input=st.text_input('Enter your message')
submit=st.button('PREDICT')
if(submit):
    ans=predict([user_input])
    st.text(ans)

