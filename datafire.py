import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import geopandas as gpd
import folium
import json
from streamlit_folium import st_folium
import france_map as f


# Function to load data with caching
@st.cache_data
def load_data(file_path):
	df = pd.read_csv(file_path, delimiter=';', header=3)
	return df


def add_sidebar():
	st.sidebar.title("made by Anne DUVEAU")
	
	
def choose_data(): 
	# title
	st.markdown("<h1 style='text-align: center;'>🔥 Fire in France ~ 2022 🔥</h1>", unsafe_allow_html=True)
	

	# Option for users to upload a new dataset
	new_dataset_option = st.checkbox("Upload a new dataset")

	df = None
 
	if new_dataset_option:
		uploaded_file = st.file_uploader("Please Upload a CSV file :smiley:", type=["csv"])

		if uploaded_file is not None:
      # si la variable uploaded_file n'est pas nulle 'None'
			df = load_data(uploaded_file)
    
	else:
		#Automatically load the default dataset (change the file path as needed)
		default_file_path = "Incendies.csv"
		df = load_data(default_file_path)	


		# Sample 1000 random rows from the DataFrame
		sample_df = df.iloc[1:].sample(n=1000, random_state=42)
		sample_df = pd.concat([df.iloc[:1], sample_df])

		# Display the sampled data
		st.write("Random sample of 1000 rows:")
		st.write(sample_df)
		
		
		st.header("France Wildfire Department Map")
		folium_map = f.create_map(df)
		st_data = st_folium(folium_map, width=725)

	
		# Display department data when a region is clicked
		st.write("Department Data:")
		if isinstance(st_data, dict) and 'json_data' in st_data:
			selected_region = st_data.json_data
			if selected_region:
				department_code = selected_region.get('name')
				st.write(f"Selected Department: {department_code}")
            
				# Get the number of rows for the selected department
				num_rows = len(df[df['Département'] == department_code])
				st.write(f"Number of fire: {num_rows}")
	
	
if __name__ == "__main__":
	add_sidebar()
	choose_data()



# idée:
# entrée, je voudrai une carte de france découpé en fonction des départements
# on pourrait sélectionner une date d'incendie et voir plusieurs paramètres
# la température (si non nulle)
# la vitesse du vent (si non nulle)
# hygrométrie (si non nulle)
# le nombre
