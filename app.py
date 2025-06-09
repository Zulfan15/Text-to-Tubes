from flask import Flask, render_template, request, send_file, jsonify
import pyttsx3
import os
import tempfile
import threading
from datetime import datetime
from gtts import gTTS
import io
from io import BytesIO
try:
    from google.cloud import texttospeech
    CLOUD_TTS_AVAILABLE = True
except ImportError:
    CLOUD_TTS_AVAILABLE = False
    print("Google Cloud TTS not available. Using gTTS only.")

app = Flask(__name__)

# Konfigurasi folder untuk menyimpan file audio
UPLOAD_FOLDER = 'audio_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def create_audio_file_cloud_tts(text, speed, format_type, gender='male'):
    """
    Membuat file audio menggunakan Google Cloud Text-to-Speech dengan voice selection yang tepat
    """
    try:
        if not CLOUD_TTS_AVAILABLE:
            return None, None
        
        # Inisialisasi client Google Cloud TTS
        client = texttospeech.TextToSpeechClient()
        
        # Set input text
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Pilih voice berdasarkan gender
        if gender == 'male':
            voice_name = "id-ID-Standard-B"  # Male voice
        else:
            voice_name = "id-ID-Standard-A"  # Female voice
        
        # Konfigurasi voice
        voice = texttospeech.VoiceSelectionParams(
            language_code="id-ID",
            name=voice_name
        )
        
        # Tentukan speaking rate berdasarkan speed
        if speed == 'slow':
            speaking_rate = 0.75
        elif speed == 'fast':
            speaking_rate = 1.25
        else:
            speaking_rate = 1.0
        
        # Konfigurasi audio
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate
        )
        
        # Generate speech
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Simpan file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cloudtts_{gender}_{timestamp}.mp3"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as out:
            out.write(response.audio_content)
        
        print(f"Audio content written to file '{filename}' using Cloud TTS {voice_name}")
        return filename, filepath
        
    except Exception as e:
        print(f"Error creating Cloud TTS audio file: {str(e)}")
        return None, None

def create_audio_file_gtts(text, speed, format_type, gender='male'):
    """
    Membuat file audio dari teks menggunakan gTTS dengan enhanced voice processing
    """
    try:
        # Coba Google Cloud TTS terlebih dahulu untuk gender selection yang lebih baik
        if CLOUD_TTS_AVAILABLE:
            cloud_result = create_audio_file_cloud_tts(text, speed, format_type, gender)
            if cloud_result[0] and cloud_result[1]:
                return cloud_result
        
        # Fallback ke gTTS
        print("Using gTTS fallback...")
        slow_speed = speed == 'slow'
        
        # Membuat nama file dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gtts_{gender}_{timestamp}.mp3"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Untuk male voice, coba beberapa pendekatan berbeda
        if gender == 'male':
            # Pendekatan 1: Gunakan domain Australia (biasanya pitch lebih rendah)
            try:
                tts = gTTS(text=text, lang='id', slow=slow_speed, tld='com.au')
                tts.save(filepath)
                return filename, filepath
            except:
                pass
            
            # Pendekatan 2: Gunakan domain UK
            try:
                tts = gTTS(text=text, lang='id', slow=slow_speed, tld='co.uk')
                tts.save(filepath)
                return filename, filepath
            except:
                pass
        
        # Default gTTS
        tts = gTTS(text=text, lang='id', slow=slow_speed)
        tts.save(filepath)
        return filename, filepath
    
    except Exception as e:
        print(f"Error creating gTTS audio file: {str(e)}")
        return None, None

def create_audio_file_pyttsx3(text, speed, format_type, gender='male'):
    """
    Membuat file audio dari teks menggunakan pyttsx3 (Windows TTS) dengan prioritas suara Indonesia
    """
    try:
        # Inisialisasi engine TTS
        engine = pyttsx3.init()
        
        # Mengatur gender suara dengan prioritas Indonesia
        voices = engine.getProperty('voices')
        selected_voice = None
        
        # Prioritas 1: Cari suara Indonesia dengan gender yang sesuai
        for voice in voices:
            voice_info = voice.name.lower()
            voice_id = voice.id.lower()
            
            # Cek apakah suara bahasa Indonesia
            is_indonesian = any(keyword in voice_info or keyword in voice_id for keyword in 
                              ['indonesia', 'indonesian', 'id-id', 'bahasa'])
            
            if is_indonesian:
                # Cek gender untuk suara Indonesia
                is_male = any(keyword in voice_info for keyword in ['male', 'pria', 'laki'])
                is_female = any(keyword in voice_info for keyword in ['female', 'wanita', 'perempuan'])
                
                if (gender == 'male' and is_male) or (gender == 'female' and is_female):
                    selected_voice = voice.id
                    print(f"Found Indonesian voice: {voice.name}")
                    break
        
        # Prioritas 2: Jika tidak ada suara Indonesia, cari berdasarkan gender saja
        if not selected_voice:
            for voice in voices:
                voice_info = voice.name.lower()
                
                # Cek gender suara (termasuk nama khusus seperti David/Zira)
                is_male = any(keyword in voice_info for keyword in ['male', 'david', 'mark', 'james'])
                is_female = any(keyword in voice_info for keyword in ['female', 'zira', 'susan', 'mary'])
                
                if gender == 'female' and is_female:
                    selected_voice = voice.id
                    print(f"Found female voice: {voice.name}")
                    break
                elif gender == 'male' and is_male:
                    selected_voice = voice.id
                    print(f"Found male voice: {voice.name}")
                    break
        
        # Prioritas 3: Gunakan suara default berdasarkan posisi
        if not selected_voice and voices:
            if gender == 'male':
                selected_voice = voices[0].id  # Biasanya David (male)
                print(f"Using default male voice: {voices[0].name}")
            else:
                selected_voice = voices[-1].id if len(voices) > 1 else voices[0].id  # Biasanya Zira (female)
                print(f"Using default female voice: {voices[-1].name if len(voices) > 1 else voices[0].name}")
        
        # Set voice property jika berhasil menemukan suara
        if selected_voice:
            engine.setProperty('voice', selected_voice)
        
        # Mengatur kecepatan berbicara
        rate = engine.getProperty('rate')
        base_rate = 200  # Rate dasar yang lebih natural
        
        if speed == 'slow':
            engine.setProperty('rate', max(base_rate - 75, 100))
        elif speed == 'fast':
            engine.setProperty('rate', min(base_rate + 75, 400))
        else:  # normal
            engine.setProperty('rate', base_rate)
        
        # Mengatur volume untuk clarity
        volume = engine.getProperty('volume')
        engine.setProperty('volume', 0.9)  # 90% volume untuk clarity
        
        # Membuat nama file dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pyttsx3_{gender}_{timestamp}.{format_type}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Menyimpan audio ke file
        engine.save_to_file(text, filepath)
        engine.runAndWait()
        
        return filename, filepath
    
    except Exception as e:
        print(f"Error creating pyttsx3 audio file: {str(e)}")
        return None, None

def create_audio_file(text, speed, format_type, gender='male', engine_type='auto'):
    """
    Membuat file audio dari teks - Smart engine selection untuk hasil terbaik
    """
    try:
        # Mode AUTO: Pilih engine terbaik berdasarkan gender dan ketersediaan
        if engine_type == 'auto':
            # Untuk gender male, coba Windows TTS terlebih dahulu (karena gTTS Indonesia cenderung female)
            if gender == 'male':
                print("AUTO MODE: Trying Windows TTS for male voice...")
                filename_pyttsx3, filepath_pyttsx3 = create_audio_file_pyttsx3(text, speed, format_type, gender)
                if filename_pyttsx3 and filepath_pyttsx3:
                    return filename_pyttsx3, filepath_pyttsx3
                
                print("Windows TTS failed, falling back to gTTS...")
                filename_gtts, filepath_gtts = create_audio_file_gtts(text, speed, format_type, gender)
                if filename_gtts and filepath_gtts:
                    return filename_gtts, filepath_gtts
            else:
                # Untuk gender female, coba gTTS terlebih dahulu
                print("AUTO MODE: Trying gTTS for female voice...")
                filename_gtts, filepath_gtts = create_audio_file_gtts(text, speed, format_type, gender)
                if filename_gtts and filepath_gtts:
                    return filename_gtts, filepath_gtts
                
                print("gTTS failed, falling back to Windows TTS...")
                filename_pyttsx3, filepath_pyttsx3 = create_audio_file_pyttsx3(text, speed, format_type, gender)
                if filename_pyttsx3 and filepath_pyttsx3:
                    return filename_pyttsx3, filepath_pyttsx3
        
        # Mode GTTS: Gunakan Google TTS
        elif engine_type == 'gtts':
            filename_gtts, filepath_gtts = create_audio_file_gtts(text, speed, format_type, gender)
            if filename_gtts and filepath_gtts:
                return filename_gtts, filepath_gtts
        
        # Mode PYTTSX3: Gunakan Windows TTS
        elif engine_type == 'pyttsx3':
            filename_pyttsx3, filepath_pyttsx3 = create_audio_file_pyttsx3(text, speed, format_type, gender)
            if filename_pyttsx3 and filepath_pyttsx3:
                return filename_pyttsx3, filepath_pyttsx3
        
        # Jika semua gagal, coba fallback terakhir
        print("All engines failed, trying final fallback...")
        return create_audio_file_gtts(text, speed, format_type, gender)
    
    except Exception as e:
        print(f"Error in audio creation: {str(e)}")
        return None, None

@app.route('/')
def index():
    """
    Halaman utama website
    """
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    """
    Endpoint untuk konversi teks ke suara dengan smart engine selection
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        speed = data.get('speed', 'normal')
        format_type = data.get('format', 'mp3')
        gender = data.get('gender', 'male')
        engine_type = data.get('engine', 'auto')  # Default ke AUTO untuk hasil terbaik
        
        if not text:
            return jsonify({'error': 'Teks tidak boleh kosong'}), 400
        
        # Validasi panjang teks
        if len(text) > 500:
            return jsonify({'error': 'Teks terlalu panjang (maksimal 500 karakter)'}), 400
        
        print(f"Converting text: '{text[:50]}...' with engine: {engine_type}, gender: {gender}")
        
        # Membuat file audio dengan parameter yang dipilih
        filename, filepath = create_audio_file(text, speed, format_type, gender, engine_type)
        
        if filename and filepath:
            # Deteksi engine yang benar-benar digunakan dari nama file
            actual_engine = 'gTTS' if filename.startswith('gtts_') else 'Windows TTS'
            
            return jsonify({
                'success': True,
                'filename': filename,
                'message': f'Audio berhasil dibuat dengan {actual_engine}',
                'engine': actual_engine,
                'gender': gender,
                'voice_info': f'{actual_engine} - {gender.title()} Voice'
            })
        else:
            return jsonify({'error': 'Gagal membuat file audio dengan semua engine yang tersedia'}), 500
    
    except Exception as e:
        print(f"Error in convert endpoint: {str(e)}")
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_audio(filename):
    """
    Endpoint untuk mengunduh file audio
    """
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'error': f'Gagal mengunduh file: {str(e)}'}), 500

@app.route('/play/<filename>')
def play_audio(filename):
    """
    Endpoint untuk memutar file audio
    """
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            return jsonify({'error': 'File tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'error': f'Gagal memutar file: {str(e)}'}), 500

@app.route('/engines')
def list_engines():
    """
    Endpoint untuk mendapatkan daftar engine TTS yang tersedia
    """
    try:
        engines = {
            'gtts': {
                'name': 'Google Text-to-Speech Enhanced',
                'language': 'Bahasa Indonesia',
                'voices': ['Cloud TTS Male (id-ID-Standard-B)', 'Cloud TTS Female (id-ID-Standard-A)', 'gTTS Default'] if CLOUD_TTS_AVAILABLE else ['gTTS Default'],
                'formats': ['mp3'],
                'features': ['Cloud TTS for proper gender selection', 'gTTS fallback'] if CLOUD_TTS_AVAILABLE else ['Basic TTS']
            },
            'pyttsx3': {
                'name': 'Windows Speech API',
                'language': 'Multi-language',
                'voices': [],
                'formats': ['mp3', 'wav'],
                'features': ['Indonesian voice detection', 'Gender-based selection']            }
        }
        
        # Cek suara pyttsx3 yang tersedia
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            for voice in voices:
                engines['pyttsx3']['voices'].append(voice.name)
        except:
            engines['pyttsx3']['voices'] = ['Microsoft David', 'Microsoft Zira']
        
        return jsonify(engines)
    
    except Exception as e:
        return jsonify({'error': f'Gagal mendapatkan daftar engine: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
