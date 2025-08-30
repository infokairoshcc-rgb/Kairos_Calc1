# Kairos Artifact Calculator

A lightweight Flask web app to calculate **Kairos artifact costs and materials** based on dimensions and build type.  
Styled with Kairos’ brutalist black/grey + gold palette and Montserrat font.

---

## 🚀 Running Locally

1. Install Python 3.10+ and pip.  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.  
   - On iPad: make sure your laptop + iPad are on same Wi‑Fi.  
   - Find your laptop’s IP (e.g. `192.168.0.12`) and open `http://192.168.0.12:5000` on your iPad.  
5. On iPad Safari → Share → “Add to Home Screen” → you now have a Kairos calculator app icon.

---

## 🌐 Deploy Online (Recommended for easy iPad access)

1. Create a new GitHub repo (e.g. `kairos-calculator`).  
2. Upload all files from this folder.  
3. Go to [https://render.com](https://render.com), create a free account.  
4. Click **New → Web Service → Connect to GitHub**.  
5. Select your repo. Render will auto-detect Flask via `requirements.txt` and `render.yaml`.  
6. Deploy — you’ll get a live URL you can bookmark or add to your iPad’s home screen.

---

## Next Steps
- Add presets for Bedside, Coffee #02, Hero Table, Lamp.  
- Add CSV export to feed into your **Kairos Notion Artifact Library**.  
- Add user authentication if you want to track multiple clients/orders.  
