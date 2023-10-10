import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt

#fichier pour nettoyer le dataset

def clean_data(df):
  #convert data into datetime
  df['Date de première alerte'] = pd.to_datetime(df['Date de première alerte'])
  #create a hour column
  df['Heure de première alerte'] = df['Date de première alerte'].dt.strftime('%H:%M')
  #we remove the time for the column 'Date de première alerte' to have only the date
  df['Date de première alerte'] = df['Date de première alerte'].dt.date

  df['Date de première alerte'] = pd.to_datetime(df['Date de première alerte'])
  #new column for the months
  df['Mois'] = df['Date de première alerte'].dt.month
  #new column for the days
  df['Jour'] = df['Date de première alerte'].dt.day
  
  return df


def show_plots(df):
  #premier plot: nombre d'incendies par Mois
  
  month_names = {
    1: 'Janvier',
    2: 'Février',
    3: 'Mars',
    4: 'Avril',
    5: 'Mai',
    6: 'Juin',
    7: 'Juillet',
    8: 'Août',
    9: 'Septembre',
    10: 'Octobre',
    11: 'Novembre',
    12: 'Décembre'
  }
  
  chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Mois:O', title='Mois'),
    y=alt.Y('count():Q', title='Nombre d\'incendies'),
    tooltip=[alt.Tooltip('count()', title='Nombre d\'incendies')]
  ).properties(
    title='Nombre d\'incendies en France par mois'
  ).interactive()

  # Afficher le graphique dans Streamlit
  st.header('Statistiques sur les incendies en France en 2022')
  st.altair_chart(chart, use_container_width=True)