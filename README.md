# 🗺️ Urban Accessibility Analysis - Qazvin Public Transport
**An interactive web-based dashboard for analyzing and visualizing public transport accessibility in Qazvin, Iran.**

<img width="1793" height="869" alt="Screenshot 2025-11-08 060101" src="https://github.com/user-attachments/assets/170f38d5-7c84-417e-8adf-cdef7e072463" />
<img width="1806" height="864" alt="Screenshot 2025-11-08 060131" src="https://github.com/user-attachments/assets/90650c56-e9a7-4be5-b5ff-f92605c19301" />

## 📖 Overview

This project provides a **Streamlit-powered dashboard** for evaluating **urban accessibility via public transport** in the city of **Qazvin**.  
It implements gravity-based accessibility models using **exponential** and **Gaussian impedance functions**, and supports:

- 🗺️ Interactive choropleth maps of accessibility for each type of destination  
- ⚙️ Adjustable impedance function parameters (β, μ, σ)  
- 🎯 Aggregated multi-destination accessibility analysis with weighted trip generation rates  
- 🚌 Optional visualization of public transport routes  
- 📊 Interactive statistics and map-based analytics  

The dashboard enables **urban planners and transport analysts** to explore accessibility inequalities and spatial patterns efficiently.

---

## 🧰 Technologies Used

- **Streamlit** — Web-based interactive dashboard  
- **GeoPandas** — Geospatial data processing  
- **Plotly (Graph Objects & Express)** — Dynamic map visualizations  
- **Matplotlib** — Impedance function plots  
- **NumPy / Pandas** — Data manipulation and analysis  
- **SciPy (norm.cdf)** — Gaussian impedance computation  

---

## 🗂️ Destination Types
The application analyzes accessibility to 14 destination categories:

| Category | Emoji | Description |
|----------|-------|-------------|
| Chain Stores | 🛒 | Major retail chains and supermarkets |
| Fruit Markets | 🍒 | Fresh produce markets |
| Clothing Complexes | 👔 | Shopping centers for clothing |
| Mobile Complexes | 📲 | Electronics and mobile phone shops |
| Cinemas | 🎬 | Movie theaters |
| Parks | 🛝 | Public parks and green spaces |
| Sports Complexes | 🏟️ | Sports facilities and gyms |
| Banks | 🏦 | Banking institutions |
| Schools | 🏫 | Educational institutions |
| Cultural Centers | 🏛️ | Community and cultural facilities |
| Mosques | 🕌 | Places of worship |
| Health Centers | 🩺 | Primary healthcare facilities |
| Public Hospitals | 🏨 | Public healthcare institutions |
| Private Hospitals | 🏥 | Private healthcare institutions |

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ali8D/qaz_acc_dashboard.git
   cd qaz_acc_dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify data structure**
   Ensure your project structure looks like this:
   ```
   qazvin-accessibility/
   ├── access_streamlit.py          # Main application
   ├── requirements.txt              # Dependencies
   ├── README.md                     # This file
   │
   └── data_qaz/
       ├── zones_areas2.geojson
       ├── BusRoutes_for_Streamlit.geojson
       ├── img_TransitNetwork.png
       │
       └── input/
           ├── traveltime_cen_to_opps/
           │   ├── qaz_mx_chainstores.csv
           │   ├── qaz_mx_FruitMarkets.csv
           │   └── ... (other CSV files)
           │
           └── opps_points/
               ├── chain_stores/geojson/
               ├── fruit_markets/geojson/
               └── ... (other geojson folders)
   ```

## 🎮 Usage

### Running the Application

```bash
streamlit run qaz_acc_dashboard.py
```

The app will automatically open in your browser at `http://localhost:8501`
