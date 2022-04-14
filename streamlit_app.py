import streamlit
import pandas as pd

streamlit.title("My mom's New Healthy Diner")

streamlit.header("Breakfast Favorites")
streamlit.text("🍲 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥯 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Bolied Free-Range Egg")
streamlit.text("🥝 Avocado toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# display the table on the page
streamlit.dataframe(my_fruit_list)
