import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title("My parents New healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("🥣Omega 3 & Blueberry oatmeal")
streamlit.text("🥗Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard boiled free range eggs")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New seciton to display fruitvice api response
def get_fruityvice_data(this_fruit_choice):
    #api call (no need key) for fruityvice
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #take the json format and normalize it
    fruityvice_normalized =  pandas.json_normalize(fruityvice_response.json())  
    return fruityvice_normalized
  
  
streamlit.header("Fruityvice Fruit Advice!")

try:
  #user input
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    from_function = get_fruityvice_data(fruit_choice)
    streamlit.write('The user entered ', from_function)
    #output as table
    streamlit.dataframe(from_function)
except URLError as e:
  streamlit.error()
#don't run anything beyond here for streamlit
streamlit.stop()
#snowflake data

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_fruit = streamlit.text_input("What fruit would you like to add",'mumbajumbo')
streamlit.text("Thanks for adding "+add_fruit)
my_cur.execute("insert into fruit_load_list values('from streamlit')")

