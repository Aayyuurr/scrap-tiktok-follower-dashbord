#import streamlit as st
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import schedule
import time
import streamlit as st

def scrapper():
    
    #url of the website
    url='https://www.tiktok.com/@tom_pouce_07'
    #check the status of the website
    r=requests.get(url)
    

    #extract the html code of the website
    soup=BeautifulSoup(r.text,'html.parser')
    #find the number of followers
    followers=soup.find('strong',attrs={"data-e2e":"followers-count"}).text
    #open csv file
    df=pd.read_csv('tomaAbonne.csv',parse_dates=['Date'])
    # #add the new number of followers with the time of the day
    df=df.append({'follower':followers,'Date':pd.datetime.now(), 'jour':datetime.date.today(), 'heur':datetime.datetime.now().strftime("%H:%M")},ignore_index=True)
    # #save the new csv file

    df.to_csv('tomaAbonne.csv',index=False)


schedule.every().hour.do(scrapper)


with st.sidebar:
    st.write('Tableau de bord pour toma')
    st.write('avoir les nouvelles abonnés')
    st.button('Nouvelles données',on_click=scrapper)

    df=pd.read_csv('tomaAbonne.csv')
    st.dataframe(df)
st.write('nombre de follower par jour')
dfJour=df.groupby('jour').max()
st.bar_chart(dfJour['follower'])
st.line_chart(dfJour['follower'])
st.write('nomber de follower gagner par jours')
dfJour['follower']=dfJour['follower'].diff()
st.bar_chart(dfJour['follower'])
st.line_chart(dfJour['follower'])

#get the number of followers of this jour
def getFollowerJour(df):
    thisJour=datetime.date.today()
    df_this_jour=df[df['jour']==str(thisJour)]
    st.write(f'Evolution du nombre de follower de {thisJour} par heure')
    st.bar_chart(df_this_jour, x='heur', y='follower')
    st.line_chart(df_this_jour, x='heur', y='follower')
    df_this_jour=df_this_jour.set_index('heur')
    #différence entre le nombre de follower de cette heure et l'heure précédente
    st.write(f'Evolution du nombre de follower gagner de {thisJour} par heure')
    x=df_this_jour['follower']=df_this_jour['follower'].diff()
    st.bar_chart(x)
    st.line_chart(x)
    return df_this_jour

getFollowerJour(df)
while True:
    schedule.run_pending()
    time.sleep(1)
