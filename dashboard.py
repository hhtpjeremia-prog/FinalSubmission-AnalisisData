import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, 'data')

    day_df = pd.read_csv(os.path.join(data_path, 'day.csv'))
    hour_df = pd.read_csv(os.path.join(data_path, 'hour.csv'))

    # Cleaning
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {1: 'Cerah/Berawan', 2: 'Berkabut', 3: 'Hujan Ringan/Salju', 4: 'Hujan Lebat/Badai'}
    day_map = {0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'}

    day_df['season_label'] = day_df['season'].map(season_map)
    hour_df['season_label'] = hour_df['season'].map(season_map)
    day_df['weather_label'] = day_df['weathersit'].map(weather_map)
    hour_df['weather_label'] = hour_df['weathersit'].map(weather_map)
    day_df['weekday_name'] = day_df['weekday'].map(day_map)
    hour_df['weekday_name'] = hour_df['weekday'].map(day_map)

    day_df['year_label'] = day_df['yr'].map({0: '2011', 1: '2012'})
    hour_df['year_label'] = hour_df['yr'].map({0: '2011', 1: '2012'})

    day_df['temp_c'] = day_df['temp'] * 41
    hour_df['temp_c'] = hour_df['temp'] * 41
    day_df['hum_pct'] = day_df['hum'] * 100
    hour_df['hum_pct'] = hour_df['hum'] * 100

    # Time cluster
    def get_time_cluster(hr):
        if hr in [0, 1, 2, 3, 4, 5]:
            return 'Dini Hari (0-5)'
        elif hr in [6, 7, 8, 9]:
            return 'Pagi/Morning Rush (6-9)'
        elif hr in [10, 11, 12, 13, 14, 15]:
            return 'Siang (10-15)'
        elif hr in [16, 17, 18, 19]:
            return 'Sore/Evening Rush (16-19)'
        else:
            return 'Malam (20-23)'

    hour_df['time_cluster'] = hour_df['hr'].apply(get_time_cluster)
    hour_df['day_type'] = hour_df['workingday'].map({1: 'Hari Kerja', 0: 'Hari Libur'})

    return day_df, hour_df

day_df, hour_df = load_data()

# ============================================
# SIDEBAR
# ============================================
st.sidebar.title("🚲 Bike Sharing Dashboard")
st.sidebar.markdown("---")
st.sidebar.markdown("**Analisis Data Capital Bikeshare**")
st.sidebar.markdown("Washington D.C., USA | 2011-2012")

# Filter Tahun
st.sidebar.subheader("🔍 Filter Data")
tahun = st.sidebar.multiselect(
    "Tahun",
    options=['2011', '2012'],
    default=['2011', '2012']
)

# Filter Musim
musim = st.sidebar.multiselect(
    "Musim",
    options=['Spring', 'Summer', 'Fall', 'Winter'],
    default=['Spring', 'Summer', 'Fall', 'Winter']
)

# Filter Tipe Hari
day_type_filter = st.sidebar.multiselect(
    "Tipe Hari",
    options=['Hari Kerja', 'Hari Libur'],
    default=['Hari Kerja', 'Hari Libur']
)

# Filter jam (untuk data per jam)
jam_range = st.sidebar.slider(
    "Rentang Jam",
    min_value=0, max_value=23, value=(0, 23)
)

# Apply filters
def apply_filters(df, is_hourly=False):
    mask = pd.Series(True, index=df.index)

    if tahun:
        mask &= df['year_label'].isin(tahun)
    if musim:
        mask &= df['season_label'].isin(musim)
    if is_hourly:
        if day_type_filter:
            mask &= df['day_type'].isin(day_type_filter)
        mask &= df['hr'].between(jam_range[0], jam_range[1])

    return df[mask].copy()

day_filtered = apply_filters(day_df)
hour_filtered = apply_filters(hour_df, is_hourly=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset Info**")
st.sidebar.markdown(f"- Data Harian: {len(day_filtered)} baris")
st.sidebar.markdown(f"- Data Jam: {len(hour_filtered)} baris")

# ============================================
# MAIN PAGE
# ============================================
st.title("🚲 Bike Sharing Dashboard")
st.markdown(
    "Dashboard interaktif untuk menganalisis pola penyewaan sepeda "
    "Capital Bikeshare, Washington D.C. berdasarkan data tahun 2011-2012."
)

# ============================================
# ROW 1: METRIC CARDS
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Penyewaan",
        value=f"{hour_filtered['cnt'].sum():,}",
        delta=f"{hour_filtered['cnt'].mean():.0f} /jam (rata-rata)"
    )

with col2:
    st.metric(
        label="Pengguna Registered",
        value=f"{hour_filtered['registered'].sum():,}",
        delta=f"{hour_filtered['registered'].mean():.0f} /jam"
    )

with col3:
    st.metric(
        label="Pengguna Casual",
        value=f"{hour_filtered['casual'].sum():,}",
        delta=f"{hour_filtered['casual'].mean():.0f} /jam"
    )

with col4:
    total_days = day_filtered['dteday'].nunique()
    st.metric(
        label="Hari Data",
        value=f"{total_days} hari",
        delta=f"{len(day_filtered)} records"
    )

st.markdown("---")

# ============================================
# TAB 1: POLA PENYEWAAN
# ============================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Pola Penyewaan",
    "🌤️ Analisis Cuaca",
    "👥 Pengguna",
    "🔬 Analisis Lanjutan"
])

with tab1:
    st.header("Pola Penyewaan Sepeda")

    col1, col2 = st.columns(2)

    with col1:
        # Line chart: pola per jam
        hourly_avg = hour_filtered.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()

        fig = go.Figure()
        colors = {'Hari Kerja': '#E74C3C', 'Hari Libur': '#2ECC71'}

        for dtype in hourly_avg['day_type'].unique():
            data = hourly_avg[hourly_avg['day_type'] == dtype]
            fig.add_trace(go.Scatter(
                x=data['hr'], y=data['cnt'],
                mode='lines+markers', name=dtype,
                line=dict(width=3, color=colors.get(dtype, '#3498DB')),
                marker=dict(size=8)
            ))

        fig.update_layout(
            title='Rata-rata Penyewaan per Jam',
            xaxis_title='Jam', yaxis_title='Rata-rata Penyewaan',
            xaxis=dict(tickmode='linear', tick0=0, dtick=2),
            template='plotly_white', height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bar chart per season
        season_avg = hour_filtered.groupby('season_label')['cnt'].mean().reset_index()
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        season_avg['order'] = season_avg['season_label'].apply(
            lambda x: season_order.index(x) if x in season_order else 99
        )
        season_avg = season_avg.sort_values('order')

        fig = px.bar(
            season_avg, x='season_label', y='cnt',
            title='Rata-rata Penyewaan per Musim',
            color='season_label',
            color_discrete_map={
                'Spring': '#2ECC71', 'Summer': '#F39C12',
                'Fall': '#E74C3C', 'Winter': '#3498DB'
            },
            text_auto='.0f'
        )
        fig.update_layout(
            xaxis_title='Musim', yaxis_title='Rata-rata Penyewaan',
            template='plotly_white', height=400, showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    st.subheader("Heatmap Rata-rata Penyewaan: Jam vs Hari")
    heatmap_data = hour_filtered.pivot_table(
        values='cnt', index='hr', columns='weekday_name', aggfunc='mean'
    )
    weekday_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    # Only keep available weekday columns
    weekday_order = [d for d in weekday_order if d in heatmap_data.columns]
    heatmap_data = heatmap_data[weekday_order]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlOrRd',
        text=heatmap_data.values.round(0),
        texttemplate='%{text}',
        textfont={'size': 8},
        colorbar=dict(title='Rata-rata cnt')
    ))
    fig.update_layout(
        xaxis_title='Hari', yaxis_title='Jam',
        template='plotly_white', height=450
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 2: ANALISIS CUACA
# ============================================
with tab2:
    st.header("Analisis Pengaruh Cuaca")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            day_filtered, x='temp_c', y='cnt',
            color='season_label', opacity=0.6,
            title='Suhu vs Jumlah Penyewaan Harian',
            labels={'temp_c': 'Suhu (°C)', 'cnt': 'Jumlah Penyewaan', 'season_label': 'Musim'},
            hover_data={'dteday': True}
        )
        fig.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            day_filtered, x='hum_pct', y='cnt',
            color='season_label', opacity=0.6,
            title='Kelembaban vs Jumlah Penyewaan Harian',
            labels={'hum_pct': 'Kelembaban (%)', 'cnt': 'Jumlah Penyewaan', 'season_label': 'Musim'},
            hover_data={'dteday': True}
        )
        fig.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Weathersit breakdown
    col1, col2 = st.columns(2)

    with col1:
        weather_avg = hour_filtered.groupby('weather_label')['cnt'].mean().reset_index()
        fig = px.bar(
            weather_avg, x='weather_label', y='cnt',
            title='Rata-rata Penyewaan per Kondisi Cuaca',
            color='weather_label',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text_auto='.0f'
        )
        fig.update_layout(
            xaxis_title='Kondisi Cuaca', yaxis_title='Rata-rata Penyewaan',
            template='plotly_white', height=400, showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Korelasi
        corr_temp = day_filtered['temp_c'].corr(day_filtered['cnt'])
        corr_hum = day_filtered['hum_pct'].corr(day_filtered['cnt'])

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Suhu (°C)', 'Kelembaban (%)'],
            y=[corr_temp, corr_hum],
            marker_color=['#E74C3C', '#3498DB'],
            text=[f'{corr_temp:.3f}', f'{corr_hum:.3f}'],
            textposition='outside'
        ))
        fig.update_layout(
            title='Korelasi Faktor Cuaca dengan Penyewaan',
            xaxis_title='Faktor', yaxis_title='Koefisien Korelasi',
            template='plotly_white', height=400
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig, use_container_width=True)

    # Temperature binning analysis
    st.subheader("Analisis Binning Suhu")
    day_filtered['temp_bin'] = pd.cut(
        day_filtered['temp_c'],
        bins=[0, 10, 20, 30, 50],
        labels=['Dingin (<10°C)', 'Sejuk (10-20°C)', 'Hangat (20-30°C)', 'Panas (>30°C)']
    )

    temp_bin_stats = day_filtered.groupby('temp_bin', observed=True)['cnt'].describe()

    fig = go.Figure()
    for idx, cat in enumerate(['Dingin (<10°C)', 'Sejuk (10-20°C)', 'Hangat (20-30°C)', 'Panas (>30°C)']):
        data = day_filtered[day_filtered['temp_bin'] == cat]['cnt']
        if len(data) > 0:
            fig.add_trace(go.Box(y=data, name=cat))

    fig.update_layout(
        title='Distribusi Penyewaan per Kategori Suhu',
        yaxis_title='Jumlah Penyewaan Harian',
        template='plotly_white', height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 3: ANALISIS PENGGUNA
# ============================================
with tab3:
    st.header("Analisis Pengguna: Casual vs Registered")

    col1, col2 = st.columns(2)

    with col1:
        hourly_user = hour_filtered.groupby('hr')[['casual', 'registered']].mean().reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hourly_user['hr'], y=hourly_user['registered'],
            mode='lines+markers', name='Registered',
            line=dict(width=3, color='#3498DB'), marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=hourly_user['hr'], y=hourly_user['casual'],
            mode='lines+markers', name='Casual',
            line=dict(width=3, color='#E67E22'), marker=dict(size=8)
        ))
        fig.update_layout(
            title='Rata-rata Pengguna per Jam',
            xaxis_title='Jam', yaxis_title='Rata-rata',
            xaxis=dict(tickmode='linear', tick0=0, dtick=2),
            template='plotly_white', height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Pie chart - proporsi total
        total_casual = hour_filtered['casual'].sum()
        total_registered = hour_filtered['registered'].sum()

        fig = go.Figure(data=[go.Pie(
            labels=['Casual', 'Registered'],
            values=[total_casual, total_registered],
            marker_colors=['#E67E22', '#3498DB'],
            textinfo='label+percent',
            pull=[0.05, 0]
        )])
        fig.update_layout(
            title='Proporsi Total Pengguna',
            template='plotly_white', height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    # Perbandingan per musim
    season_user = hour_filtered.groupby('season_label')[['casual', 'registered']].mean().reset_index()
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_user['order'] = season_user['season_label'].apply(
        lambda x: season_order.index(x) if x in season_order else 99
    )
    season_user = season_user.sort_values('order')

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=season_user['season_label'], y=season_user['registered'],
        name='Registered', marker_color='#3498DB'
    ))
    fig.add_trace(go.Bar(
        x=season_user['season_label'], y=season_user['casual'],
        name='Casual', marker_color='#E67E22'
    ))
    fig.update_layout(
        title='Rata-rata Pengguna per Musim',
        xaxis_title='Musim', yaxis_title='Rata-rata',
        barmode='group', template='plotly_white', height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 4: ANALISIS LANJUTAN
# ============================================
with tab4:
    st.header("Analisis Lanjutan: Clustering & Binning")

    st.markdown("""
    **Teknik analisis lanjutan tanpa machine learning:**
    - **Time-based Clustering**: Mengelompokkan jam ke dalam segmen waktu
    - **Binning**: Mengkategorikan variabel kontinu
    - **Usage Level Segmentation**: Segmentasi tingkat penggunaan
    """)

    col1, col2 = st.columns(2)

    with col1:
        # Time cluster analysis
        cluster_avg = hour_filtered.groupby('time_cluster', observed=True)['cnt'].mean().reset_index()
        cluster_avg = cluster_avg.sort_values('cnt', ascending=True)

        colors = {
            'Dini Hari (0-5)': '#6A994E',
            'Pagi/Morning Rush (6-9)': '#2E86AB',
            'Siang (10-15)': '#A23B72',
            'Sore/Evening Rush (16-19)': '#F18F01',
            'Malam (20-23)': '#C73E1D'
        }

        fig = go.Figure(go.Bar(
            x=cluster_avg['cnt'],
            y=cluster_avg['time_cluster'],
            orientation='h',
            marker_color=[colors.get(c, '#999') for c in cluster_avg['time_cluster']],
            text=cluster_avg['cnt'].round(0),
            textposition='outside'
        ))
        fig.update_layout(
            title='Rata-rata Penyewaan per Cluster Waktu',
            xaxis_title='Rata-rata Penyewaan',
            yaxis_title='',
            template='plotly_white', height=350
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Usage level distribution
        quartiles = hour_filtered['cnt'].quantile([0.25, 0.5, 0.75]).values

        def get_usage_level(cnt):
            if cnt <= quartiles[0]:
                return 'Rendah'
            elif cnt <= quartiles[2]:
                return 'Sedang'
            else:
                return 'Tinggi'

        hour_filtered['usage_level'] = hour_filtered['cnt'].apply(get_usage_level)
        usage_counts = hour_filtered['usage_level'].value_counts()

        fig = go.Figure(data=[go.Pie(
            labels=usage_counts.index,
            values=usage_counts.values,
            marker_colors=['#E74C3C', '#F39C12', '#2ECC71'],
            textinfo='label+percent'
        )])
        fig.update_layout(
            title='Segmentasi Tingkat Penggunaan',
            template='plotly_white', height=350
        )
        st.plotly_chart(fig, use_container_width=True)

    # Cross-tab: time cluster vs usage level
    st.subheader("Tabulasi Silang: Cluster Waktu vs Level Penggunaan")
    cross_tab = pd.crosstab(
        hour_filtered['time_cluster'],
        hour_filtered['usage_level'],
        normalize='index'
    ) * 100
    cross_tab = cross_tab.round(1)
    cross_tab = cross_tab[['Rendah', 'Sedang', 'Tinggi']]  # Ensure order
    st.dataframe(cross_tab, use_container_width=True)

    # Temperature binning detail
    st.subheader("Analisis Binning Detail")
    col1, col2 = st.columns(2)

    with col1:
        temp_bins = pd.cut(
            hour_filtered['temp_c'],
            bins=[0, 5, 10, 15, 20, 25, 30, 35, 45],
            labels=['<5°C', '5-10°C', '10-15°C', '15-20°C', '20-25°C', '25-30°C', '30-35°C', '>35°C']
        )
        temp_stats = hour_filtered.groupby(temp_bins, observed=True)['cnt'].mean().reset_index()
        temp_stats.columns = ['Rentang Suhu', 'Rata-rata Penyewaan']

        fig = px.line(
            temp_stats, x='Rentang Suhu', y='Rata-rata Penyewaan',
            markers=True, title='Tren Penyewaan per Rentang Suhu'
        )
        fig.update_layout(template='plotly_white', height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        hum_bins = pd.cut(
            hour_filtered['hum_pct'],
            bins=[0, 25, 50, 75, 101],
            labels=['Sangat Rendah', 'Rendah (25-50%)', 'Sedang (50-75%)', 'Tinggi (>75%)']
        )
        hum_stats = hour_filtered.groupby(hum_bins, observed=True)['cnt'].mean().reset_index()
        hum_stats.columns = ['Rentang Kelembaban', 'Rata-rata Penyewaan']

        fig = px.bar(
            hum_stats, x='Rentang Kelembaban', y='Rata-rata Penyewaan',
            title='Penyewaan per Rentang Kelembaban',
            color='Rentang Kelembaban',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text_auto='.0f'
        )
        fig.update_layout(template='plotly_white', height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🚲 <b>Bike Sharing Dashboard</b> | "
    "Dataset: Capital Bikeshare Washington D.C. (2011-2012) | "
    "Dibuat dengan Streamlit"
    "</div>",
    unsafe_allow_html=True
)
