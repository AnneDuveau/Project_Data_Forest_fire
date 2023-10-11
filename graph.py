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
  df['Heure'] = df['Date de première alerte'].dt.hour
  #we remove the time for the column 'Date de première alerte' to have only the date
  df['Date de première alerte'] = df['Date de première alerte'].dt.date

  df['Date de première alerte'] = pd.to_datetime(df['Date de première alerte'])
  #new column for the months
  df['Mois'] = df['Date de première alerte'].dt.month
  #new column for the days
  df['Jour'] = df['Date de première alerte'].dt.day
  # Créer une colonne pour le jour de la semaine
  df['Jour de la semaine'] = df['Date de première alerte'].dt.day_name()
  df['Date de première alerte'] = df['Date de première alerte'].dt.date
  
  return df

# to count nb of row
def count_rows(rows):
  return len(rows)


def show_plots(df):
  #premier plot: nombre d'incendies par Mois
  
  month_names = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
  }
  
  # Remplacez les valeurs numériques des mois par les noms de mois correspondants
  df['Mois'] = df['Mois'].map(month_names)    
  
  st.write(df)
  
  df = df.sort_values('Mois')  
  
  chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Mois:O', title='Mois', sort=list(month_names.values())),
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
  
  #st.header('Données df2')
  #st.dataframe(df2)
  
  pie_chart1 = alt.Chart(df2).mark_arc().encode(
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

  pie_chart1 = pie_chart1.configure_legend(
    labelLimit=0,  # Show all labels
    titleLimit=0,  # Show the full legend title
  )

  # Afficher le graphique dans Streamlit
  st.header('Distribution')
  st.altair_chart(pie_chart1, use_container_width=True)


  
  # autre pie chart
  df['Contour valide'] = df["Présence d'un contour valide"]
  
  contour = df.groupby('Contour valide').apply(count_rows)
  df4 = pd.DataFrame({'Contour valide': contour.index, 'Nombre': contour.values})
  total_nb_2 = df2['Nombre'].sum()
  df4['Pourcentage'] = (df4['Nombre'] / total_nb_2)*100 
  df4['Pourcentage'] = df4['Pourcentage'].round(2) 
  
  #st.header('Données df2')
  #st.dataframe(df2)
  
  pie_chart2 = alt.Chart(df4).mark_arc().encode(
      theta = 'Nombre:Q',
      color = alt.Color('Contour valide:N', scale=alt.Scale(scheme='cividis')),
      tooltip = [
        alt.Tooltip('Contour valide:N'),
        alt.Tooltip('Pourcentage:Q', title='Pourcentage (%)')
        ]
  ).properties(
      width=400,
      height=400,  
      title="Présence d\'un Contour valide"
  )

  pie_chart2 = pie_chart2.configure_legend(
    labelLimit=0,  # Show all labels
    titleLimit=0,  # Show the full legend title
  )

  # Afficher le graphique dans Streamlit
  st.altair_chart(pie_chart2, use_container_width=True)

  
  #troisième plot
  
  monthly_avg = df.groupby('Mois').agg({
    'Surface parcourue (m2)': 'mean',
    'Surface forêt (m2)': 'mean'
  }).reset_index()
  
  
  # Créez un DataFrame avec les moyennes
  df3 = pd.DataFrame({
    'Mois': monthly_avg['Mois'],
    'Moyenne Surface parcourue (m2)': monthly_avg['Surface parcourue (m2)'],
    'Moyenne Surface forêt (m2)': monthly_avg['Surface forêt (m2)']
  })  
  
  df3['Moyenne Surface parcourue (m2)'] = df3['Moyenne Surface parcourue (m2)'].round(2)
  df3['Moyenne Surface forêt (m2)'] = df3['Moyenne Surface forêt (m2)'].round(2)
  
  # Affichez le DataFrame résumé
  st.dataframe(df3)
  
  chart = alt.Chart(df3).transform_fold(
    ['Moyenne Surface parcourue (m2)', 'Moyenne Surface forêt (m2)'],
    as_=['Variable', 'Value'] 
  ).mark_area().encode(
    x=alt.X('Mois:O', title='Mois', sort=list(month_names.values())),
    y=alt.Y('Value:Q', title='Valeur(m2)', stack='normalize'),
    color=alt.Color('Variable:N', title='Variable'),
    tooltip=['Mois:O', 'Value:Q','Variable:N']
  ).properties(
    title='Surface parcourue en forêt par mois'
  ).interactive()
  
  chart = chart.configure_legend(
    labelLimit=0,  # Show all labels
    titleLimit=0,  # Show the full legend title
)

  # Afficher le graphique dans Streamlit
  st.header('Surface parcourue en forêt par mois')
  st.altair_chart(chart, use_container_width=True)
  
  
  # Quatrième plot
  
  weekday_names = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday'
  }
  
  heathour = alt.Chart(df).mark_rect().encode(
    x=alt.X('Jour de la semaine:N', title='Jour de la semaine', sort=list(weekday_names.values())),
    y=alt.Y('Heure', title='Heure de la journée', bin=True),
    color='count()'
  ).properties( 
    title='Taux d\'incendie par heure'
  ).interactive()
  
  st.altair_chart(heathour, use_container_width=True)