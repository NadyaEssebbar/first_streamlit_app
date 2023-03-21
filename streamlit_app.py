import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#use panda to load the csv fron an AWS s3 bucket
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#set column Fruit as index
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include  and prepopulate the select
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Apple','Avocado'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table of selected fruit on the page.
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
   back_from_function = get_fruityvice_data(fruit_choice)
   streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()

#Connect to snowflake
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from FRUIT_LOAD_LIST")
    return my_cur.fetchall()

if streamlit.button('Get Fruit load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  # Displays the data into a table
  streamlit.dataframe(my_data_rows)

#Add fruit to snowflake
def insert_row_snowflake(new_fruit):
  my_cur.execute("insert into FRUIT_LOAD_LIST values ()")
  return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
back_from_function = insert_row_snowflake(add_my_fruit)
streamlit.write(back_from_function)
