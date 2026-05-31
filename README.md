# Proyek Analisis Data Bike Sharing - Capital Bikeshare

**Tugas Akhir Analisis Data** | Bootcamp Tempa

Proyek ini menganalisis dataset Bike Sharing dari Capital Bikeshare, Washington D.C. (2011-2012) menggunakan metode analisis data eksploratif, visualisasi interaktif, dan teknik analisis lanjutan seperti clustering manual (time-based clustering) dan binning analysis.

---

## Struktur Proyek

```
submission/
├───dashboard/
│   ├───dashboard.py              # Dashboard Streamlit interaktif
│   └───main_data.csv             # Data utama hasil cleansing
├───data/
│   ├───day.csv                   # Data harian (731 records)
│   └───hour.csv                  # Data per jam (17.379 records)
├───Proyek_Analisis_Data.ipynb    # Notebook analisis data
├───README.md                     # Dokumentasi proyek
├───requirements.txt              # Dependencies Python
└───url.txt                       # URL dashboard yang sudah dideploy
```

---

## Kriteria yang Dipenuhi

### Ketentuan Wajib
1. **Pertanyaan Bisnis SMART** - 2 pertanyaan bisnis dengan kerangka SMART
2. **Data Wrangling** - Gathering, Assessing (missing values, duplicates, outliers), Cleaning
3. **EDA** - Eksplorasi data untuk menjawab pertanyaan bisnis
4. **Visualization & Explanatory Analysis** - Visualisasi interaktif (Plotly) untuk setiap pertanyaan
5. **Conclusion & Recommendation** - 2 kesimpulan + 3 rekomendasi action item

### Saran untuk Rating Tinggi (Target: 5 Bintang)
1. Dokumentasi markdown/text cell di notebook (.ipynb)
2. Visualisasi data efektif dengan Plotly (prinsip desain dan integritas)
3. Dashboard Streamlit interaktif (siap deploy ke Streamlit Cloud)
4. Analisis Lanjutan:
   - Time-based Clustering - Pengelompokan jam ke segmen waktu (Dini Hari, Pagi, Siang, Sore, Malam)
   - Binning Analysis - Kategorisasi suhu, kelembaban, dan tingkat penggunaan
   - Segmentasi Pengguna - Analisis mendalam casual vs registered users

---

## Cara Menjalankan di Local

### 1. Buka Folder Proyek
```bash
cd submission
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan Notebook
```bash
jupyter notebook Proyek_Analisis_Data.ipynb
```

### 4. Jalankan Dashboard
```bash
streamlit run dashboard/dashboard.py
```

### 5. Akses Dashboard Online
Dashboard juga sudah dideploy ke Streamlit Cloud dan bisa diakses di:
```
https://submission-tempa.streamlit.app/
```

---

## Dataset

**Sumber**: Capital Bikeshare System Data (http://capitalbikeshare.com/system-data)

| File | Records | Kolom |
|------|---------|-------|
| day.csv | 731 | 16 |
| hour.csv | 17.379 | 17 |

**Referensi**: Fanaee-T, Hadi, and Gama, Joao, "Event labeling combining ensemble detectors and background knowledge", Progress in Artificial Intelligence (2013)
