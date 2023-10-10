import folium
import json
import streamlit as st



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
    
  communes_in_department = sorted(department_data['Nom de la commune'].unique().tolist())
    
  st.header(f"Communes in Department {department_code}")
    
  # Use a selectbox to choose a commune
  selected_commune = st.selectbox("Select a Commune:", communes_in_department)
    
  # Display the selected commune
  st.write("Selected Commune:", selected_commune)