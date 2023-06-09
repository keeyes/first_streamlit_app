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
    #output as table
    streamlit.dataframe(from_function)
except URLError as e:
  streamlit.error()
#don't run anything beyond here for streamlit

#snowflake data
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

streamlit.header("The fruit load list contains:")
    
#add button to load fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
    
    

    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('"+ new_fruit +"')")
        return "Thanks for adding "+ new_fruit
        my_cnx.close()

    
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
add_fruit = streamlit.text_input("What fruit would you like to add",'mumbajumbo')
insert_row_snowflake(add_fruit)

