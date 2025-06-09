# Text-to-Speech Web Application

Aplikasi web Text-to-Speech dengan User Experience yang telah ditingkatkan, mendukung konversi teks menjadi suara dengan berbagai fitur advanced.

## ✨ Fitur Utama yang Ditingkatkan

### 🎯 Core TTS Features
- **Mode AUTO**: Pemilihan engine otomatis berdasarkan gender untuk hasil terbaik
- **Google TTS Enhanced**: Menggunakan Google Cloud TTS untuk gender selection yang tepat
- **Windows TTS**: Support suara lokal dengan deteksi gender
- **👨👩 Gender Selection**: Pilihan suara laki-laki dan perempuan yang akurat
- **⚡ Multi-Speed**: Kontrol kecepatan berbicara (lambat, normal, cepat)
- **🎵 Multi-Format**: Support MP3 dan WAV

### 🚀 Enhanced User Experience Features

#### 1. **📊 Detailed Progress Indicators**
- Progress bar dengan 6 tahap konversi yang jelas
- Status pesan real-time untuk setiap tahap proses
- Animasi progress yang smooth dan informatif

#### 2. **👁️ Preview Functionality**
- Preview cepat dengan 50 karakter pertama
- Generasi audio sementara untuk testing
- Konfirmasi user untuk text truncation
- Instant playback tanpa download

#### 3. **📜 Conversion History & Records**
- Penyimpanan otomatis 20 konversi terakhir di localStorage
- Interface history yang collapsible dan elegant
- Fitur play, download, dan replay untuk setiap item history
- Clear history dengan konfirmasi safety
- Informasi lengkap: text preview, timestamp, engine, gender

#### 4. **📈 Smart Input Assistance**
- **Character Counter**: Real-time counter dengan warning indicators
- **Duration Estimation**: Estimasi durasi audio berdasarkan teks dan speed
- **File Size Estimation**: Perkiraan ukuran file output
- **Auto-limitation**: Pembatasan otomatis input untuk optimal performance

#### 5. **🎨 Enhanced Visual Design**
- **Modern UI**: Gradient backgrounds dan smooth animations
- **Responsive Design**: Mobile-friendly dengan adaptive layouts
- **Interactive Elements**: Hover effects dan transitions
- **Color-coded Feedback**: Visual indicators untuk status dan warnings
- **Improved Typography**: Clear hierarki dan readable fonts

#### 6. **⚡ Performance & Usability**
- **Form Auto-fill**: Replay konversi dengan data history
- **Smart Engine Selection**: Auto-optimization berdasarkan gender
- **Error Handling**: Comprehensive error messages dan recovery
- **Loading States**: Clear loading indicators untuk semua operations
- **Auto-hide Alerts**: Temporary messages dengan auto-dismiss

## 🚀 Cara Instalasi

### Metode 1: Setup Otomatis (Recommended)
```bash
python setup_cloud_tts.py
```

### Metode 2: Manual Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Google Cloud TTS (Opsional, untuk gender selection terbaik):**
   - Install Google Cloud SDK
   - Jalankan: `gcloud auth application-default login`
   - Enable Text-to-Speech API di Google Cloud Console

3. **Jalankan aplikasi:**
   ```bash
   python app.py
   ```

4. **Buka browser dan akses:**
   ```
   http://localhost:5000
   ```

## 🔧 Konfigurasi Engine

### Google TTS Enhanced
- **Dengan Cloud TTS**: Mendukung voice selection yang tepat untuk gender
  - Male: `id-ID-Standard-B`
  - Female: `id-ID-Standard-A`
- **Fallback gTTS**: Menggunakan variasi domain untuk optimasi
  - Male: `com.au`, `co.uk` domains
  - Female: default domain

### Windows TTS
- Deteksi otomatis suara Indonesia
- Prioritas gender selection:
  1. Suara Indonesia dengan gender match
  2. Suara Windows dengan gender match
  3. Suara default berdasarkan gender

### Mode AUTO
- **Male**: Prioritas Windows TTS → Google TTS
- **Female**: Prioritas Google TTS → Windows TTS

## 📋 Dependencies

- Flask 2.3.3
- pyttsx3 2.90
- gTTS 2.4.0
- google-cloud-texttospeech 2.16.3 (opsional)
- pygame 2.5.2

## 🗂️ Struktur Proyek

```
├── app.py                    # Main Flask application
├── setup_cloud_tts.py      # Setup script untuk Cloud TTS
├── requirements.txt         # Dependencies
├── templates/
│   └── index.html          # Frontend interface
├── static/
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
└── audio_files/           # Generated audio files
```

## 🎛️ Penggunaan

1. **Masukkan teks** (maksimal 500 karakter)
2. **Pilih kecepatan** berbicara
3. **Pilih format** audio (MP3/WAV)
4. **Pilih engine** TTS:
   - AUTO: Pilihan otomatis terbaik
   - Google TTS Enhanced: Menggunakan Cloud TTS
   - Windows TTS: Menggunakan sistem Windows
5. **Pilih gender** suara
6. **Klik konversi** dan nikmati hasilnya!

## 🔧 Technical Specifications

### Frontend Technologies
- **HTML5**: Semantic structure dengan accessibility features
- **Bootstrap 5**: Modern responsive framework
- **CSS3**: Custom animations, gradients, dan advanced styling
- **JavaScript ES6+**: Modern syntax dengan async/await
- **Font Awesome**: Icon library untuk visual consistency

### Backend Technologies
- **Flask**: Python web framework
- **Google Cloud TTS**: Premium voice synthesis
- **gTTS**: Fallback TTS engine
- **pyttsx3**: Windows native TTS
- **Audio Processing**: MP3/WAV generation dan streaming

### Data Management
- **localStorage**: Client-side history management
- **JSON**: Data serialization untuk API communication
- **File Streaming**: Efficient audio delivery

### Performance Features
- **Lazy Loading**: On-demand resource loading
- **Progress Simulation**: Real-time user feedback
- **Error Recovery**: Graceful fallback mechanisms
- **Memory Management**: Efficient audio file handling

## 🚀 Setup & Installation

### Prerequisites
- Python 3.7+
- pip package manager
- Modern web browser
- (Optional) Google Cloud account untuk premium TTS

### Metode 1: Quick Setup (Recommended)
```bash
# Clone dan setup otomatis
python setup_cloud_tts.py
python app.py
```

### Metode 2: Manual Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Google Cloud TTS (Optional):**
   ```bash
   # Install Google Cloud SDK
   gcloud auth application-default login
   # Enable Text-to-Speech API di Console
   ```

3. **Run application:**
   ```bash
   python app.py
   ```

4. **Access application:**
   ```
   http://localhost:5000
   ```

## 📋 Usage Guide

### Text-to-Speech Conversion
1. Masukkan teks (max 500 karakter)
2. Pilih speed, format, gender, dan engine
3. Gunakan Preview untuk test cepat (50 karakter)
4. Klik Konversi untuk full generation
5. Play audio atau download file

### History Management
1. View automatic history (20 items max)
2. Play audio langsung dari history
3. Download file lama
4. Replay konversi dengan settings yang sama
5. Clear history jika diperlukan

## 🔍 API Endpoints

### Core Endpoints
- `GET /` - Main application interface
- `POST /convert` - Single text conversion
- `GET /play/<filename>` - Stream audio file
- `GET /download/<filename>` - Download audio file
- `GET /engines` - Available TTS engines info

### Enhanced Endpoints
- Preview mode dalam `/convert` endpoint (parameter `preview=true`)

## ⚙️ Configuration Options

### Engine Settings
```python
# Auto mode - optimal engine selection
engine: "auto"

# Specific engines
engine: "gtts"    # Google TTS (recommended)
engine: "pyttsx3" # Windows TTS
```

### Speed Settings
```python
speed: "slow"     # ~120 WPM
speed: "normal"   # ~150 WPM (default)
speed: "fast"     # ~180 WPM
```

### Gender Optimization
```python
# Auto mode behavior:
gender: "male"   → prioritizes Windows TTS (David voice)
gender: "female" → prioritizes Google TTS (optimized)
```

## 🎯 UX Improvements Summary

### Before vs After
| Feature | Before | After |
|---------|--------|-------|
| Progress Feedback | ❌ None | ✅ 6-step detailed progress |
| Preview | ❌ None | ✅ 50-char instant preview |
| History | ❌ None | ✅ 20-item localStorage history |
| Input Validation | ❌ Basic | ✅ Real-time with estimations |
| Visual Design | ❌ Standard | ✅ Modern with animations |
| Mobile Support | ❌ Limited | ✅ Fully responsive |
| Error Handling | ❌ Basic | ✅ Comprehensive with recovery |

### User Journey Improvements
1. **Input**: Smart validation dengan real-time feedback
2. **Processing**: Detailed progress dengan status messages
3. **Results**: Rich playback dan download options
4. **History**: Persistent storage dengan easy replay

## 🔧 Troubleshooting

### Common Issues
1. **Audio tidak bisa diplay**: Check browser audio permissions
2. **Preview tidak muncul**: Check network connection
3. **History tidak tersimpan**: Verify localStorage permission

### Performance Tips
1. Gunakan Preview untuk testing sebelum full conversion
2. Clear history secara berkala untuk optimal performance
3. Gunakan Auto mode untuk optimal engine selection

---

**Aplikasi ini menyediakan pengalaman user yang kaya dengan feedback yang jelas, processing yang efisien, dan interface yang modern dan responsive.**
