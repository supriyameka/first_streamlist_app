
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new Healthy Diner')
streamlit.header('Breakfast Favourites')
streamlit.text('🥣🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥬Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚🥚Hard Boiled Free-Range Egg')
streamlit.text('🍞🥑Avocado Toast')

streamlit.header('🍐🍌Build your own Fruit Smoothie🥝🍓')

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list=my_fruit_list.set_index('Fruit')
                      
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.                      
streamlit.dataframe(fruits_to_show)

#Create fruitvice API call function
def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  #Text input option to the user to select the fruit to know the more information
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to know the information")
  else:
    back_from_function=get_fruitvice_data(fruit_choice)    
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

streamlit.header("The Fruit Load List contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cursor:    
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
  
if streamlit.button("Get the fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row=get_fruit_load_list()                      
  streamlit.dataframe(my_data_row)

streamlit.stop()

#Allow the end user to add fruit to the list
add_my_fruit = streamlit.text_input("What fruit would you like to add:",'jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
#Insert the fruits added by the user into the snowflake table
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
