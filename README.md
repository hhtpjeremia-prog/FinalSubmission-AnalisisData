# Proyek Analisis Data Bike Sharing - Capital Bikeshare

**Tugas Akhir Analisis Data** | Bootcamp Tempa

Proyek ini menganalisis dataset Bike Sharing dari Capital Bikeshare, Washington D.C. (2011-2012) menggunakan metode analisis data eksploratif, visualisasi interaktif, dan teknik analisis lanjutan seperti clustering manual (time-based clustering) dan binning analysis.

---

## Struktur Proyek

```
submission/
├── Proyek_Analisis_Data.ipynb   # Notebook analisis data (template)
├── dashboard.py                  # Dashboard Streamlit interaktif
├── requirements.txt              # Dependencies Python
├── README.md                     # Dokumentasi proyek
└── data/
    ├── day.csv                   # Data harian (731 records)
    └── hour.csv                  # Data per jam (17.379 records)
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
streamlit run dashboard.py
```

---

## Cara Deploy ke Streamlit Cloud

### Langkah-langkah:

#### 1. Push ke GitHub
```bash
git init
git add .
git commit -m "Final submission bike sharing analysis"

# Buat repository di GitHub, lalu push
git remote add origin https://github.com/username/nama-repo.git
git branch -M main
git push -u origin main
```

#### 2. Buka Streamlit Cloud
- Buka https://streamlit.io/cloud
- Login dengan akun GitHub
- Klik "New app"

#### 3. Konfigurasi App
| Field | Value |
|-------|-------|
| Repository | Pilih repo GitHub yang telah di-push |
| Branch | main |
| Main file path | submission/dashboard.py |

#### 4. Advanced Settings
- Python version: 3.11 atau 3.12
- Requirements file: submission/requirements.txt

#### 5. Klik "Deploy"

Proses deploy memakan waktu 2-5 menit. Setelah selesai, Anda akan mendapatkan URL publik seperti:
```
https://username-nama-repo-submission-dashboard.streamlit.app
```

### Catatan Penting
- Pastikan path file di dashboard.py menggunakan path relatif (data/day.csv)
- File data sudah termasuk dalam repository (ukuran kecil)
- Streamlit Cloud akan menginstall dependencies dari requirements.txt secara otomatis

---

## Dataset

**Sumber**: Capital Bikeshare System Data (http://capitalbikeshare.com/system-data)

| File | Records | Kolom |
|------|---------|-------|
| day.csv | 731 | 16 |
| hour.csv | 17.379 | 17 |

**Referensi**: Fanaee-T, Hadi, and Gama, Joao, "Event labeling combining ensemble detectors and background knowledge", Progress in Artificial Intelligence (2013)
