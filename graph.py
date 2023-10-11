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

# to count nb of row
def count_rows(rows):
  return len(rows)


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
  
  
  #deuxième plot
  
  damage = df.groupby('Décès ou bâtiments touchés').apply(count_rows)
  df2 = pd.DataFrame({'Décès ou bâtiments touchés': damage.index, 'Nombre': damage.values})
  total_nb = df2['Nombre'].sum()
  df2['Pourcentage'] = (df2['Nombre'] / total_nb)*100 
  df2['Pourcentage'] = df2['Pourcentage'].round(2) 
  
  st.header('Données df2')
  st.dataframe(df2)
  
  pie_chart = alt.Chart(df2).mark_arc().encode(
      theta = 'Nombre:Q',
      color = alt.Color('Décès ou bâtiments touchés:N', scale=alt.Scale(scheme='dark2')),
      tooltip = [
        alt.Tooltip('Décès ou bâtiments touchés:N'),
        alt.Tooltip('Pourcentage:Q', title='Pourcentage (%)')
        ]
  ).properties(
      width=400,
      height=400,  
      title='Décès ou bâtiments touchés'
  )

  pie_chart = pie_chart.configure_legend(
    labelLimit=0,  # Show all labels
    titleLimit=0,  # Show the full legend title
  )

  # Afficher le graphique dans Streamlit
  st.header('Distribution')
  st.altair_chart(pie_chart, use_container_width=True)