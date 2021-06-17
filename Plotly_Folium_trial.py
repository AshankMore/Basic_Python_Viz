#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
get_ipython().run_line_magic('matplotlib', 'inline')
warnings.filterwarnings("ignore")


# In[18]:


data = pd.read_csv('./Downloads/worldhap2021.csv')


# In[19]:


data21 = pd.read_csv('./Downloads//worldhapold.csv')


# In[7]:


import plotly 
import plotly.express as ex
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.graph_objs as go


# In[11]:


display(data.head())
display(data21.head())


# In[21]:


display(data.shape)
display(data21.shape)


# In[22]:


data.columns


# In[23]:


data21.columns


# In[24]:


data.sort_values(by='Ladder score',ascending=False,inplace=True)


# In[25]:


data['Regional indicator'].value_counts()


# In[27]:


RI_grp=data.groupby(['Regional indicator']).agg({'Country name':'count','Ladder score':'mean'}).reset_index().rename({'Country name':'Country count','Ladder score':'Avg. Ladder score'},axis=1)
RI_grp['Avg. Ladder score']=round(RI_grp['Avg. Ladder score'],3)


# In[28]:


## Plot Region wise count of countries and average ladder score

from plotly.subplots import make_subplots
fig=go.Figure()
fig.add_trace(go.Bar(
    x=RI_grp['Regional indicator'],
    y=RI_grp['Country count'],
    name='Country Count',
    marker_color='lightblue',
    text=RI_grp['Country count'],
    textposition='inside',
    yaxis='y1'
))
fig.add_trace(go.Scatter(
    x=RI_grp['Regional indicator'],
    y=RI_grp['Avg. Ladder score'],
    name='Average Ladder Score',
    mode='markers+text+lines',
    marker_color='magenta',
    marker_size=10,
    text=RI_grp['Avg. Ladder score'],
    textposition='top center',
    line=dict(color='#5D69B1',dash='dash'),
    yaxis='y2'

))
fig.update_layout(
    title="Region Wise Counts and Avg ladder Score",
    xaxis_title="Region",
    yaxis_title="Count of Country",
    template='ggplot2',
    font=dict(
        size=12,
        color="Black",
        family="Garamond"
        
    ),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    plot_bgcolor='white',
    yaxis2=dict(showgrid=True,overlaying='y',side='right',title='Avg. Ladder Score'),
    legend=dict(yanchor="top",
    y=1.3,
    xanchor="left",
    x=0.78)
)
fig.show()


# In[29]:


RI_grp1=data.groupby('Regional indicator').agg({'Social support':'mean','Healthy life expectancy':'mean'}).reset_index().rename({'Social support':'Avg. Social support','Healthy life expectancy':'Avg. Healthy life expectancy'},axis=1)


# In[30]:


RI_grp1['Avg. Social support']=round(RI_grp1['Avg. Social support'],3)
RI_grp1['Avg. Healthy life expectancy']=round(RI_grp1['Avg. Healthy life expectancy'],3)


# In[31]:


from plotly.subplots import make_subplots
fig=go.Figure()
fig.add_trace(go.Bar(
    x=RI_grp1['Regional indicator'],
    y=RI_grp1['Avg. Healthy life expectancy'],
    name='Avg health life exp.',
    marker_color='mediumspringgreen',
    text=RI_grp1['Avg. Healthy life expectancy'],
    yaxis='y1'
))
fig.add_trace(go.Scatter(
    x=RI_grp1['Regional indicator'],
    y=RI_grp1['Avg. Social support'],
    name='Average Ladder Score',
    mode='markers+text',
    marker_color='black',
    marker_size=10,
    text=RI_grp1['Avg. Social support'],
    textposition='bottom center',
    textfont=dict(color='black'),
    yaxis='y2'

))
fig.update_layout(
    title="Region Wise Avg. Social support & Healthy life expectancy",
    xaxis_title="Region",
    yaxis_title="Avg. Healthy life expectancy",
    template='ggplot2',
    font=dict(
        size=10,
        color="black",
        family="Garamond"
        
    ),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    plot_bgcolor='white',
    yaxis2=dict(showgrid=True,overlaying='y',side='right',title='Avg. Social support'),
    legend=dict(yanchor="top",
    y=1.3,
    xanchor="left",
    x=0.78)
)
fig.show()


# In[32]:


#defining data
trace = go.Scatter(x = data['Perceptions of corruption'],y=data['Dystopia + residual'],text = data['Country name'],mode='markers',marker={'color':'red'})
df=[trace]
#defining layout
layout = go.Layout(title='Perceptions of corruption & Dystopia + residual : Scatter Plot',xaxis=dict(title='Perceptions of corruption'),yaxis=dict(title='Dystopia + residual'),hovermode='closest')
#defining figure and plotting
figure = go.Figure(data=df,layout=layout)
figure.update_layout(template='ggplot2',
                  xaxis=dict(showgrid=True),
                  yaxis=dict(showgrid=True),
                  plot_bgcolor='lightgrey',
                  font=dict(family="Garamond"))
figure.show()


# In[36]:


pip install geopy


# In[37]:


#function to get longitude and latitude data from country name
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="<masked>")### pass a valid mailid
def geolocate(country):
    try:
        # Geolocate the center of the country
        loc = geolocator.geocode(country)
        # And return latitude and longitude
        return (loc.latitude, loc.longitude)
    except:
        # Return missing value
        return np.nan


# In[38]:


data['lat_long']=data['Country name'].apply(geolocate)


# In[39]:


### Get the country name where lat long is not present 
# data['lat_long'].isna().sum()
# data[data['lat_long'].isna()] ## Hong kong SAR of china

## add lat long 
data['lat_long']=np.where(data['Country name']=='Hong Kong S.A.R. of China','(22.3193,114.1694)',data['lat_long'])


# In[40]:


data['lat_long']=data['lat_long'].astype(str)
data['lat_long']=data['lat_long'].str.replace('(','')
data['lat_long']=data['lat_long'].str.replace(')','')
data=pd.concat([data,data['lat_long'].str.split(',',expand=True).rename({0:'lat',1:'long'},axis=1)],axis=1)


# In[41]:


# Create a world map to show distributions of users 
import folium
from folium.plugins import MarkerCluster
#empty map
world_map= folium.Map(tiles="cartodbpositron")
marker_cluster = MarkerCluster().add_to(world_map)
#for each coordinate, create circlemarker of user percent
for i in range(len(data)):
        lat = data.iloc[i]['lat']
        long = data.iloc[i]['long']
        radius=5
        popup_text = """Country : {}<br>
                    Logged GDP per capita : {}<br>
                    Ladder score : {}<br>"""
        popup_text = popup_text.format(data.iloc[i]['Country name'],
                                   data.iloc[i]['Logged GDP per capita'],data.iloc[i]['Ladder score']
                                   )
        folium.CircleMarker(location = [lat, long], radius=radius, popup= popup_text, fill =True).add_to(marker_cluster)
#show the map
world_map


# In[ ]:




