import streamlit
import pandas
import requests
import snowflake.connector

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
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# writes json response to screen
#streamlit.text(fruityvice_response.json())

# convert nested json into a flatten table
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Displays the data into a table
streamlit.dataframe(fruityvice_normalized)

#Connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fuit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)
