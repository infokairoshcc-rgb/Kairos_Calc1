# Kairos Artifact Calculator — Presets + Polished
- Presets: Bedside, Coffee #02, Lamp, Hero
- Single-file app, safe on Render

Deploy:
- Push app.py, requirements.txt, render.yaml to GitHub (repo root)
- Render → New → Web Service → connect repo
- Build: pip install -r requirements.txt
- Start: gunicorn -b 0.0.0.0:$PORT app:app
- Health: /healthz → {"status":"ok"}
