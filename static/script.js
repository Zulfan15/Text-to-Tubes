document.addEventListener('DOMContentLoaded', function() {    // Form Elements
    const ttsForm = document.getElementById('ttsForm');
    const textInput = document.getElementById('textInput');
    const speedSelect = document.getElementById('speedSelect');
    const formatSelect = document.getElementById('formatSelect');
    const genderSelect = document.getElementById('genderSelect');
    const engineSelect = document.getElementById('engineSelect');
    const convertBtn = document.getElementById('convertBtn');
    const previewBtn = document.getElementById('previewBtn');    const btnText = document.getElementById('btnText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    
    // Progress Elements
    const progressArea = document.getElementById('progressArea');
    const progressBar = document.getElementById('progressBar');
    const progressPercent = document.getElementById('progressPercent');
    const progressTitle = document.getElementById('progressTitle');
    const progressStatus = document.getElementById('progressStatus');
    
    // Result Elements
    const resultArea = document.getElementById('resultArea');
    const errorArea = document.getElementById('errorArea');
    const errorMessage = document.getElementById('errorMessage');
    const audioPlayer = document.getElementById('audioPlayer');
    const downloadBtn = document.getElementById('downloadBtn');
    const voiceInfo = document.getElementById('voiceInfo');
    
    // History Elements
    const historySection = document.getElementById('historySection');
    const historyList = document.getElementById('historyList');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    
    // Help Elements
    const genderHelp = document.getElementById('genderHelp');
    const engineHelp = document.getElementById('engineHelp');

    // History Management
    let conversionHistory = JSON.parse(localStorage.getItem('ttsHistory')) || [];

    // Initialize
    loadHistory();
      // Progress Management
    function updateProgress(percent, status) {
        progressBar.style.width = percent + '%';
        progressPercent.textContent = percent + '%';
        progressStatus.textContent = status;
    }
    
    function showProgress(title = 'Memproses...') {
        progressTitle.textContent = title;
        progressArea.classList.remove('d-none');
        updateProgress(0, 'Menginisialisasi...');
    }
    
    function hideProgress() {
        progressArea.classList.add('d-none');
    }
    
    function simulateProgress(callback) {
        const steps = [
            { percent: 10, status: 'Menginisialisasi engine TTS...', delay: 300 },
            { percent: 25, status: 'Memproses teks input...', delay: 500 },
            { percent: 50, status: 'Menganalisis parameter suara...', delay: 400 },
            { percent: 75, status: 'Generating audio file...', delay: 800 },
            { percent: 90, status: 'Menyimpan file audio...', delay: 300 },
            { percent: 100, status: 'Selesai!', delay: 200 }
        ];
        
        let currentStep = 0;
        
        function nextStep() {
            if (currentStep < steps.length) {
                const step = steps[currentStep];
                updateProgress(step.percent, step.status);
                currentStep++;
                setTimeout(nextStep, step.delay);
            } else {
                setTimeout(callback, 300);
            }
        }
        
        nextStep();
    }

    // History Management Functions
    function addToHistory(data) {
        const historyItem = {
            id: Date.now(),
            text: data.text,
            filename: data.filename,
            engine: data.engine,
            gender: data.gender,
            speed: data.speed,
            format: data.format,
            timestamp: new Date().toLocaleString('id-ID')
        };
        
        conversionHistory.unshift(historyItem);
        
        // Keep only last 20 items
        if (conversionHistory.length > 20) {
            conversionHistory = conversionHistory.slice(0, 20);
        }
        
        localStorage.setItem('ttsHistory', JSON.stringify(conversionHistory));
        loadHistory();
    }
    
    function loadHistory() {
        if (conversionHistory.length === 0) {
            historySection.classList.add('d-none');
            return;
        }
        
        historySection.classList.remove('d-none');
        historyList.innerHTML = '';
        
        conversionHistory.forEach(item => {
            const historyItem = createHistoryItem(item);
            historyList.appendChild(historyItem);
        });
    }
    
    function createHistoryItem(item) {
        const div = document.createElement('div');
        div.className = 'border rounded p-3 mb-3';
        div.innerHTML = `
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <h6 class="mb-1">${item.text.substring(0, 50)}${item.text.length > 50 ? '...' : ''}</h6>
                    <small class="text-muted">
                        <i class="fas fa-clock me-1"></i>${item.timestamp} | 
                        <i class="fas fa-cog me-1"></i>${item.engine} | 
                        <i class="fas fa-user me-1"></i>${item.gender}
                    </small>
                </div>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="playHistoryAudio('${item.filename}')" title="Play">
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="btn btn-outline-success" onclick="downloadHistoryAudio('${item.filename}')" title="Download">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="btn btn-outline-info" onclick="replayConversion('${item.id}')" title="Replay">
                        <i class="fas fa-redo"></i>
                    </button>
                </div>
            </div>
        `;
        return div;
    }
    
    function clearHistory() {
        conversionHistory = [];
        localStorage.removeItem('ttsHistory');
        loadHistory();
    }

    // Global functions for history actions
    window.playHistoryAudio = function(filename) {
        audioPlayer.src = `/play/${filename}`;
        audioPlayer.play();
    };
    
    window.downloadHistoryAudio = function(filename) {
        window.open(`/download/${filename}`, '_blank');
    };

    window.replayConversion = function(itemId) {
        const item = conversionHistory.find(h => h.id == itemId);
        if (item) {
            // Fill form with history data
            textInput.value = item.text;
            speedSelect.value = item.speed;
            formatSelect.value = item.format;
            genderSelect.value = item.gender;
            engineSelect.value = item.engine;
              // Trigger engine change event to update UI
            engineSelect.dispatchEvent(new Event('change'));
            
            // Scroll to form
            ttsForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            // Show confirmation message
            const tempAlert = document.createElement('div');
            tempAlert.className = 'alert alert-info alert-dismissible fade show mt-2';
            tempAlert.innerHTML = `
                <i class="fas fa-redo me-2"></i>
                Form telah diisi dengan data riwayat. Klik "Konversi ke Suara" untuk mengulang konversi.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            ttsForm.appendChild(tempAlert);
            
            setTimeout(() => {
                if (tempAlert.parentNode) {
                    tempAlert.remove();
                }
            }, 5000);
        }
    };

    // Event Listeners
      // Handle form submission
    ttsForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const text = textInput.value.trim();
        const speed = speedSelect.value;
        const format = formatSelect.value;
        const gender = genderSelect.value;
        const engine = engineSelect.value;

        // Validate input
        if (!text) {
            showError('Silakan masukkan teks yang ingin dikonversi.');
            return;
        }

        if (text.length < 3) {
            showError('Teks minimal harus 3 karakter.');
            return;
        }

        // Show loading state and progress
        setLoadingState(true);
        hideResults();
        showProgress('Memproses Konversi...');

        // Simulate progress while making request
        let progressComplete = false;
        simulateProgress(() => {
            progressComplete = true;
        });

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    speed: speed,
                    format: format,
                    gender: gender,
                    engine: engine
                })
            });

            const data = await response.json();
            
            // Wait for progress to complete
            while (!progressComplete) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }

            if (response.ok && data.success) {
                // Add to history
                addToHistory({
                    text: text,
                    filename: data.filename,
                    engine: data.engine,
                    gender: gender,
                    speed: speed,
                    format: format
                });
                
                showSuccess(data.filename, format, data.engine || 'unknown', data.voice_info);
            } else {
                showError(data.error || 'Terjadi kesalahan saat memproses permintaan.');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Terjadi kesalahan koneksi. Silakan coba lagi.');
        } finally {
            setLoadingState(false);
            hideProgress();
        }
    });

    // Clear history button
    clearHistoryBtn.addEventListener('click', function() {
        if (confirm('Yakin ingin menghapus semua riwayat konversi?')) {
            clearHistory();
        }
    });

    // Handle engine selection change
    engineSelect.addEventListener('change', function() {
        const selectedEngine = this.value;
        if (selectedEngine === 'auto') {
            engineHelp.textContent = 'Mode AUTO akan memilih engine terbaik berdasarkan gender yang dipilih';
            genderHelp.textContent = 'Mode AUTO akan mengoptimalkan pemilihan engine untuk gender ini';
            formatSelect.innerHTML = '<option value="mp3" selected>MP3</option>';
        } else if (selectedEngine === 'gtts') {
            engineHelp.textContent = 'Google TTS menggunakan suara alami bahasa Indonesia';
            genderHelp.textContent = 'Google TTS: Variasi suara berdasarkan domain';
            formatSelect.innerHTML = '<option value="mp3" selected>MP3</option>';
        } else {
            engineHelp.textContent = 'Windows TTS mendukung multiple gender dengan suara David & Zira';
            genderHelp.textContent = 'Pilih gender suara Windows TTS (David/Zira)';
            formatSelect.innerHTML = `
                <option value="mp3" selected>MP3</option>
                <option value="wav">WAV</option>
            `;
        }
    });

    // Handle gender selection change  
    genderSelect.addEventListener('change', function() {
        const selectedGender = this.value;
        const selectedEngine = engineSelect.value;
        
        if (selectedEngine === 'auto') {
            if (selectedGender === 'male') {
                genderHelp.textContent = '👨 Mode AUTO akan prioritaskan Windows TTS untuk suara laki-laki';
            } else {
                genderHelp.textContent = '👩 Mode AUTO akan prioritaskan Google TTS untuk suara perempuan';
            }
        }
    });    // Helper functions for UI state management
    function setLoadingState(isLoading) {
        if (isLoading) {
            convertBtn.disabled = true;
            btnText.textContent = 'Sedang Memproses...';
            loadingSpinner.classList.remove('d-none');
        } else {
            convertBtn.disabled = false;
            btnText.textContent = 'Konversi ke Suara';
            loadingSpinner.classList.add('d-none');
        }
    }

    function showSuccess(filename, format, engine, voiceInfo) {
        hideError();
        
        // Set audio source
        const audioSrc = `/play/${filename}`;
        audioPlayer.src = audioSrc;
        
        // Set download link
        downloadBtn.href = `/download/${filename}`;
        downloadBtn.download = filename;
        
        // Update success message with engine info
        const alertHeading = resultArea.querySelector('.alert-heading');
        alertHeading.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>Konversi Berhasil! 
            <small class="badge bg-success ms-2">${engine.toUpperCase()}</small>
        `;
        
        // Show result area with animation
        resultArea.classList.remove('d-none');
        resultArea.classList.add('fade-in');
        
        // Scroll to result
        resultArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function showError(message) {
        hideResults();
        errorMessage.textContent = message;
        errorArea.classList.remove('d-none');
        errorArea.classList.add('fade-in');
        
        // Scroll to error
        errorArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideResults() {
        resultArea.classList.add('d-none');
        resultArea.classList.remove('fade-in');
    }    function hideError() {
        errorArea.classList.add('d-none');
        errorArea.classList.remove('fade-in');
    }

    // Character counter and audio duration estimation
    const charCount = document.getElementById('charCount');

    function estimateAudioDuration(text, speed = 'normal') {
        // Average speaking rate: normal = 150 wpm, slow = 120 wpm, fast = 180 wpm
        const wordsPerMinute = {
            'slow': 120,
            'normal': 150,
            'fast': 180
        };
        
        const words = text.trim().split(/\s+/).length;
        const minutes = words / wordsPerMinute[speed];
        const seconds = Math.round(minutes * 60);
        
        if (seconds < 60) {
            return `~${seconds}s`;
        } else {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `~${mins}m ${secs}s`;
        }
    }

    function updateCharCount() {
        const text = textInput.value;
        const length = text.length;
        const maxLength = 500;
        
        charCount.textContent = `${length}/${maxLength}`;
        
        if (length > maxLength * 0.9) {
            charCount.className = 'text-warning fw-bold';
        } else if (length > maxLength * 0.7) {
            charCount.className = 'text-info';
        } else {
            charCount.className = 'text-muted';
        }
        
        // Add duration estimation
        if (length > 0) {
            const speed = speedSelect.value;
            const duration = estimateAudioDuration(text, speed);
            charCount.textContent += ` | Durasi: ${duration}`;
        }    }

    // Auto-hide alerts after some time
    function autoHideAlert(element, delay = 10000) {
        setTimeout(() => {
            if (!element.classList.contains('d-none')) {
                element.style.transition = 'opacity 0.5s ease';
                element.style.opacity = '0';
                setTimeout(() => {
                    element.classList.add('d-none');
                    element.style.opacity = '1';
                }, 500);
            }
        }, delay);
    }

    // File size estimation (rough estimate)
    function estimateFileSize(text, format = 'mp3') {
        // Very rough estimate: MP3 ~1KB per second, WAV ~10KB per second
        const duration = estimateAudioDuration(text, speedSelect.value);
        const seconds = parseInt(duration.match(/\d+/)[0]);
        
        if (format === 'mp3') {
            return `~${Math.round(seconds * 1)}KB`;
        } else {
            return `~${Math.round(seconds * 10)}KB`;
        }
    }

    // Enhanced form validation with size estimation
    function validateForm() {
        const text = textInput.value.trim();
        if (!text) return false;
        if (text.length < 3) return false;
        
        // Show estimated file size
        const format = formatSelect.value;
        const estimatedSize = estimateFileSize(text, format);
        console.log(`Estimated file size: ${estimatedSize}`);
        
        return true;
    }

    // Enhanced input event listeners
    textInput.addEventListener('input', function() {
        const maxLength = 500;
        if (this.value.length > maxLength) {
            this.value = this.value.substring(0, maxLength);
        }
        updateCharCount();
    });    speedSelect.addEventListener('change', updateCharCount);

    // Initialize counters
    updateCharCount();

    // Preview functionality
    previewBtn.addEventListener('click', async function() {
        const text = textInput.value.trim();
        
        if (!text) {
            showError('Silakan masukkan teks untuk preview.');
            return;
        }
        
        // Use first 50 characters for preview
        const previewText = text.substring(0, 50);
        if (text.length > 50) {
            const confirmed = confirm('Teks akan dipotong menjadi 50 karakter pertama untuk preview. Lanjutkan?');
            if (!confirmed) return;
        }
        
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating Preview...';
        
        try {
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: previewText,
                    speed: speedSelect.value,
                    format: 'mp3',
                    gender: genderSelect.value,
                    engine: engineSelect.value,
                    preview: true
                })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                audioPlayer.src = `/play/${data.filename}`;
                audioPlayer.play();
                
                // Show a temporary message
                const tempAlert = document.createElement('div');
                tempAlert.className = 'alert alert-info alert-dismissible fade show mt-2';
                tempAlert.innerHTML = `
                    <i class="fas fa-info-circle me-2"></i>
                    Preview berhasil dibuat (50 karakter pertama)
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                previewBtn.parentNode.appendChild(tempAlert);
                
                setTimeout(() => {
                    if (tempAlert.parentNode) {
                        tempAlert.remove();
                    }
                }, 5000);
            } else {
                showError(data.error || 'Gagal membuat preview.');
            }
        } catch (error) {
            showError('Terjadi kesalahan saat membuat preview.');
        } finally {
            this.disabled = false;
            this.innerHTML = '<i class="fas fa-eye me-2"></i>Preview (50 karakter)';
        }
    });
});
