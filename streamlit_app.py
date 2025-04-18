# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df=my_dataframe.to_pandas()
ingredients_list=st.multiselect ('Choose up to 5 ingredients :'
                           , my_dataframe
                         ,max_selections=5)

if ingredients_list:
    ingredients_st=''
    
    for i in ingredients_list:
        current_fruit=i
        ingredients_st+=current_fruit +' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == current_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', current_fruit,' is ', search_on, '.')

        st.subheader(current_fruit+' nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
  
    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order,ingredients)
            values ('""" + name_on_order + """','""" + ingredients_st + """')"""

    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
