import streamlit
import pandas
import snowflake.connector
import requests

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('Kale Salad , Beet, cole Slaw')
streamlit.text('Orange Juice')
streamlit.header('Build Your Own Smoothie')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

fruit_choice = streamlit.text_input('What fruit would you like information about?')

try:
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +  fruit_choice)
   #streamlit.text(fruityvice_response)
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +  fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   streamlit.dataframe(fruityvice_normalized)
except URLError as e:
   streamlit.error()

