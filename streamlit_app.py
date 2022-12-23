import streamlit
import pandas
import snowflake.connector
import requests

# Function to get fruitvice_data normalized  
def get_fruitvice_data(this_fruit_choice):
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +  fruit_choice)
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       return fruityvice_normalized

# Function to get Fruit List from Snowflake
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("SELECT * from fruit_load_list")
         return  my_cur.fetchall()

# Function Insert row into  Snowflake
def insert_row_fruit_load_list(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
         return  "Thanks for adding " + new_fruit

# Function Insert row into  Snowflake
def delete_row_fruit_load_list(delete_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("Delete from fruit_load_list where fruit_name like ('" + delete_fruit + "')")
         return  "Deleted from Table " + delete_fruit


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

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
  if not fruit_choice:
       streamlit.error("Please select a fruit to get information")
  else:
       back_from_f_fruityvice = get_fruitvice_data(fruit_choice)
       streamlit.dataframe(back_from_f_fruityvice)
except URLError as e:
       streamlit.error()
    
    
# Snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

#Verify Snowflake Connection
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)

# Readinf from Snowflake Table 
my_data_rows = get_fruit_load_list()
streamlit.dataframe(my_data_rows)
my_cnx.close()                        

# Add Fruit 
input_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', input_fruit)

# Snowflake connection
if streamlit.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_fruit_load_list(input_fruit)
   streamlit.text(back_from_function)
   my_cnx.close()                        

if streamlit.button('Delete  a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = delete_row_fruit_load_list(input_fruit)
   streamlit.text(back_from_function)
   my_cnx.close()                        

       
       
