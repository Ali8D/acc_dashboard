import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Urban Accessibility Analysis - Qazvin",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 6px;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown('<div class="main-header">🗺️ Analysis of Accessibility via Public Transport in Qazvin</div>', unsafe_allow_html=True)

# Destination type mapping
destination_mapping = {
    '🛒Chain Stores': ('qaz_mx_chainstores.csv', 'accessibility_to_ChainStores', 'chain_stores/geojson/edited/final_chain_stores.geojson', 'brand_en'),
    '🍒Fruit Markets': ('qaz_mx_FruitMarkets.csv', 'accessibility_to_FruitMarkets', 'fruit_markets/geojson/edited/fruit_markets.geojson', 'name:en'),
    '👔Clothing Complexes': ('qaz_mx_ClothingComplexes.csv', 'accessibility_to_ClothingComplexes', 'Clothing_complexes/geojson/edited/Clothing_complexes.geojson', 'name:en'),
    '📲Mobile Complexes': ('qaz_mx_MobileComplexes.csv', 'accessibility_to_MobileComplexes', 'mobile_centers/geojson/mobile_centers.geojson', 'name:en'),
    '🎬Cinemas': ('qaz_mx_cinemas.csv', 'accessibility_to_cinemas', 'cinemas/geojson/cinemas.geojson', 'name:en'),
    '🛝Parks': ('qaz_mx_Parks.csv', 'accessibility_to_parks', 'parks/geojson/edited/parks.geojson', 'name:en'),
    '🏟️Sports Complexes': ('qaz_mx_Sports.csv', 'accessibility_to_sports', 'sports/geojson/sports.geojson', 'name:en'),
    '🏦Banks': ('qaz_mx_banks.csv', 'accessibility_to_banks', 'banks/geojson/banks.geojson', 'name:en'),
    '🏫Schools': ('qaz_mx_Schools.csv', 'accessibility_to_schools', 'schools/geojson/schools.geojson', 'name'),
    '🏛️Cultural Centers': ('qaz_mx_CommunityCenters.csv', 'accessibility_to_CulturalCenters', 'community_centers/geojson/community_centers.geojson', 'name:en'),
    '🕌Mosques': ('qaz_mx_PlacesOfWorship.csv', 'accessibility_to_mosques', 'places_of_worship/geojson/places_of_worship.geojson', 'name:en'),
    '🩺Health Centers': ('qaz_mx_HealthCenters.csv', 'accessibility_to_HealthCenters', 'health_centers/geojson/edited/health_centers.geojson', 'name:en'),
    '🏨Public Hospitals': ('qaz_mx_public_hospitals.csv', 'accessibility_to_PublicHospitals', 'hospitals/geojson/Separatedby_public_or_private/public_hospitals.geojson', 'name:en'),
    '🏥Private Hospitals': ('qaz_mx_private_hospitals.csv', 'accessibility_to_PrivateHospitals', 'hospitals/geojson/Separatedby_public_or_private/private_hospitals.geojson', 'name:en')
}

# Visualization type
viz_type = st.sidebar.radio(
    "🎨 Select visualization mode:",
    ["Individual Destinations", "Aggregate Accessibility"],
    help="Show individual destination accessibility or combined weighted accessibility"
)

# Add destination selector for Individual Destinations mode
destination_to_show = None
if viz_type == "Individual Destinations":
    destination_to_show = st.sidebar.selectbox(
        "Select destination to visualize:",
        options=list(destination_mapping.keys())
    )

st.sidebar.markdown("---")

# Impedance function type selection
impedance_type = st.sidebar.selectbox(
    "📈 Select Impedance Function:",
    ["Exponential", "Gaussian"],
    help="Choose the type of distance decay function"
)

# Get parameters for Gaussian
travel_time_mean = 40.64907
travel_time_std = 14.55334
max_travel_time = 89.0

# Parameters section based on impedance type
if impedance_type == "Exponential":
    # Beta parameter input
    beta = st.sidebar.number_input(
        "Exponential Decay Coefficient (β):",
        min_value=0.0,
        max_value=1.0,
        value=0.1068,
        step=0.1,
        format="%.4f",
        help="The exponential impedance function is: exp(-β × travel_time)"
    )
    
    # Show impedance function plot
    max_time = 60
    travel_times = np.linspace(0, max_time, 1000)
    impedance_values = np.exp(-beta * travel_times)
    
    fig_sidebar, ax_sidebar = plt.subplots(figsize=(4, 2.5))
    ax_sidebar.plot(travel_times, impedance_values, linewidth=2, color='#2C3E50')
    ax_sidebar.set_xlabel('Time (min)', fontsize=8)
    ax_sidebar.set_ylabel('f(t) = e^(-βt)', fontsize=8)
    ax_sidebar.set_title(f'β = {beta:.4f}', fontsize=9, fontweight='bold')
    ax_sidebar.grid(True, alpha=0.3)
    ax_sidebar.tick_params(labelsize=7)
    plt.tight_layout()
    st.sidebar.pyplot(fig_sidebar)
    plt.close()

else:  # Gaussian
    st.sidebar.text(f"Gaussian Parameters:")
    st.sidebar.info(f"Mean (μ): {travel_time_mean:.2f} min\n\nStd Dev (σ): {travel_time_std:.2f} min")
    
    # Show impedance function plot
    max_time = max_travel_time
    travel_times = np.linspace(0, max_time, 1000)
    impedance_values = 1 - norm.cdf(travel_times, loc=travel_time_mean, scale=travel_time_std)
    
    fig_sidebar, ax_sidebar = plt.subplots(figsize=(4, 2.5))
    ax_sidebar.plot(travel_times, impedance_values, linewidth=2, color='#2C3E50')
    ax_sidebar.set_xlabel('Time (min)', fontsize=8)
    ax_sidebar.set_ylabel('f(t) = 1 - Φ(t)', fontsize=8)
    ax_sidebar.set_title(f'μ={travel_time_mean:.1f}, σ={travel_time_std:.1f}', fontsize=8, fontweight='bold')
    ax_sidebar.grid(True, alpha=0.3)
    ax_sidebar.tick_params(labelsize=7)
    plt.tight_layout()
    st.sidebar.pyplot(fig_sidebar)
    plt.close()
    
    beta = None  # Not used for Gaussian


# Multi-select for destinations (for Aggregate mode)
if viz_type == "Aggregate Accessibility":
    st.sidebar.markdown("---")
    selected_destinations = st.sidebar.multiselect(
        "🎯 Select destination types to include:",
        options=list(destination_mapping.keys()),
        default=list(destination_mapping.keys()),
        help="Select one or more destination types to calculate accessibility"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.text("📊 Trip Generation Rates (Weights)", help="The default values ​​are the average peak hour passenger-trip generation rates, derived from the local standard equivalent to ITE.")
    default_weights = {
        '🛒Chain Stores': 1201.76,
        '🍒Fruit Markets': 2042.133,
        '👔Clothing Complexes': 5066.175,
        '📲Mobile Complexes': 2253.2,
        '🎬Cinemas': 531.0,
        '🛝Parks': 2267.6362,
        '🏟️Sports Complexes': 580.8,
        '🏦Banks': 191.7,
        '🏫Schools': 193.14,
        '🏛️Cultural Centers': 3640.56,
        '🕌Mosques': 447.32,
        '🩺Health Centers': 503.0,
        '🏨Public Hospitals': 1994.3,
        '🏥Private Hospitals': 632.1
    }
    
    # Create weight inputs as sliders
    weights = {}
    for destination, default_value in default_weights.items():
        weights[destination] = st.sidebar.slider(
            destination,
            min_value=0.0,
            max_value=10000.0,
            value=default_value,
            step=10.0,
            format="%.2f"
        )

# Add bus lines toggle
st.sidebar.markdown("---")
show_bus_lines = st.sidebar.toggle(
    "Show *public transport routes* on map 🚌",
    value=False,
    help="Toggle to display public transport routes layer on the map"
)

# Load base data
@st.cache_data
def load_base_data():
    qazvin_zoning_map = gpd.read_file("data_qaz/zones_areas2.geojson")
    qazvin_zoning_map['dauid'] = qazvin_zoning_map['dauid'].astype(int)
    # Ensure it's in WGS84 (EPSG:4326) for Plotly
    if qazvin_zoning_map.crs is not None and qazvin_zoning_map.crs != "EPSG:4326":
        qazvin_zoning_map = qazvin_zoning_map.to_crs("EPSG:4326")
    return qazvin_zoning_map

# Load bus lines data
@st.cache_data
def load_bus_lines():
    try:
        bus_lines = gpd.read_file("data_qaz/BusRoutes_for_Streamlit.geojson")
        # Reproject to WGS84 (EPSG:4326) if needed
        if bus_lines.crs is not None and bus_lines.crs != "EPSG:4326":
            bus_lines = bus_lines.to_crs("EPSG:4326")
        return bus_lines
    except Exception as e:
        st.warning(f"Could not load bus lines: {str(e)}")
        return None

# Calculate accessibility for a single destination type
def calculate_accessibility(travel_time_file, beta, opportunity_weight=1):
    try:
        dtypes = {'from_id': int, 'travel_time': float}
        mx = pd.read_csv(f'data_qaz/input/traveltime_cen_to_opps/{travel_time_file}', dtype=dtypes)
        
        # Apply impedance function based on type
        if impedance_type == "Exponential":
            mx['impedance'] = np.exp(-beta * mx['travel_time'])
        else:  # Gaussian
            mx['impedance'] = 1 - norm.cdf(mx['travel_time'], loc=travel_time_mean, scale=travel_time_std)
        
        # Apply opportunity weight
        mx['opportunity'] = opportunity_weight
        mx['weighted_impedance'] = mx['impedance'] * mx['opportunity']
        
        # Sum over all destinations for each origin
        access = mx.groupby('from_id', as_index=False)['weighted_impedance'].sum()
        
        return access
    except Exception as e:
        st.error(f"Error loading {travel_time_file}: {str(e)}")
        return None

# Updated function to include bus lines
def create_choropleth_map(gdf, access_column, title, points_gdf=None, tooltip_col=None, bus_lines_gdf=None):
    # Prepare hover data
    gdf['hover_text'] = gdf.apply(
        lambda row: f"Zone ID: {row['dauid']}<br>Accessibility: {row[access_column]:.2f}",
        axis=1
    )
    
    # Create the choropleth map
    fig = px.choropleth_mapbox(
        gdf,
        geojson=gdf.geometry.__geo_interface__,
        locations=gdf.index,
        color=access_column,
        hover_data={'hover_text': True},
        color_continuous_scale='Plasma_r',
        mapbox_style='open-street-map',
        zoom=12,
        center={'lat': gdf.geometry.centroid.y.mean(), 'lon': gdf.geometry.centroid.x.mean()},
        opacity=0.7,
        labels={access_column: 'Accessibility'}
    )
    
    # Update hover template
    fig.update_traces(
        hovertemplate='%{customdata[0]}<extra></extra>',
        customdata=gdf[['hover_text']].values
    )
    
    # Add bus lines if provided
    if bus_lines_gdf is not None:
        for idx, row in bus_lines_gdf.iterrows():
            if row.geometry is not None and row.geometry.geom_type == 'LineString':
                coords = list(row.geometry.coords)
                lons = [coord[0] for coord in coords]
                lats = [coord[1] for coord in coords]
                
                # Get line name if available ('line_name' column)
                line_name = "Bus Line"
                if 'line_name' in row and pd.notna(row['line_name']):
                    line_name = str(row['line_name'])
                elif 'name' in row and pd.notna(row['name']):
                    line_name = str(row['name'])
                
                fig.add_trace(go.Scattermapbox(
                    lon=lons,
                    lat=lats,
                    mode='lines',
                    line=dict(width=2, color='blue'),
                    text=line_name,
                    hovertemplate=f'<b>{line_name}</b><extra></extra>',
                    name='Public Transport Routes',
                    showlegend=(idx == 0),  # Only show legend for first line
                    legendgroup='Public_Transport_Routes'
                ))
            elif row.geometry is not None and row.geometry.geom_type == 'MultiLineString':
                # Handle MultiLineString geometry
                for line in row.geometry.geoms:
                    coords = list(line.coords)
                    lons = [coord[0] for coord in coords]
                    lats = [coord[1] for coord in coords]
                    
                    line_name = "Bus Line"
                    if 'name' in row:
                        line_name = str(row['name'])
                    elif 'route' in row:
                        line_name = f"Route {row['route']}"
                    
                    fig.add_trace(go.Scattermapbox(
                        lon=lons,
                        lat=lats,
                        mode='lines',
                        line=dict(width=2, color='blue'),
                        text=line_name,
                        hovertemplate=f'<b>{line_name}</b><extra></extra>',
                        name='Bus Lines',
                        showlegend=(idx == 0),
                        legendgroup='bus_lines'
                    ))
    
    # Add points if provided
    if points_gdf is not None and tooltip_col is not None:
        lats = []
        lons = []
        names = []
        for idx, row in points_gdf.iterrows():
            if row.geometry is not None:
                lats.append(row.geometry.y)
                lons.append(row.geometry.x)
                if tooltip_col in row:
                    names.append(str(row[tooltip_col]))
                else:
                    names.append("Unknown")
        
        fig.add_trace(go.Scattermapbox(
            lon=lons,
            lat=lats,
            mode='markers',
            marker=dict(
                size=12, 
                color="black",
                opacity=0.95,
                symbol='circle'
            ),
            text=names,
            hovertemplate='<b>%{text}</b><extra></extra>',
            name='Destinations',
            showlegend=True
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=16)
        ),
        height=800,
        margin=dict(l=0, r=0, t=100, b=0),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )
    
    return fig

# Main application logic
try:
    # Load base map first
    qazvin_zoning_map = load_base_data()
    
    # Load bus lines if toggle is on
    bus_lines_gdf = None
    if show_bus_lines:
        bus_lines_gdf = load_bus_lines()
    
    if viz_type == "Individual Destinations":
        if destination_to_show:
            with st.spinner(f'Calculating accessibility to {destination_to_show}...'):
                file_info = destination_mapping[destination_to_show]
                travel_time_file, access_col, points_file, tooltip_col = file_info
                
                # Calculate accessibility
                access_df = calculate_accessibility(travel_time_file, beta)
                
                if access_df is not None:
                    # Merge with map
                    map_data = qazvin_zoning_map.merge(
                        access_df.rename(columns={'weighted_impedance': access_col}),
                        left_on='dauid',
                        right_on='from_id',
                        how='left'
                    )
                    
                    # Load points
                    points_gdf = None
                    try:
                        points_gdf = gpd.read_file(f"data_qaz/input/opps_points/{points_file}")
                        if tooltip_col in points_gdf.columns:
                            points_gdf = points_gdf.rename(columns={tooltip_col: 'name_en'})
                            tooltip_col = 'name_en'
                    except Exception as e:
                        st.warning(f"Could not load points layer: {str(e)}")
                        points_gdf = None
                        tooltip_col = None
                    
                    # Create and display map - Added bus lines parameter
                    fig = create_choropleth_map(
                        map_data,
                        access_col,
                        f"Accessibility to <span style='color: purple;'>{destination_to_show}</span> in Qazvin",
                        points_gdf,
                        tooltip_col,
                        bus_lines_gdf
                    )
                    # Add border around plot
                    st.markdown(
                        """
                        <style>
                        .plot-container {
                            border: 2px solid #ddd;
                            border-radius: 5px;
                            padding: 10px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Min Accessibility", f"{map_data[access_col].min():.2f}",
                        help="Lowest accessibility value across all zones")
                    with col2:
                        st.metric("Mean Accessibility", f"{map_data[access_col].mean():.2f}",
                        help="Mean accessibility across all zones")
                    with col3:
                        st.metric("Max Accessibility", f"{map_data[access_col].max():.2f}",
                        help="Highest accessibility value across all zones")
    
    else:  # Aggregate Accessibility
        if not selected_destinations:
            st.warning("⚠️ Please select at least one destination type from the sidebar.")
        else:
            with st.spinner('Calculating aggregate accessibility...'):
                # Initialize merged dataframe
                merged_df = None
                total_weight = 0
                
                for dest_name in selected_destinations:
                    file_info = destination_mapping[dest_name]
                    travel_time_file = file_info[0]
                    weight = weights[dest_name]
                    
                    # Calculate accessibility
                    access_df = calculate_accessibility(travel_time_file, beta, opportunity_weight=weight)
                    
                    if access_df is not None:
                        access_df = access_df.rename(columns={'weighted_impedance': f'w_{dest_name}'})
                        
                        if merged_df is None:
                            merged_df = access_df
                        else:
                            merged_df = merged_df.merge(access_df, on='from_id', how='outer')
                        
                        total_weight += weight
                
                if merged_df is not None and total_weight > 0:
                    # Calculate total weighted accessibility
                    weight_cols = [col for col in merged_df.columns if col.startswith('w_')]
                    merged_df[weight_cols] = merged_df[weight_cols].fillna(0)
                    merged_df['total_weighted_access'] = merged_df[weight_cols].sum(axis=1)
                    merged_df['final_accessibility'] = merged_df['total_weighted_access'] / total_weight
                    
                    # Merge with map
                    map_data = qazvin_zoning_map.merge(
                        merged_df[['from_id', 'final_accessibility']],
                        left_on='dauid',
                        right_on='from_id',
                        how='left'
                    )
                    
                    # Fill any remaining NaN values
                    map_data['final_accessibility'] = map_data['final_accessibility'].fillna(0)
                    
                    # Check if we have valid data
                    if map_data['final_accessibility'].max() == 0:
                        st.error("❌ All accessibility values are zero. Please check your travel time data.")
                    else:
                        # Create and display map - MODIFICATION 2: Added bus lines parameter
                        fig = create_choropleth_map(
                            map_data,
                            'final_accessibility',
                            "Accessibility to Urban Opportunities in Qazvin via Public Transport",
                            None,
                            None,
                            bus_lines_gdf
                        )
                        
                        # Add border around plot
                        st.markdown(
                            """
                            <style>
                            .plot-container {
                                border: 2px solid #ddd;
                                border-radius: 5px;
                                padding: 10px;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                        # Show statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Min Accessibility", f"{map_data['final_accessibility'].min():.3f}")
                        with col2:
                            st.metric("Mean Accessibility", f"{map_data['final_accessibility'].mean():.3f}")
                        with col3:
                            st.metric("Max Accessibility", f"{map_data['final_accessibility'].max():.3f}")
                        
                        # Show selected destinations
                        st.subheader("📋 Selected Destinations & Weights")
                        dest_summary = pd.DataFrame({
                            'Destination': selected_destinations,
                            'Weight': [weights[d] for d in selected_destinations]
                        })
                        st.dataframe(dest_summary, use_container_width=True)
                else:
                    st.error("❌ Could not calculate accessibility. Please check that all data files are accessible.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
# Added image at the bottom
st.image("data_qaz/img_TransitNetwork.png", 
         caption="Qazvin Public Transport Network", 
         use_container_width=True)
st.markdown(''' **Accessibility Analysis Tool - Qazvin Urban Transit System** ''')
st.markdown(''' *Analyzing public transport accessibility patterns using gravity-based model* ''')
st.markdown("*Darvishvand & Kermanshah*")