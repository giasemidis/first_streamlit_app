import requests
import streamlit
import pandas as pd
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # take the json version of the response and normalize it
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()


def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
    msg = "Thanks for adding " + new_fruit
    return msg


streamlit.title("My mom's New Healthy Diner")

streamlit.header("Breakfast Favorites")
streamlit.text("🍲 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥯 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Bolied Free-Range Egg")
streamlit.text("🥝 Avocado toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# New section to display fruity api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input("What fruit would you like information about?")
  streamlit.write("The user entered", fruit_choice)
  if not fruit_choice:
    streamlit.error("Plase select a fruit to get information.")
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

streamlit.header("View Our Fruit List - Add Your Favorites")
# Add a button to load the fruit
if streamlit.button("Get Fruit List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

# don't run anything past here while we troubleshoot
# streamlit.stop()

add_my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button("Add a Fruit to the List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  msg = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.write(msg)
