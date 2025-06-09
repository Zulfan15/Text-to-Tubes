"""
Setup script untuk Google Cloud Text-to-Speech
Jalankan script ini untuk menginstall dependencies dan setup authentication
"""

import subprocess
import sys
import os

def install_requirements():
    """Install dependencies from requirements.txt"""
    try:
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_google_cloud_auth():
    """Check if Google Cloud authentication is set up"""
    try:
        # Check if Google Cloud SDK is installed
        subprocess.check_call(["gcloud", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Google Cloud SDK is installed")
        
        # Check if authenticated
        result = subprocess.run(["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print(f"✅ Authenticated as: {result.stdout.strip()}")
            return True
        else:
            print("❌ Not authenticated with Google Cloud")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Google Cloud SDK not found")
        return False

def setup_authentication():
    """Guide user through authentication setup"""
    print("\n🔧 Setting up Google Cloud Text-to-Speech...")
    print("\nOptions to enable Google Cloud TTS:")
    print("1. Use Google Cloud SDK (Recommended)")
    print("2. Use Service Account Key File")
    print("3. Skip (use basic gTTS only)")
    
    choice = input("\nChoose option (1/2/3): ").strip()
    
    if choice == "1":
        print("\n📝 Steps to set up Google Cloud SDK:")
        print("1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install")
        print("2. Run: gcloud auth application-default login")
        print("3. Enable Text-to-Speech API in your Google Cloud project")
        print("4. Restart this application")
        
    elif choice == "2":
        print("\n📝 Steps to set up Service Account:")
        print("1. Go to Google Cloud Console")
        print("2. Create a Service Account with Text-to-Speech permissions")
        print("3. Download the JSON key file")
        print("4. Set environment variable:")
        print("   set GOOGLE_APPLICATION_CREDENTIALS=path\\to\\your\\service-account-file.json")
        
    elif choice == "3":
        print("✅ Skipping Cloud TTS setup. App will use basic gTTS only.")
        
    else:
        print("❌ Invalid choice")

def main():
    print("🚀 Google Cloud Text-to-Speech Setup")
    print("="*50)
    
    # Install requirements first
    if not install_requirements():
        return
    
    # Check authentication
    if check_google_cloud_auth():
        print("✅ Google Cloud TTS is ready to use!")
    else:
        setup_authentication()
    
    print("\n🎉 Setup complete! You can now run: python app.py")

if __name__ == "__main__":
    main()
