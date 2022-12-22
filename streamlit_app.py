
import streamlit
import pandas
import requests
import snowflake.connector

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

#Display fruityvice Advice header
streamlit.header("Fruityvice Fruit Advice!")
#Text input option to the user to select the fruit to know the more information
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#displays on the screen user selected fruit
streamlit.write('The user entered ', fruit_choice)

#Get the Fruityvice data from the API get
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#Normalize the response json
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display the normalized json response
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The Fruit Load List contains:")
streamlit.dataframe(my_data_row)
                    
#Allow the end user to add fruit to the list
add_my_fruit = streamlit.text_input("What fruit would you like to add:",'jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
