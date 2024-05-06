"""
REPAIRS
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
            df_trans.sort_index(ascending=True, inplace=True) #[DA2] sorting the data by ascending order
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
        new_color_list= [color.lower() for color in color_list] #[PY4 List Comprehension]
        final_color_list= []
        for i in new_color_list:
            for key in theme_colors:
                if i in theme_colors[key]:
                    final_color_list.append(i)
    else:
        final_color_list=color_list
    return [final_color_list, kind, stacked]

# SLIDER FOR BRIDGE AGE -> Pie chart good vs. fair
df_owner= dfbridge.loc[:,["22 - Owner Agency", "lat","lon", "CAT10 - Bridge Condition"]]
df_count_owner= df_owner.groupby(["22 - Owner Agency"]).count() #[DA7]  frequency count
options= list(df_count_owner.index)
df_owner.rename(columns={"22 - Owner Agency":"owner","CAT10 - Bridge Condition":"condition"}, inplace=True)

st.sidebar.header("Agency")
agency_radio= st.sidebar.radio("Please select the type of agency that commissioned the company to repair the bridges it owns.", options) #[ST2] - radio widget
st.title(f"Repair Information for {agency_radio}-Owned Bridges")
st.header("Context")
st.success(f"The {agency_radio} has/have commissioned a Georgia repair company to make updates to out-of-date bridges it owns. For repair professionals, it may be worthwhile to investigate certain criteria such as age of the bridges and condition. This application will allow the repair company to determine and locate bridges of a certain age range, condition, and material make-up in order to most efficiently prepare for and subsequently excecute their project.")

slider_number= st.slider(f"Please select a range of {agency_radio} bridge ages.",0, 140, (0,140), 20) #[ST3] - slider

min_slider= min(slider_number)
max_slider= max(slider_number)
df_bridgeage= dfbridge.loc[:,["Bridge Age (yr)","CAT10 - Bridge Condition", "22 - Owner Agency", "lat","lon","43A - Main Span Material"]]
df_bridgeage.rename(columns= {"Bridge Age (yr)":"Age", "CAT10 - Bridge Condition":"condition", "22 - Owner Agency": "agency","43A - Main Span Material":"material"}, inplace=True)

select_df= df_bridgeage[(df_bridgeage.Age >= min_slider) & (df_bridgeage.Age <= max_slider) & (df_bridgeage.agency== agency_radio)]
condition_df= select_df.set_index(["condition"])
df_piechart= condition_df.groupby(["condition"]).count()
plot_elements3= graph_design(color_list=["lightskyblue","pink","yellowgreen"])
df_piechart1= df_piechart.iloc[:,:1]
df_piechart1.plot(kind= "pie", autopct= "%.0f%%", subplots= True, legend= False, colors=plot_elements3[0]) #[VIZ2] - piechart
plt.title(f"Percentage of Bridge Condition for {agency_radio} Bridges Aged {min_slider} to {max_slider} (yrs)")
plt.ylabel("")
st.pyplot()

#Seaborn categorical line dot plot
# what data frame main span material, from selected bridge age, key color codes which condition
condition_list= ["Good","Fair","Poor"]
condition_select= st.multiselect("Please select a condition:",condition_list)
df_dotplot= dfbridge.loc[:,["Bridge Age (yr)","CAT10 - Bridge Condition","43A - Main Span Material", "22 - Owner Agency"]]
df_dotplot.rename(columns= {"Bridge Age (yr)":"Age", "CAT10 - Bridge Condition":"condition", "43A - Main Span Material":"material", "22 - Owner Agency":"agency"}, inplace=True)
select_df2= df_dotplot[(df_dotplot.Age >= min_slider) & (df_dotplot.Age <= max_slider) & (df_dotplot.condition.isin(condition_select)) & (df_dotplot.agency == agency_radio)] #[DA5] - filtering data with two or more conditions
select_df2.dropna(inplace=True) #[DA1]- clean the data


if len(condition_select) != 0:
    st.header(f"Main-Span Material of {agency_radio} Bridges Aged {min_slider} to {max_slider} (yrs)")
    sns.set_theme(style="whitegrid", palette="muted")
    # Draw a categorical scatterplot to show each observation
    ax = sns.swarmplot(data=select_df2, x="Age", y="material", hue="condition") #[VIZ3] Seaborn swarmplot
    ax.set(ylabel="")
    st.pyplot()

# LONGITUDE LATITUDE MAP SIDE BAR
map_df= df_bridgeage[(df_bridgeage.Age >= min_slider) & (df_bridgeage.Age <= max_slider) & (df_bridgeage.agency== agency_radio) & (df_bridgeage.condition.isin(condition_select))]
map_df.rename_axis("structure", inplace=True)
map_df.reset_index(inplace=True)
df_materials= map_df[["structure","material"]]
df_materials.set_index("structure", inplace=True)
if len(condition_select) != 0:
    st.title("Bridges and Location")
    st.write(f"Figure 1: Main Span Materials of Specific {agency_radio} Owned Bridges in {condition_select} Condition")
    st.write(df_materials)
    st.write("Figure 2: Locations of Bridges in Figure 1")
# Create custom icons NEED TO FIND LINK OF AN ICON!!!
ICON_URL = "https://static.vecteezy.com/system/resources/previews/022/825/541/original/peach-fruit-peach-on-transparent-background-png.png" # Get the custom icon online
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
            "style": { "backgroundColor": "orange",
                        "color": "white"}
          }


icon_data_list = []
for index, row in map_df.iterrows(): #[DA8] - iterate using iterrows
    icon_data_list.append(icon_data)

# Add the icon_data list as a new column to map_df
map_df["icon_data"] = icon_data_list #[DA9] - add a new column to a data frame

# Create a layer with your custom icon
icon_layer = pdk.Layer(type="IconLayer",
                        data = map_df,
                        get_icon="icon_data",
                        get_position='[lon,lat]',
                        get_size=40,
                        pickable=True)

# Create a view of the map: https://pydeck.gl/view.html
view_state = pdk.ViewState(
    latitude=map_df["lat"].mean(),
    longitude=map_df["lon"].mean(),
    zoom=6,
    pitch=0
    )


icon_map = pdk.Deck(
    map_style='mapbox://styles/mapbox/outdoors-v12',
    layers=[icon_layer],
    initial_view_state= view_state,
    tooltip = tool_tip
    )

st.pydeck_chart(icon_map)
st.pyplot() #[VIZ1] - icon map

