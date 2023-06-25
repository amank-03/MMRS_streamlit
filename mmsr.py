#!/usr/bin/env python
# coding: utf-8

# imports 
# --------------------------------------------------------

import streamlit as st

import pandas as pd 
import numpy as np
import requests
import pickle 
from pathlib import Path

import streamlit_authenticator as stauth
#import streamlit_lottie 
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
import yaml

st.set_page_config(page_title= "MMRS", page_icon= "chart_with_upwards_trend", layout="wide", initial_sidebar_state="auto", menu_items=None)

page_bg_img_ = '''
<style> 
[data-testid="stAppViewContainer"]{
background-image:  url("#https://img.freepik.com/free-photo/yellow-cardboard-papers-row-blue-background_23-2147878381.jpg?size=626&ext=jpg&ga=GA1.2.2098132722.1687610023&semt=ais");
background-size: cover;
}


[data-testid="stSidebar"]{
background-image: url("https://img.freepik.com/free-vector/grunge-watercolor-background-using-pastel-colours_1048-6530.jpg?size=626&ext=jpg&ga=GA1.1.2098132722.1687610023&semt=ais");
background-size: cover;
}

[data-testid="stHeader"] {
background-image: url("https://img.freepik.com/free-photo/colorful-geometric-cardboards_24972-1078.jpg?size=626&ext=jpg&ga=GA1.1.2098132722.1687610023&semt=ais");
background-size: cover;
}

</style>
'''
st.markdown(page_bg_img_, unsafe_allow_html=True)

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-image: url("https://assets1.lottiefiles.com/packages/lf20_3vbOcw.json");
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )



data = pd.read_csv("mms.csv")
data_purchase = pd.read_csv("purchase.csv" )
#---------------------------------------------------------


# Authentication 

from yaml.loader import SafeLoader
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status is False:
    st.error('Username/password is incorrect')

if authentication_status is None:
    st.warning('Please enter your username and password')

if authentication_status:
    authenticator.logout('Logout', 'sidebar', key='unique_key')
    st.write(f'Welcome!!:hatching_chick: *{name}*')
    
    radio = st.sidebar.selectbox('Select Task', ["Home", "Registration" , "Billing" , "Transaction" , "UpdateEntries"])
    #tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])


#-----------------------------------------------------------------------------------------------------------
    if radio != "Home":
        page_bg_img__ = '''
        <style> 
        [data-testid="stAppViewContainer"]{
        background-image:  url("https://img.freepik.com/free-photo/yellow-cardboard-papers-row-blue-background_23-2147878381.jpg?size=626&ext=jpg&ga=GA1.2.2098132722.1687610023&semt=ais");
        background-size: cover;
        }
        </style>
        '''
        st.markdown(page_bg_img__, unsafe_allow_html=True)

    if radio == "Home":  
        st.title('Welcome to Manpower Management and Reward System')  

        @st.cache_data
        def load_lottieurl(url:str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json( )
        
        lottie_url = "https://assets1.lottiefiles.com/packages/lf20_wtpprtnc.json"
        lottie_json = load_lottieurl(lottie_url)

        st_lottie(lottie_json ,key = "Hello" ,  height= 400) 

        

    if radio == "Registration":

      st.title("Manpower Registration")

      with st.form(key='my_form'):
        col1, col2 = st.columns(2)
        with col1:
            ID = st.text_input("Enter ID")
            name = st.text_input("Name")
            F_name = st.text_input("Father's Name")
            add = st.text_input("Address")
        with col2:
            mob = st.text_input("Mobile Number")
            aadhar_num = st.text_input("Enter Aadhar number")
            bp_num = st.text_input("Enter BP number")
            ref = st.text_input("Enter reference ID")
        #data.loc[len(data.index)] = [ID , name , F_name , add , mob, bp_num , ref]

        #data.to_csv("mms.csv" , index = False)


        submit_button = st.form_submit_button(label='Submit')

      if submit_button:
        if len(mob) == 10:
            if len(aadhar_num) == 12:
            
                if ID and name and F_name and add and mob and aadhar_num and bp_num and ref:
                    if ID not in list(data["ID"]) and aadhar_num not in list(data["Aadhar Number"]) and bp_num not in list(data['BP number']):
                        new_row = {"ID": ID , 'Name': name, 'Father Name': F_name, 'Address': add, 'Mobile Number ':mob, 'Aadhar Number':aadhar_num ,  'BP number':bp_num, 'Ref by':ref , 'Reward_points': 0 }
                        data = data.append(new_row, ignore_index=True)
                        st.success("Data added successfully.")
                    else:
                        st.error("User already exists!")
                        st.warning("ID, Aadhar number and BP number has to be unique")      

                    

                else:

                    st.warning("Please fill in all fields.")
            else:
                st.warning("Invalid Aadhaar Number" , icon="⚠️")
        else:
            st.warning("Invalid Phone Number" , icon="⚠️")

      data.to_csv("mms.csv" , index = False)
      data_ = data
        
      @st.cache_data
      def convert_df(df):
            
      # IMPORTANT: Cache the conversion to prevent computation on every rerun
          return df.to_csv().encode('utf-8')

      csv = convert_df(data)

      st.download_button(label="Download Registration data as CSV",data=csv, file_name='mms.csv',mime='text/csv',)
  
    #-----------------------------------------------------------------------------------------------------------------------------

    if radio == "Billing":

        st.title("Purchase Details")

        purchase_type = st.selectbox('Purchase Type', ["Self" , "Referral"])

        with st.form(key='my_form_purchase'):
          
          col3 , col4 = st.columns(2)
          with col3: 
              buyer_ID = st.text_input("Enter Buyer's ID")
              bill_num = st.text_input("Enter Bill Number")
              date = st.date_input("Enter Date of Purchase")
              bill_amt = st.number_input("Enter Bill Amount")
          with col4:
              percent = st.selectbox('Select Reward Percentage', [0.5, 1, 1.5, 2, 2.5 , 3, 3.5, 4, 4.5, 5, 5.5, 6])
              if purchase_type == "Referral":
                ref_num = st.text_input("Enter referrer ID")
                percent_ref = st.selectbox('Select Reward Percentage for referrer', [0.5, 1, 1.5, 2, 2.5 , 3, 3.5, 4, 4.5, 5, 5.5, 6])
          
          submit_button = st.form_submit_button(label='Submit')

        if purchase_type =="Self":
          ref_num = "N/A"
          percent_ref = 0

        if submit_button:
            if buyer_ID and  bill_num and bill_amt:
                if buyer_ID in list(data["ID"]):
                    if int(bill_num) not in list(data_purchase['Bill_no']):
                        new_row = {'P_type':purchase_type, 'Bill_no': bill_num, 'DOP':date, 'Bill Amount':bill_amt, 'Reward percent self ':percent, 'Referrer ID':ref_num , 'Reward percent referrer': percent_ref , "Buyers ID": buyer_ID }

                        data_purchase = data_purchase.append(new_row, ignore_index=True)
                        st.success("Data added successfully.")
                    else:
                        st.error("Incorrect Bill Number")
                else:
                    st.error("Buyer is not registered")

            else:
                st.warning("Please fill in all fields.")

        data_purchase.to_csv("purchase.csv" , index = False)
        
        @st.cache_data
        def convert_df(df):
            
      # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(data_purchase)

        st.download_button(label="Download Billing data",data=csv, file_name='purchase.csv',mime='text/csv',)

        if bill_amt:
            
            points_buyer = float(float(bill_amt)*(percent/100))
            buyer_idx = data[data["ID"] == buyer_ID].index[0]
            buyer_points = data._get_value(buyer_idx, "Reward_points", takeable=False)+ points_buyer
            buyer_name = data._get_value(buyer_idx, "Name", takeable=False)
            data.loc[buyer_idx , "Reward_points"] = buyer_points
            st.write('Points earned by ', buyer_name, ' is ' , points_buyer ,  )
            st.write('Total available points: ' , buyer_points )



        if purchase_type == "Referral" and ref_num:
            points_referrer = float(float(bill_amt)*percent_ref/100)
            referrer_idx = data[data["ID"] == ref_num].index[0]
            referrer_name = data._get_value(referrer_idx, "Name", takeable=False)
            referrer_points = data._get_value(referrer_idx, "Reward_points", takeable=False) + points_referrer
            st.write('Points earned by ', referrer_name, ' is ' , points_referrer  )
            st.write('Total available points: ' , referrer_points )
            data.loc[referrer_idx , "Reward_points"] = referrer_points

        
        data.to_csv("mms.csv" ,  index = False)
        @st.cache_data
        def convert_df(df):
            
      # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(data)

        st.download_button(label="Download Registration data",data=csv, file_name='mms.csv',mime='text/csv',)

    #----------------------------------------------------------------------------------------------------------------

    if radio == "Transaction": 

        st.title("Transaction History")

        ID = st.text_input("Enter ID")

        if ID:
          idx = data[data["ID"] == ID].index[0]

          total_available = data._get_value(idx, "Reward_points", takeable=False)
            
          html_str_ = f""" ## Total points avialable: {total_available}"""

          st.markdown(html_str_ , unsafe_allow_html=True)

          self_df = data_purchase[data_purchase['Buyers ID'] == float(ID)]
          
          
          amt_self = self_df['Bill Amount']
          per_self = self_df['Reward percent self ']
          total_self  = np.dot(amt_self, per_self)/100
            
          html_str_4 = f""" ### :green[Total points earned by self: {total_self}]"""

          st.markdown(html_str_4 , unsafe_allow_html=True)

          st.dataframe(self_df)
          @st.cache_data
          def convert_df(df):
            return df.to_csv().encode('utf-8')

          csv_self = convert_df(self_df)

          st.download_button(label="Download Self Earned Data ",data=csv_self, file_name='self_data.csv',mime='text/csv',)


          refer_df = data_purchase[data_purchase['Referrer ID'] == float(ID)]
          amt_ref = refer_df['Bill Amount']
          per_ref = refer_df['Reward percent self ']
          total_ref  = np.dot(amt_ref, per_ref)/100
          html_str_5 = f""" ### :green[Total points earned by referrals: {total_ref}]"""

          st.markdown(html_str_5 , unsafe_allow_html=True)
          st.dataframe(refer_df)
            
          @st.cache_data
          def convert_df(df):
            return df.to_csv().encode('utf-8')

          csv_ref = convert_df(refer_df)

          st.download_button(label="Download Referral Earned Data ",data=csv_ref, file_name='referred_data.csv',mime='text/csv',)



        st.title("Redeem Points")

        with st.form(key='my_form'):
          redeem = st.number_input("Enter amount to be redeemed")
          submit_button = st.form_submit_button(label='Submit')

        if ID:

          if float(redeem) > float(total_available):
            st.error("Please enter ponits less than available points")
          elif submit_button:
            total_available = total_available -  float(redeem)
            
            html_str = f""" ## :red[Points availed: {redeem}]"""
            st.markdown(html_str, unsafe_allow_html=True)
            
            html_str2 = f""" ##  :green[Points left: {total_available}]"""
      
            st.markdown(html_str2, unsafe_allow_html=True)
            
            data.loc[idx , "Reward_points"] = total_available
          data.to_csv("mms.csv" ,  index = False)

    if radio == "UpdateEntries": 
        tab1 , tab2 = st.tabs(["Update Registration Detials" , "Update Billing Details"])
        
        with tab1:
            ID_update = st.text_input("Enter ID to be updated")
            
            if ID_update:
                if ID_update in list(data["ID"]):
                    idx_update = data[data["ID"] == ID_update].index[0]
                    curr_ent = data[data["ID"] == ID_update]
                    st.write("Current Entry is" )
                    st.write(curr_ent)
                    st.write("Fill detils to be changed")
                    
                    with st.form(key='reg_update'):   
                        
                        col5 , col6 = st.columns(2)

                        with col5:

                            name_up = st.text_input("Name")
                            F_name_up = st.text_input("Father's Name")
                            add_up = st.text_input("Address")
                            mob_up = st.text_input("Mobile Number")
                        with col6:

                            aadhar_num_up = st.text_input("Enter Aadhar number")
                            bp_num_up = st.text_input("Enter BP number")
                            ref_up = st.text_input("Enter reference ID")

                        
                        
                        submit_button_up = st.form_submit_button(label='Submit')
                else:
                    st.warning("No user found", icon="⚠️")      

                if ID_update in list(data["ID"]) and submit_button_up:

                    if name_up:
                        data.loc[idx_update , 'Name'] = name_up
                    if F_name_up:
                        data.loc[idx_update , 'Father Name'] = F_name_up
                    if add_up: 
                        data.loc[idx_update , 'Address'] = add_up
                    if mob_up:
                        data.loc[idx_update , 'Mobile Number '] = mob_up
                    if aadhar_num_up:  
                        data.loc[idx_update , 'Aadhar Number'] = aadhar_num_up
                    if bp_num_up:
                        data.loc[idx_update , 'BP number'] = bp_num_up
                    if ref_up:
                        data.loc[idx_update , 'Ref by'] = ref_up

                    
                    updated_entry = data[data["ID"] == ID_update]

                    st.write("Entries Updated!" )
                    st.write(updated_entry)
                    data.to_csv("mms.csv" ,  index = False)
        with tab2:
            bill_update = st.text_input("Enter Bill number to be updated")
            
            if bill_update:

                if int(bill_update) in list(data_purchase["Bill_no"]):
                    idx_bill_update = data_purchase[data_purchase["Bill_no"] == int(bill_update)].index[0]
                    curr_ent_bill = data_purchase[data_purchase["Bill_no"] == int(bill_update)]
                    st.write("Current Entry is" )
                    st.write(curr_ent_bill)
                    st.write("Fill detils to be changed")
                    
                    purchase_type_up = st.selectbox('Purchase Type',  ["Self" , "Referral"])
                    
                    with st.form(key='bill_update'):   
                        
                        col7 , col8 = st.columns(2)

                        with col7:
                            
                            buyer_ID_up = st.text_input("Enter Buyer's ID")
                            date_up = st.date_input("Enter Date of Purchase")
                            bill_amt_up = st.number_input("Enter Bill Amount")

                    
                        with col8:
                            
                            percent_up = st.selectbox('Select Reward Percentage', [0.5, 1, 1.5, 2, 2.5 , 3, 3.5, 4, 4.5, 5, 5.5, 6])
                            if purchase_type_up == "Referral":
                                ref_num_up = st.text_input("Enter referral ID")
                                percent_ref_up = st.selectbox('Select Reward Percentage for referrer', [0.5, 1, 1.5, 2, 2.5 , 3, 3.5, 4, 4.5, 5, 5.5, 6])
                        submit_button_bill_up = st.form_submit_button(label='Submit')
                else:
                    st.warning("NO such bill found" , icon="⚠️")    

                    
 
                if int(bill_update) in list(data_purchase["Bill_no"]) and submit_button_bill_up:

                    if buyer_ID_up:
                        data_purchase.loc[idx_bill_update , 'Buyers ID'] = buyer_ID_up
                        
                    if date_up:
                        data_purchase.loc[idx_bill_update , 'DOP'] = date_up
                    
                    if bill_amt_up:
                        data_purchase.loc[idx_bill_update , 'Bill Amount'] = bill_amt_up
                    
                    if percent_up:
                        data_purchase.loc[idx_bill_update , 'Reward percent self '] = percent_up
                     
                    if purchase_type_up == "Referral":
                        if ref_num_up:
                            data_purchase.loc[idx_bill_update , 'Referrer ID'] = ref_num_up
                        if percent_ref_up:
                            data_purchase.loc[idx_bill_update , 'Reward percent referrer'] = percent_ref_up
                            
        
                    updated_bill_entry = data_purchase[data_purchase["Bill_no"] == int(bill_update)]

                    st.write("Entries Updated!" )
                    st.write(updated_bill_entry)
                    data_purchase.to_csv("purchase.csv" , index = False)
        
                        

                        