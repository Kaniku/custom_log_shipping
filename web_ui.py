import pymongo
import pandas as pd
import streamlit as st
from PIL import Image

logo = Image.open("tetech.png")
pic_author = Image.open("nimas.png")

st.image(logo, width=200)
st.title("Log List")
st.text("This is the list of log")
st.write("[![Star](https://img.shields.io/github/stars/kaniku/custom_log_shipping.svg?logo=github&style=social)](https://gitHub.com/kaniku/custom_log_shipping)")

author_hdr = st.sidebar.header("About Creator")
author_pict = st.sidebar.image(pic_author, width=100)
author_text = st.sidebar.text(""" A hard-working person and have 
interest in data analytics, 
data science, machine learning, 
deep learning, 
artificial intelligence, 
and big data. 
I have learned about 
artificial intelligence 
since in the second year. 
I able to use Python and SQL 
as artificial intelligence tools. 
In short, I am detail 
oriented person 
and loved to learn something new 
about artificial 
intelligence issues. 
I am able to work both on 
my own initiative an as part 
of a team as well.
Strong experience: 
Analytical thinking, 
machine learning, 
data wrangling, 
data visualization, 
data manipulation, 
and critical thinking. 
""")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

def get_data():
    mydb = myclient["prod"]
    mycol = mydb["log_name_mdb"]
    myquery = mycol.find({},{"_id": 0, "log_name": 1})
    items = list(myquery)  # make hashable for st.cache
    return items

items = get_data()

df = pd.DataFrame(items)

st.table(df)

st.header("Prerequisite")
st.subheader("Installed application")
st.text("""
Microsoft SQL Server Express 2019
Mongodb 5.0.4
""")
st.subheader("Tools that are used to build custom log shipping")
st.text("""
Python 3.8.12
Anaconda3
Streamlit
""")