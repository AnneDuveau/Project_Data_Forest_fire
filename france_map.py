import folium
import json
import streamlit as st
import pandas as pd


def create_map(df):
	# Charger les données géographiques des départements de France
	with open('dep_France.geojson', 'r') as file:
    		geojson_data = json.load(file)
      
	# Créer une carte Folium
	m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

	# Ajouter les départements à la carte
	for feature in geojson_data['features']:
		code = feature['properties']['code']
		nom = feature['properties']['nom']
		geometry = feature['geometry']
		
		#coordinates
		if geometry['type'] == 'Polygon':
			coordinates = geometry['coordinates'][0] #prd les coordonnées du 1er anneau supérieur
			latitudes = [point[1] for point in coordinates]
			longitudes = [point[0] for point in coordinates]
			center_latitude = sum(latitudes) / len(latitudes) #calcule la moy de latitude dans le dep
			center_longitude = sum(longitudes) / len(longitudes) #calcule la moy de lg dans le dep
    
		# Get the number of rows for the current department
		department_data = df[df['Département'] == code]
		num_rows = len(department_data)
  
		# Calculate the color based on the number of fires
		department_color = calculate_color(num_rows)
  
		# Créer une couche GeoJSON pour chaque département
		department_layer = folium.GeoJson(
      geometry,
      name=f'Department {code}',
      tooltip=f'Department {code} - {nom}',
      style_function=lambda x, color=department_color: {'fillColor': color, 'color': 'black', 'weight': 1, 'fillOpacity': 1}
    )
  
		# Add a popup with department data
		popup_html = f'<b>Department:</b> {nom}<br><b>Code:</b> {code} <br><b>Number of Fire:</b> {num_rows}'
		folium.Popup(popup_html, max_width=200, color='blue').add_to(department_layer)

		# Add the department layer to the map
		department_layer.add_to(m)
 
	return m


# Function to calculate a color gradient based on the number of fires
def calculate_color(num_fires):
    # Adjust the color scale as needed
    color_scale = ['#ffcccc', '#ff9999', '#ff6666', '#ff3333', '#ff0000', '#990000']
    if num_fires < 5:
      return color_scale[0]
    elif num_fires < 10:
      return color_scale[1]
    elif num_fires < 20:
      return color_scale[2]
    elif num_fires < 30:
      return color_scale[3]
    elif num_fires < 50:
      return color_scale[4]
    else:
      return color_scale[5]



def department(df, department_code, st_data):
  # Filtrer les données pour le département sélectionné
  department_data = df[df['Département'] == department_code]
  
  department_data.loc[:, 'Nom de la commune'] = department_data['Nom de la commune'].astype(str)

  communes_in_department = sorted(department_data['Nom de la commune'].unique().tolist())
    
  st.header(f"Communes in Department {department_code}")
    
  # Use a selectbox to choose a commune
  selected_commune = st.selectbox("Select a Commune:", communes_in_department)
    
  # Display the selected commune
  st.write("Selected Commune:", selected_commune)
  
  # Afficher les informations pour chaque incendie enregistré dans la commune sélectionnée
  selected_incidents = department_data[department_data['Nom de la commune'] == selected_commune]  
  
  
  for i, incident in selected_incidents.iterrows():
    st.subheader(f"Incident {i+1}")
    
    st.write(f"Date de l'incendie: {incident['Date de première alerte']}")
    col1, col2, col3 = st.columns(3)
    
    if pd.notnull(incident['Température (°C)']):
        col1.markdown(f'<h4 style="font-size: 18px;">Température</h4>', unsafe_allow_html=True)
        temperature_value = f"{incident['Température (°C)']} °C"
        font_size = 50
        styled_temperature = f'<span style="background-color: green; color: white; padding: 2px; border-radius: 5px; font-size: {font_size}px; ">{temperature_value}</span>'
        col1.markdown(styled_temperature, unsafe_allow_html=True)

    if pd.notnull(incident['Direction du vent']): 
        col2.markdown(f'<h4 style="font-size: 18px;">Direction du vent</h4>', unsafe_allow_html=True)
        direction_value = f"{incident['Direction du vent']}"
        font_size = 50
        styled_direction = f'<span style="background-color: blue; color: white; padding: 2px; border-radius: 5px; font-size: {font_size}px; ">{direction_value}</span>'
        col2.markdown(styled_direction, unsafe_allow_html=True)
        
    if pd.notnull(incident['Vitesse moyenne du vent (Km/h)']):
        col3.markdown(f'<h4 style="font-size: 18px;">Vitesse moyenne du vent</h4>', unsafe_allow_html=True)
        vitesse_value = f"{incident['Vitesse moyenne du vent (Km/h)']} Km/h"
        font_size = 50
        styled_vitesse = f'<span style="background-color: yellow; color: black; padding: 2px; border-radius: 5px; font-size: {font_size}px; ">{vitesse_value}</span>'
        col3.markdown(styled_vitesse, unsafe_allow_html=True)
    
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Ajoutez une ligne séparatrice
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
        
