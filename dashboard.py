import streamlit as st
import pandas as pd
import sys
from pathlib import Path

project_root = Path.cwd().parent
sys.path.insert(0, str(project_root))

from utils.map_functions import create_applications_to_turkey_map, create_applications_from_turkey_map
from utils.config import VISUALIZATIONS_DIR, CLEAN_DATA_DIR, CLEAN_DATASETS

st.set_page_config(
    page_title='Turkey Migration Analysis',
    page_icon='🗺️',
    layout='wide'
)

st.title('🗺️ Turkey Migration Analysis Dashboard')
st.markdown("""
Interactive exploration of refugee and asylum seeker flows involving Turkey from 2000-2025.  
This dashboard examines Turkey's unique dual role as both a major refugee host country and a source of asylum seekers.
""")

st.sidebar.header('About This Project')
st.sidebar.info(
    """
    **Data Source:** UNHCR Population Statistics Database
    
    This analysis explores:
    - Refugees seeking asylum **IN** Turkey (mainly from Syria, Iraq, Afghanistan)
    - Turkish citizens seeking asylum **abroad** (post-2016 surge)
    
    **Note:** Post-2018 data for applications TO Turkey is incomplete due to Turkey's 
    shift to "Temporary Protection" status for many refugees.
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Key Findings:**")
st.sidebar.markdown("""
**Turkey as Refugee Host (2011-2018):**
- 🔴 Syrian crisis peaked at ~130k applications in 2015
- Recognition rates varied widely by nationality

**Turkey as Origin Country (2016-present):**
- 🟠 Initial surge after 2016 coup attempt
- 📈 Dramatic increase 2021-2023 (economic crisis, political repression)
- Applications peaked at ~150k in 2023
""")

with st.expander("⚠️ Data Limitations & Important Context"):
    st.markdown("""
    ### Data Completeness Issues
    
    **Syrian refugees:** This dataset captures formal asylum applications only. Turkey's ~3.6 million Syrian 
    refugees are under "Temporary Protection" status and not reflected in these numbers.
    
    **Missing recent data:** Some countries (Syria, Somalia) have incomplete data post-2018, likely due to 
    reporting changes or Turkey's shift to Temporary Protection policies.
    
    **Recognition vs. immigration:** Recognition rates reflect formal asylum/refugee decisions only, not other 
    immigration pathways (work visas, student visas, family reunification, etc.).
    
    ### Implications
    
    The "FROM Turkey" data (Turkish asylum seekers abroad) is more complete and reliable for recent years, 
    while "TO Turkey" data significantly underrepresents the true scale of Turkey's refugee population after 2018. 
    Comparisons after 2018 should be interpreted with caution.
    """)

@st.cache_data
def load_data():
    apps_to = pd.read_csv(CLEAN_DATA_DIR / CLEAN_DATASETS['apps_to_turkey'])
    apps_from = pd.read_csv(CLEAN_DATA_DIR / CLEAN_DATASETS['apps_from_turkey'])
    
    return apps_to, apps_from

apps_to_turkey, apps_from_turkey = load_data()


st.header('📊 Quick Stats')

col1, col2 = st.columns(2)

with col1:
    total_apps_to_turkey = apps_to_turkey['Number of Applications'].sum()
    st.metric('Total Applications TO Turkey', f"{total_apps_to_turkey:,}")

with col2:
    total_apps_from_turkey = apps_from_turkey['Number of Applications'].sum()
    st.metric('Total Applications FROM Turkey', f"{total_apps_from_turkey:,}")



st.header('🗺️ Interactive Maps')
st.markdown("""
Use the **year slider** on each map to see how refugee flows evolved over time.  
Hover over countries for detailed statistics including recognition rates.
""")

tab1, tab2 = st.tabs(['Applications TO Turkey', 'Applications FROM Turkey'])

with tab1:
    fig1 = create_applications_to_turkey_map()
    st.plotly_chart(fig1, width='stretch')

with tab2:
    fig2 = create_applications_from_turkey_map()
    st.plotly_chart(fig2, width='stretch')



st.header('📊 Detailed Analysis')
st.markdown("""
The following charts provide deeper statistical insights into application volumes, 
recognition rates by nationality, and temporal trends. Expand each section to explore.
""")

with st.expander('🔍 Turkey as a Refugee Host Country'):
    st.image(VISUALIZATIONS_DIR / 'to_turkey_analysis.png', width='stretch')
    st.caption("""
    **Key Insights:** Afghanistan sent the most applications overall (~389k), followed by Iraq (~301k).  
    Syria has the highest recognition rate among top applicant countries (~93%), with others varying significantly.
    """)

with st.expander('🔍 Turkey as an Origin Country'):
    st.image(VISUALIZATIONS_DIR / 'from_turkey_analysis.png', width='stretch')
    st.caption("""
    **Key Insights:** Germany received the most Turkish asylum applications (~350k), followed by France.  
    Recognition rates vary widely by destination country, with Canada showing the highest acceptance rate.
    """)

with st.expander("🔍 Comparative Analysis: Turkey's Dual Role"):
    st.image(VISUALIZATIONS_DIR / 'comparison_analysis.png', width='stretch')
    st.caption("""
    **Key Insight:** The crossover point occurred around 2021-2023, when Turkish citizens seeking asylum abroad 
    began to exceed refugees seeking protection in Turkey (in formal applications tracked by UNHCR).
    """)
    
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    📓 <a href='https://github.com/oganbayril/turkey-asylum-analysis' target='_blank'>View on GitHub</a> 
    for detailed methodology and Jupyter notebooks<br>
    Data: UNHCR Population Statistics Database | Analysis: 2000-2025
</div>
""", unsafe_allow_html=True)