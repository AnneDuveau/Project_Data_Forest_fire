import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import geopandas as gpd
import folium
import json
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

import france_map as f
import graph as g

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
		sample_df = df.iloc[1:].sample(n=3000, random_state=42)
		sample_df = pd.concat([df.iloc[:1], sample_df])

		sample_df = g.clean_data(sample_df)
  
		# Display the sampled data
		st.write("Random sample of 3000 rows:")
		st.write(sample_df)
		
		st.header("France Wildfire Department Map")
		folium_map = f.create_map(df)
		st_data = st_folium(folium_map, width=700)
  
		# Add a placeholder to dynamically display the selectbox
		selectbox_placeholder = st.empty()
  
		 # After the map is displayed, call the department function
		selected_department = st.selectbox("Select a Department", sorted(df['Département'].unique()))
  
    # Display department data using the st_data variable
		f.department(df, selected_department, st_data)
  
	return sample_df

	
if __name__ == "__main__":
	add_sidebar()
	sample_df = choose_data()
 
	g.show_plots(sample_df)


