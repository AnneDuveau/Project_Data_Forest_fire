import folium
import json


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
    
		# Créer une couche GeoJSON pour chaque département
		department_layer = folium.GeoJson(
			geometry,
			name=f'Department {code}',
			tooltip=f'Department {code} - {nom}'
		)
		
		# Get the number of rows for the current department
		department_data = df[df['Département'] == code]
		num_rows = len(department_data)
		
		# Add a popup with department data
		popup_html = f'<b>Department:</b> {nom}<br><b>Code:</b> {code} <br><b>Number of Fire:</b> {num_rows}'
		folium.Popup(popup_html).add_to(department_layer)

		# Add the department layer to the map
		department_layer.add_to(m)
  
	return m

