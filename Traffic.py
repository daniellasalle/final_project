"""
TRAFFIC
"""
#INTRODUCTORY CODE
import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns

path = "C:/Users/Daniella Salle/Downloads/"
dfbridge = pd.read_csv(path + 'georgia_bridges.csv', low_memory=False, index_col= '8 - Structure Number')
dfbridge.rename(columns={"16 - Latitude (decimal)":"lat", "17 - Longitude (decimal)": "lon"}, inplace= True) # make sure to rename them to small cases
st.set_option('deprecation.showPyplotGlobalUse', False)
###
num_lanes= 0
#FUNCTIONS
def chart_title(title, xtitle, ytitle, xreference):
    title_dict= {"Title":title,"X-axis":xtitle, "Y-axis":ytitle,
                 "Intended X-axis":xreference}
    return title_dict

def plot_preference(titles, data, order=False):
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

def graph_design(color_list=["orange"], kind= "bar",num_elements=0, stacked= False):
    theme_colors = {"ORANGE": ["orange", "navajowhite", "sandybrown", "red", "coral"],
                    "YELLOW": ["gold", "yellow", "khaki"],
                    "REDPINK": ["salmon", "tomato", "pink", "lightpink"],
                    "PURPLE": ["thistle", "plum", "violet"],
                    "GREEN": ["teal", "yellowgreen"],
                    "BLUE": ["lightskyblue"]}
    if len(color_list) >= num_elements:
        new_color_list= [color.lower() for color in color_list] #[PY4] List Comprehension
        final_color_list= []
        for i in new_color_list:
            for key in theme_colors:
                if i in theme_colors[key]:
                    final_color_list.append(i)
    else:
        final_color_list=color_list
    return [final_color_list, kind, stacked]

# Highway district vs avg daily traffic
st.sidebar.header("How is Daily Traffic Measured?")
st.sidebar.write("Data is collected, aggregated, and analyzed so that Average Daily Traffic (ADT) can be interpreted as of the average number of vehicles that pass through the bridges each day.")
st.title("Traffic Information to Determine Efficient Routes")
st.header("Context")
st.success("A truck driving service has been looking to take more efficient routes in Georgia. With a truck driver's statewide route and responsibilities for deliveries, it's important to be as timely as possible. By examining traffic levels of bridges filtered through different criteria of interest, drivers can be more informed about crossing specific bridges that will make for a faster route.")
st.sidebar.header("Highway District")
st.sidebar.write("Drivers can view the daily traffic levels from bridges in specific highway districts, or general locations of various highway networks, that are most suitable for their route.")
st.sidebar.header("Number of Lanes")
st.sidebar.write("Why would the number of lanes on each bridge be important? Fewer lanes could be indicitive of routes that cross through more rural areas, while many lanes could be a more industrial, highway oriented route.")
select_traffic = ["Above","Below"]
select_type= st.selectbox("Please select for bridges with ABOVE or BELOW average traffic.",select_traffic)


df_traffic= dfbridge[["2 - Highway Agency District","29 - Average Daily Traffic"]].set_index("2 - Highway Agency District")
df_traffic.rename_axis("Highway District", inplace=True)
df_traffic.rename(columns={"29 - Average Daily Traffic":"Average Daily Traffic"}, inplace= True)

mean_traffic= df_traffic.groupby(["Highway District"]).mean(numeric_only= True)
average= mean_traffic.mean()

greater= mean_traffic[(mean_traffic["Average Daily Traffic"] > average.iloc[0])]
less= mean_traffic[(mean_traffic["Average Daily Traffic"] < average.iloc[0])]

if select_type == "Above":
    traffic_titles = chart_title(title="Above Average Daily Traffic on Georgia Bridges", ytitle="Highway District", xtitle="Daily Traffic", xreference="Daily Traffic")
    traffic_chart = plot_preference(titles=traffic_titles, data=greater, order="ascending")
    plot_elements2 = graph_design(color_list=["salmon"],num_elements=len(greater), kind="barh")
    greater.plot(kind=plot_elements2[1], color=plot_elements2[0], legend= False)
    plt.xlabel(traffic_titles["X-axis"])
    plt.ylabel(traffic_titles["Y-axis"])
    plt.title(traffic_titles["Title"])
    st.pyplot()
elif select_type == "Below":
    traffic_titles = chart_title(title="Below Average Daily Traffic on Georgia Bridges", ytitle="Highway District",xtitle="Daily Traffic", xreference="Daily Traffic")
    traffic_chart = plot_preference(titles=traffic_titles, data=less, order="ascending")
    plot_elements2 = graph_design(color_list=["teal"],num_elements=len(less), kind="barh")
    less.plot(kind=plot_elements2[1], color=plot_elements2[0], legend=False)
    plt.xlabel(traffic_titles["X-axis"])
    plt.ylabel(traffic_titles["Y-axis"])
    plt.title(traffic_titles["Title"])
    st.pyplot()
# BRIDGE NUMBER LANES (x) VS AVG DAILY TRAFFIC (y)
#select highway district
highway_list= [1,3,5,6,7,0,2,4,12,14,25,26,34,62]
highway_select= st.multiselect("Please select (a) Highway District(s):",highway_list)
df_lanes= dfbridge[["29 - Average Daily Traffic","2 - Highway Agency District","28A - Lanes On the Structure"]]
df_lanes.rename(columns={"29 - Average Daily Traffic":"Traffic","2 - Highway Agency District":"highway_district","28A - Lanes On the Structure":"Lanes"}, inplace= True)
df_select3= df_lanes[df_lanes.highway_district.isin(highway_select)] #[DA4] - filtering the data by one condition
sns.set_theme(style="white")
sns.relplot(x="Lanes", y="Traffic", hue="highway_district",
            sizes=(40, 400), alpha=.5, palette="muted",
            height=6, data=df_select3)

if len(highway_select) != 0:
    st.header(f"Number of Lanes and Traffic Levels by District")
    st.pyplot()
    num_lanes= st.slider("Please choose the number of lanes:",1,17)
    if num_lanes in list(df_select3.Lanes):
        st.subheader("Best Bridges for Route by Structure Number")
        st.write(f"Figure 1: Bridges in highway district(s) {highway_select} with {num_lanes} lane(s).")
        df_lanes_structure = df_select3[df_select3.Lanes == num_lanes]
        df_lanes_structure.rename_axis("Bridge Structure Number", inplace=True)
        st.write(df_lanes_structure.iloc[:,:-1])
    else:
        st.write("Please select a valid number of lanes.")

if num_lanes !=0:
    st.write("Figure 2: Locations of Bridges in Figure 1")
    df_map2=dfbridge[["lat","lon","2 - Highway Agency District","28A - Lanes On the Structure"]]
    df_map2.rename(columns={"2 - Highway Agency District":"district","28A - Lanes On the Structure":"lanes"},inplace=True)
    df_conditions= df_map2[(df_map2.district.isin(highway_select)) & (df_map2.lanes == num_lanes)]
    df_conditions.reset_index(inplace=True)
    df_conditions.rename(columns={"8 - Structure Number":"structure"}, inplace=True)
    df_final_map= df_conditions[["structure","lat","lon"]]
    #st.write(df_final_map)
    ICON_URL = "https://images.vexels.com/media/users/3/200180/isolated/preview/1be046b7047961357b49301c0dd9e38d-truck-icon-flat-by-vexels.png" # Get the custom icon online
    #Icon or picture finder: https://commons.wikimedia.org/

     # Format your icon
    icon_data = {
        "url": ICON_URL,
        "width": 100,
        "height": 100,
        "anchorY": 0
        }
    # anchorY means how far away you want your icon from the location
    tool_tip = {"html": "Structure Number:<br/> <b>{structure}</b>",
                "style": { "backgroundColor": "red",
                            "color": "black"}
              }


    icon_data_list = []
    for index, row in df_final_map.iterrows():
        icon_data_list.append(icon_data)

    # Add the icon_data list as a new column to map_df
    df_final_map["icon_data"] = icon_data_list

    # Create a layer with your custom icon
    icon_layer = pdk.Layer(type="IconLayer",
                            data = df_final_map,
                            get_icon="icon_data",
                            get_position='[lon,lat]',
                            get_size=40,
                            pickable=True)

    # Create a view of the map: https://pydeck.gl/view.html
    view_state = pdk.ViewState(
        latitude=df_final_map["lat"].mean(),
        longitude=df_final_map["lon"].mean(),
        zoom=6,
        pitch=0
        )

    icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v11',
        layers=[icon_layer],
        initial_view_state= view_state,
        tooltip = tool_tip
        )

    st.pydeck_chart(icon_map)
    st.pyplot()
