import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .config import CLEAN_DATA_DIR, CLEAN_DATASETS

def create_applications_to_turkey_map():
    """Create the Applications TO Turkey choropleth map"""
    
    apps_from_turkey = pd.read_csv(CLEAN_DATA_DIR / CLEAN_DATASETS['apps_to_turkey'])
    decisions_turkey = pd.read_csv(CLEAN_DATA_DIR / CLEAN_DATASETS['decisions_turkey'])
    
    apps_to_turkey_by_country = apps_from_turkey.groupby(['Country of Origin Name', 'Country of Origin Code', 'Year'])['Number of Applications'].sum().reset_index()

    recognition_data_turkey = decisions_turkey.groupby(['Country of Origin Name', 'Year']).agg({
        'Recognized': 'sum',
        'Total Decided': 'sum'
    }).reset_index()

    recognition_data_turkey['Recognition Rate'] = (
        recognition_data_turkey['Recognized'] / recognition_data_turkey['Total Decided'] * 100
    ).round(1)


    apps_to_turkey_by_country = apps_to_turkey_by_country.merge(
        recognition_data_turkey[['Country of Origin Name', 'Year', 'Recognition Rate']], 
        on=['Country of Origin Name', 'Year'], 
        how='left'  # Left join so we keep all applications even if no decision data
    )

    apps_to_turkey_by_country['Recognition Rate'] = apps_to_turkey_by_country['Recognition Rate'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else 'No data'
    )

    apps_to_turkey_by_country.columns = ['Country', 'ISO_Code', 'Year', 'Applications', 'Recognition Rate']
    apps_to_turkey_by_country = apps_to_turkey_by_country.sort_values(['Year', 'Country']).reset_index(drop=True)

    # Cut off at 2018 because of the Temporary Protection status of migrants after 2018 which caused data incompleteness.
    apps_to_turkey_by_country_filtered = apps_to_turkey_by_country[apps_to_turkey_by_country['Year'] <= 2018]

    fig = px.choropleth(
        apps_to_turkey_by_country_filtered,
        locations='ISO_Code',                 
        color='Applications',              
        hover_name='Country',
        animation_frame='Year',
        hover_data={'ISO_Code': False,
                    'Year': False,
                    'Applications': ':,',
                    'Recognition Rate': True
                    },
        color_continuous_scale='Viridis',       
        labels={'Applications': 'Applications',
                'Recognition Rate': 'Recognition Rate'},
        title='Asylum Applications to Turkey by Origin Country (2000-2018)'
    )

    fig.update_geos(
        fitbounds='locations',
        visible=False,
        showcountries=True
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        height=600
    )

    fig.update_coloraxes(
        colorbar=dict(
            title='Number of<br>Applications',
            thickness=15,
            len=0.7
        )
    )

    fig.add_trace(
        go.Choropleth(
            locations=['TUR'],
            z=[0],
            colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],  # Transparent fill
            showscale=False,
            marker_line_color='red',
            marker_line_width=2,
            text=['Turkey (Destination)'],
            hoverinfo='text',
        )
    )

    fig.add_annotation(
        text='Source: UNHCR Population Statistics Database',
        xref='paper', yref='paper',
        x=0, y=-0.1,
        showarrow=False,
        font=dict(size=10, color='gray')
    )
    
    return fig

def create_applications_from_turkey_map():
    """Create the Applications FROM Turkey choropleth map"""
    
    apps_from_turkey = pd.read_csv(CLEAN_DATA_DIR / CLEAN_DATASETS['apps_from_turkey'])
    decisions_from_others = pd.read_csv(CLEAN_DATA_DIR / CLEAN_DATASETS['decisions_others'])
    
    apps_from_turkey_by_country = apps_from_turkey.groupby(['Country of Asylum Name', 'Country of Asylum Code', 'Year'])['Number of Applications'].sum().reset_index()

    recognition_data_others = decisions_from_others.groupby(['Country of Asylum Name', 'Year']).agg({
        'Recognized': 'sum',
        'Total Decided': 'sum'
    }).reset_index()

    recognition_data_others['Recognition Rate'] = (
        recognition_data_others['Recognized'] / recognition_data_others['Total Decided'] * 100
    ).round(1)

    apps_from_turkey_by_country = apps_from_turkey_by_country.merge(
        recognition_data_others[['Country of Asylum Name', 'Year', 'Recognition Rate']],
        on=['Country of Asylum Name', 'Year'],
        how='left'
    )

    apps_from_turkey_by_country['Recognition Rate'] = apps_from_turkey_by_country['Recognition Rate'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else 'No Data'
    )

    apps_from_turkey_by_country.columns = ['Country', 'ISO_Code', 'Year', 'Applications', 'Recognition Rate']
    apps_from_turkey_by_country = apps_from_turkey_by_country.sort_values(['Year', 'Country']).reset_index(drop=True) # Sort by year first so the map slider is accurate
    
    fig2 = px.choropleth(
        apps_from_turkey_by_country,
        locations='ISO_Code',
        color='Applications',
        hover_name='Country',
        animation_frame='Year',
        hover_data={'ISO_Code': False,
                    'Year': False,
                    'Applications': ':,',
                    'Recognition Rate': True
                    },
        color_continuous_scale='Viridis',
        labels={'Applications': 'Applications',
                'Recognition Rate': 'Recognition Rate'},
        title='Asylum Applications from Turkey by Destination Country (2000-2025)'
    )

    fig2.update_geos(
        visible=False,
        showcountries=True
    )

    fig2.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        height=600
    )

    fig2.update_coloraxes(
        colorbar=dict(
            title='Number of<br>Applications',
            thickness=15,
            len=0.7
        )
    )

    fig2.add_trace(
        go.Choropleth(
            locations=['TUR'],
            z=[0],
            colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],  # Transparent fill
            showscale=False,
            marker_line_color='orange',
            marker_line_width=2,
            text=['Turkey (Origin)'],
            hoverinfo='text',
        )
    )

    fig2.add_annotation(
        text='Source: UNHCR Population Statistics Database',
        xref='paper', yref='paper',
        x=0, y=-0.1,
        showarrow=False,
        font=dict(size=10, color='gray')
    )

    return fig2