# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """ Choose the fruits you want in your custom Smoothie.
  """
)

name_on_order=st.text_input("Movie title")
st.write('The name of your Smoothie will be:',name_on_order)


cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list=st.multiselect ('Choose up to 5 ingredients :'
                           , my_dataframe
                         ,max_selections=5)

if ingredients_list:
    ingredients_st=''
    
    for i in ingredients_list:
        ingredients_st+=i +' '

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order,ingredients)
            values ('""" + name_on_order + """','""" + ingredients_st + """')"""

    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")




smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json()
