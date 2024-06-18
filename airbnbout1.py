#Import the necessary library
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.graph_objects as go                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
import seaborn as sns
import matplotlib.pyplot as plt

#Read csv files
df = pd.read_csv("E:/Data scientist/Airbnb/airbnb_analysis.csv")

st.sidebar.image(r"E:/Data scientist/Airbnb/images.png",use_column_width=600) #airbnb Image

st.write(" ")
st.write(" ")
st.write(" ")
st.markdown("""
                <style>
                .centered-text {
                    text-align: center;
                    font-style:'Arial', sans-serif;
                    font-weight: bold;
                    font-size: 100px; 
                    pointer-events: none;
                }
                </style>
                <div class="centered-text">
                    Airbnb Analysis
                </div>
                """, unsafe_allow_html=True)    
  
Options = st.sidebar.radio("Options", ("Home", "Analysis", "Insights"))

if Options=="Home":

    st.write(" ") 
    st.write(" ")     
    st.markdown("#### :red[*Overview:* ]")
    st.markdown("##### This project aims to analyze Airbnb data with help of perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends in this market field.")

    st.markdown("#### :red[*Domain:* ] ")
    st.markdown(" ##### Travel Industry, Property Management and Tourism ")
    st.markdown("""
                #### :red[*Skills take away:*]    
        
                ##### Python scripting, Data Preprocessing, Visualization,EDA, Streamlit

                """)
    
elif Options=="Analysis":
    st.write(" ")

    col,col1,col2,col3= st.columns([3,3,3,3])  

    with col:
        on = st.checkbox("##### Price Analysis")

        if on:
            
            st.write(" ") #Price vs Number of Amenities
            df["num_amenities"] = df['Amenities'].apply(lambda x: len(x.split(',')))
            fig = px.scatter(df, x='num_amenities', y='Price', title='Price vs. Number of Amenities')
            st.plotly_chart(fig)
            
            #Average price for each property
            avg_price_by_type = df.groupby("Property_type")["Price"].mean()
            fig = px.line(
                avg_price_by_type.reset_index(),
                x="Property_type",
                y="Price",
                title="Average Price for each Property",width=1300,height=700,
                labels={"Property_type": "Property Type", "Price": "Average Price"},
            )
            fig.update_traces(mode='markers+lines') 
            fig.update_layout(xaxis_title='Property Type', yaxis_title='Average Price')
            st.plotly_chart(fig)
            
            #Average price by city
            avg_price_by_location = df.groupby("Host_neighbourhood")["Price"].mean().reset_index()

            fig = px.strip(avg_price_by_location, x="Host_neighbourhood", y="Price", color="Host_neighbourhood",
                        title="Average Price by City",
                        labels={"Host_neighbourhood": "Host Neighbourhood", "Price": "Average Price"},
                        width=1410, height=700)

            st.plotly_chart(fig)
            
            
    with col1:
        on = st.checkbox("##### Avalaibility Analysis")

        if on:
            st.write(" " )
            #Average Availability by Property Type
            avg_prop_avail = df.groupby("Property_type")["Availability_365"].mean().reset_index()
            fig = px.line(avg_prop_avail, x="Property_type", y="Availability_365", markers=True,
                        title="Average Availability by Property Type",
                        labels={"Property_type": "Property Type", "Availability_365": "Average Availability (Days)"},
                        width=1300, height=700)

            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig)
            
            #Average Availability by Room Type
            avg_availability_by_room_type = df.groupby('Room_type')['Availability_365'].mean().reset_index()

            fig = px.pie(avg_availability_by_room_type, values='Availability_365', names='Room_type',
                                title='Average Availability by Room Type', width=1300,height=700,)
            st.plotly_chart(fig)
            
            #Average Price by Cancellation Policy
            avg_price_by_policy = df.groupby('Cancellation_policy')['Price'].mean().sort_values(ascending=False)
            fig = px.bar(
                avg_price_by_policy,
                x=avg_price_by_policy.index,
                y=avg_price_by_policy.values,
                title="Average Price by Cancellation Policy",
                labels={'x': 'Cancellation Policy', 'y': 'Average Price ($)', 'Price':'Average Price ($)'},  # Labels for x and y-axis
                width=1300,
                height=700
            )
            
            st.plotly_chart(fig)
            
    with col2:
        on = st.checkbox("##### Location Analysis")

        if on:
            #Distribution of Property Types Across Neighborhoods
            property_type_distribution = df.groupby(['suburb', 'Property_type']).size().reset_index(name='count')

            fig = px.scatter(property_type_distribution, x='suburb', y='count', color='Property_type',
                            title='Distribution of Property Types Across Neighborhoods',width=1110,height=700,
                            labels={'count': 'Number of Listings', 'suburb': 'Neighborhood'})
            fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Number of Listings')
            st.plotly_chart(fig)
            
            #Top and Least 10 Neighborhoods by Average Review Score
            avg_review_score_by_neighborhood = df.groupby('suburb')['Review_scores'].mean().reset_index()
            top_10_neighborhoods = avg_review_score_by_neighborhood.sort_values(by='Review_scores', ascending=False).head(10)
            top_10_neighborhoods['Rank'] = 'Top 10'
            least_10_neighborhoods = avg_review_score_by_neighborhood.sort_values(by='Review_scores', ascending=True).head(10)
            least_10_neighborhoods['Rank'] = 'Least 10'
            merged_neighborhoods = pd.concat([top_10_neighborhoods, least_10_neighborhoods])
            fig = px.bar(merged_neighborhoods, x='suburb', y='Review_scores', color='Rank',
                        labels={'Review_scores': 'Average Review Score'},
                        title='Top and Least 10 Neighborhoods by Average Review Score',width=1200,height=700,
                        color_discrete_sequence=px.colors.qualitative.Pastel)

            fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Average Review Score')
            st.plotly_chart(fig)

            #Top Amenities Offered in Listings Across Different Neighborhoods
            amenities = df['Amenities'].str.replace('[{}]', '').str.replace('"', '').str.split(',')
            amenity_counts = {}
            for amns in amenities:
                for amenity in amns:
                    if amenity.strip() in amenity_counts:
                        amenity_counts[amenity.strip()] += 1
                    else:
                        amenity_counts[amenity.strip()] = 1
            sorted_amenities = sorted(amenity_counts.items(), key=lambda x: x[1], reverse=True)
            top_n = 10
            top_amenities = dict(sorted_amenities[:top_n])

            
            fig = go.Figure(go.Bar(
                x=list(top_amenities.values()),
                y=list(top_amenities.keys()),
                orientation='h',   
                marker=dict(color='royalblue'),  
            ))

            fig.update_layout(
                title='Top Amenities Offered in Listings Across Different Neighborhoods',
                xaxis_title='Count',
                yaxis_title='Amenity',
                width=1000,
                height=700,
            )

            st.plotly_chart(fig)     
    
    with col3:
        on = st.checkbox("##### Geo visualisation")
        if on:
            #Listing Availability by Location
            df_filtered = df[df['Availability_365'] < 365]
            fig = px.scatter_mapbox(df_filtered, lat="Latitude", lon="Longitude", color="Availability_365",
                                    hover_name="suburb", hover_data={"suburb": True, "market": True, "Country": True, "Availability_365": True},
                                    color_continuous_scale=px.colors.sequential.Viridis,
                                    zoom=1,width=1300,height=700)
            fig.update_layout(mapbox_style="open-street-map", title="Listing Availability by Location")
            st.plotly_chart(fig)
            

elif Options=="Insights":
        st.markdown(
    """
    <style>
        .css-15qegpx {
            display: flex;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
                
        title=st.selectbox("Select one of these",
                                    ["Choose a Title...",
                                     '1.Top 10 Most Common Amenities Provided in Listings',
                                     '2.Top 10 Countries with the Most Listings',
                                     '3.Neighborhoods with the Highest Number of Listings',
                                     '4.Distribution of Average Review Scores for Top Hosts',
                                     '5.Number of Available Listings in the Next 30 Days by City'],
                                    index=0)
          
        if title=='1.Top 10 Most Common Amenities Provided in Listings':
            all_amenities = ', '.join(df['Amenities'])
            amenities_list = [amenity.strip() for amenity in all_amenities.split(',')]
            amenity_counts = pd.Series(amenities_list).value_counts().reset_index()
            amenity_counts.columns = ['Amenity', 'Count']

            top_10_common_amenities = amenity_counts.head(10)

            fig = px.pie(top_10_common_amenities, values='Count', names='Amenity',
                        title='Top 10 Most Common Amenities Provided in Listings', width=1300,height=700)
            st.plotly_chart(fig)
            
            
        elif title=="2.Top 10 Countries with the Most Listings":
            listings_by_country = df['Country'].value_counts().reset_index()
            listings_by_country.columns = ['Country', 'Number of Listings']
            listings_by_country = listings_by_country.sort_values(by='Number of Listings', ascending=False)
            top_10_countries = listings_by_country.head(10)
            
            fig = px.bar(
                top_10_countries,
                x='Country',
                y='Number of Listings',
                title='Top 10 Countries with the Most Listings',
                labels={'Number of Listings': 'Number of Listings', 'Country': 'Country'},
                width=1300,
                height=700,
            )
            st.plotly_chart(fig)
            
        elif title=='3.Neighborhoods with the Highest Number of Listings':
            neighborhood_counts = df['Host_neighbourhood'].value_counts().reset_index()
            neighborhood_counts.columns = ['Neighborhood', 'Number of Listings']
            neighborhood_counts = neighborhood_counts.sort_values(by='Number of Listings', ascending=False)
          
            fig = px.bar(neighborhood_counts.head(10), x='Neighborhood', y='Number of Listings',
                                labels={'Neighborhood': 'Neighborhood', 'Number of Listings': 'Number of Listings'},
                                title='Neighborhoods with the Highest Number of Listings', width=1300,height=700,color='Number of Listings',color_continuous_scale= "plasma")
                    
            st.plotly_chart(fig)
            
        elif title=='4.Distribution of Average Review Scores for Top Hosts':
            
            avg_review_scores_by_host = df.groupby('Host_id')['Review_scores'].mean().reset_index()
            avg_review_scores_by_host = avg_review_scores_by_host.sort_values(by='Review_scores', ascending=False)
            top_hosts = avg_review_scores_by_host.head(10)

            fig = px.pie(top_hosts, values='Review_scores', names='Host_id',
                        title='Distribution of Average Review Scores for Top Hosts', width=1300,height=700,color='Host_id',
                        hole=0.4)  
            st.plotly_chart(fig)
            
        elif title=='5.Number of Available Listings in the Next 30 Days by City':
            availability_30_by_city = df.groupby('market')['Availability_30'].sum().reset_index()
            availability_30_by_city_sorted = availability_30_by_city.sort_values(by='Availability_30', ascending=False)

            fig = px.bar(availability_30_by_city_sorted, x='market', y='Availability_30',color="Availability_30",color_continuous_scale='oryel',
                        title='Number of Available Listings in the Next 30 Days by City', width=1300,height=700,
                        labels={'market': 'City', 'Availability_30': 'Available'})

            fig.update_layout(xaxis_title='City', yaxis_title='Available')
            st.plotly_chart(fig)
