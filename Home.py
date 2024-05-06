"""
Daniella Salle
CS 230
Final Project
"""
#INTRODUCTORY CODE
import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

path = "C:/Users/Daniella Salle/Downloads/"
dfbridge = pd.read_csv(path + 'georgia_bridges.csv', low_memory=False, index_col= '8 - Structure Number')
dfbridge.rename(columns={"16 - Latitude (decimal)":"lat", "17 - Longitude (decimal)": "lon"}, inplace= True) # make sure to rename them to small cases
st.set_option('deprecation.showPyplotGlobalUse', False)
###

#FUNCTIONS
def chart_title(title, xtitle, ytitle, xreference): #[PY3] a function called at least two different times in your program
    title_dict= {"Title":title,"X-axis":xtitle, "Y-axis":ytitle,
                 "Intended X-axis":xreference}
    return title_dict

def plot_preference(titles, data, order=False): #[PY1] a function with two or more parameters, one of which has a default
    df= pd.DataFrame(data)
    if titles["Intended X-axis"] in df.head(0):
        df_trans = df.transpose() #switches x and y
    else:
        df_trans = df
    if order != False:
        if order== "ascending":
            df_trans.sort_index(ascending=True, inplace=True) #[DA2]
        elif order== "descending":
            df_trans.sort_index(ascending=False,inplace=True)
    return df_trans

def graph_design(color_list=["orange"], kind= "bar",num_elements=0, stacked= False): #[PY2] a function that returns more than one value
    theme_colors = {"ORANGE": ["orange", "navajowhite", "sandybrown", "red", "coral"],
                    "YELLOW": ["gold", "yellow", "khaki"],
                    "REDPINK": ["salmon", "tomato", "pink", "lightpink"],
                    "PURPLE": ["thistle", "plum", "violet"],
                    "GREEN": ["teal", "yellowgreen"],
                    "BLUE": ["lightskyblue"]} #[PY5] pt. 1, a dictionary where you call its keys
    if len(color_list) >= num_elements:
        new_color_list= [color.lower() for color in color_list]
        final_color_list= []
        for i in new_color_list:
            for key in theme_colors: # [PY5] pt. 2, here is where keys are being called for
                if i in theme_colors[key]:
                    final_color_list.append(i)
    else:
        final_color_list=color_list
    return [final_color_list, kind, stacked]

home_title = '<p style="font-family:Georgia; color:orange; font-size: 70px;">Bridges in Georgia'
st.markdown(home_title, unsafe_allow_html=True)
st.header("Context")
st.success("Aggregate data on 10,000 bridges in the state of Georgia was collected. There are relevent applications that analyses of specific variables can provide: Repairs and Traffic.")

st.sidebar.subheader("Photos of Bridges in Savannah, Georgia")
img = Image.open("C:/Users/Daniella Salle/Downloads/bridge!.png") #[ST4] sidebar and images
st.sidebar.image(img, width= 300, caption= "'Savannah, Georgia, USA' by pom'. is licensed under CC BY-SA 2.0.")
img2 = Image.open("C:/Users/Daniella Salle/Downloads/bridge2.png")
st.sidebar.image(img2, width= 300, caption= "'Savannah, Georgia, USA' by pom'. is licensed under CC BY-SA 2.0.")
img3= Image.open("C:/Users/Daniella Salle/Downloads/peaches5.png")
st.image(img3, width= 400, caption= "'Peaches' by La Grande Farmers' Market is licensed under CC BY 2.0.")


st.subheader("Compare the number of bridges in each Georgia county!")
#MULTISELECT TO COUNTY BAR CHART
county_names = list(dfbridge["3 - County Name"])
select_county= st.multiselect("Please select a county.",county_names) #[ST1] multiselect
if len(select_county)== 0:
    st.write("Please make a selection.")
elif len(select_county) == 1:
    st.write(f"The county you choose is {', '.join(select_county)}.")
else:
    st.write(f"The counties you chose are {', '.join(select_county)}.")


dfc= dfbridge.set_index("3 - County Name")
dfcounty= pd.DataFrame(dfc)
dfcounty.rename_axis("County", inplace=True)
df_chart = dfcounty.groupby("County").count()
df_chart2= df_chart.iloc[:,0:1]
df_chart2.rename(columns={"1 - State Code":"Number of Bridges"}, inplace= True)
list1= [x for x in select_county] #[PY4] List Comprehension
select_county_chart= df_chart2.loc[list1]

county_titles= chart_title(title="Total Bridges in Each Georgia County", xtitle="County", ytitle="Number of Bridges", xreference="County")
county_chart= plot_preference(titles=county_titles, data=df_chart2, order="ascending")
plot_elements= graph_design(color_list=["orange","salmon","yellow","pink","red"],num_elements=len(select_county))
if len(select_county) != 0:
    select_county_chart.plot(kind=plot_elements[1], color= plot_elements[0], legend= False) #[VIZ1] -bar chart
    plt.xlabel(county_titles["X-axis"])
    plt.ylabel(county_titles["Y-axis"])
    plt.title(county_titles["Title"])
    st.pyplot()