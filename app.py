import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    return jsonify(status="ok")

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Kairos Calculator</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root{--bg:#0f0f0f; --panel:#171717; --card:#1e1e1e; --ink:#efefef; --muted:#bdbdbd; --line:#2b2b2b; --gold:#c9a646; --gold-2:#e2c876; --accent:#ffffff;}
  *{box-sizing:border-box}
  body{font-family:Montserrat,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);margin:0}
  header{position:sticky;top:0;background:linear-gradient(180deg,#121212,#0f0f0f);border-bottom:2px solid var(--gold);padding:16px 20px;display:flex;align-items:center;gap:14px;z-index:5}
  .kbox{width:28px;height:28px;border:2px solid var(--gold);display:grid;place-items:center;border-radius:4px;font-weight:700;color:var(--gold)}
  h1{margin:0;font-size:18px;letter-spacing:1.5px;color:var(--gold)}
  main{max-width:1000px;margin:0 auto;padding:20px;display:grid;grid-template-columns:1fr 1fr;gap:20px}
  @media (max-width:920px){ main{grid-template-columns:1fr} }
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}
  .panel h2{margin:0 0 12px;font-size:16px;color:var(--accent);letter-spacing:1px}
  .row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  .row3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
  label{font-size:12px;color:var(--muted)}
  input{width:100%;padding:10px 12px;margin-top:6px;background:#242424;border:1px solid var(--line);border-radius:8px;color:var(--ink);font-size:14px}
  .btn{margin-top:14px;padding:12px 14px;background:var(--gold);color:#111;font-weight:700;border:0;border-radius:10px;cursor:pointer;width:100%;box-shadow:0 0 0 1px #0006}
  .btn:hover{background:var(--gold-2)}
  .preset-bar{display:flex;flex-wrap:wrap;gap:10px;margin:-4px 0 12px}
  .chip{border:1px solid var(--gold);color:var(--gold);padding:8px 10px;border-radius:999px;font-size:12px;cursor:pointer;background:transparent}
  .chip:hover{background:#3a2f10}
  .results{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}
  ul{list-style:none;padding:0;margin:0}
  li{padding:8px 0;border-bottom:1px dashed var(--line)}
  li:last-child{border-bottom:0}
  .err{color:#ff6b6b;font-weight:700}
  .sub{color:var(--muted);font-size:12px;margin:6px 0 0}
</style>
<script>
  function fillPreset(p){
    const d = {
      "bedside": {length:500, width:400, thickness:25, legs:2, leg_w:300, leg_h:450, leg_t:60},
      "coffee_core": {length:1100, width:650, thickness:25, legs:2, leg_w:320, leg_h:650, leg_t:70},
      "lamp": {length:180, width:180, thickness:15, legs:1, leg_w:180, leg_h:400, leg_t:15},
      "hero": {length:1200, width:700, thickness:30, legs:2, leg_w:340, leg_h:650, leg_t:80}
    }[p];
    if(!d) return;
    for (const k in d){ const el = document.querySelector('[name="'+k+'"]'); if(el){ el.value = d[k]; } }
    const btn = document.getElementById('calcBtn'); btn.animate([{transform:'scale(1)'},{transform:'scale(1.03)'},{transform:'scale(1)'}],{duration:300});
  }
</script>
</head>
<body>
  <header>
    <div class="kbox">K</div>
    <h1>KAIROS — Artifact Calculator</h1>
  </header>
  <main>
    <section class="panel">
      <h2>Presets</h2>
      <div class="preset-bar">
        <button type="button" class="chip" onclick="fillPreset('bedside')">Bedside (Core)</button>
        <button type="button" class="chip" onclick="fillPreset('coffee_core')">Coffee #02 (Core)</button>
        <button type="button" class="chip" onclick="fillPreset('lamp')">Lamp (Entry)</button>
        <button type="button" class="chip" onclick="fillPreset('hero')">Coffee #03 (Hero)</button>
      </div>
      <p class="sub">Tap a preset, tweak any numbers, then press Calculate.</p>
    </section>

    <section class="panel">
      <h2>Inputs (mm)</h2>
      <form method="POST" novalidate>
        <div class="row">
          <div><label>Top Length<input type="number" name="length" required></label></div>
          <div><label>Top Width<input type="number" name="width" required></label></div>
        </div>
        <div class="row3">
          <div><label>Top Thickness<input type="number" name="thickness" required></label></div>
          <div><label># Legs<input type="number" name="legs" required></label></div>
          <div></div>
        </div>
        <div class="row3">
          <div><label>Leg Width<input type="number" name="leg_w" required></label></div>
          <div><label>Leg Height<input type="number" name="leg_h" required></label></div>
          <div><label>Leg Thickness<input type="number" name="leg_t" required></label></div>
        </div>
        <button id="calcBtn" class="btn" type="submit">Calculate</button>
      </form>
      {% if error %}<p class="err">{{ error }}</p>{% endif %}
    </section>

    {% if result %}
    <section class="results">
      <h2>Results</h2>
      <ul>
        <li><b>Total Volume:</b> {{ result.total_vol }} m³</li>
        <li><b>Premix Mass:</b> {{ result.premix_mass }} kg ({{ result.bags }} bags)</li>
        <li><b>Premix Cost:</b> ${{ result.premix_cost }}</li>
        <li><b>Fibres:</b> {{ result.fibres_kg }} kg — ${{ result.fibres_cost }}</li>
        <li><b>Oxide:</b> {{ result.oxide_kg }} kg — ${{ result.oxide_cost }}</li>
        <li><b>Resin:</b> ${{ result.resin_cost }}</li>
        <li><b>Packaging:</b> ${{ result.packaging_cost }}</li>
        <li><b>Plaque:</b> ${{ result.plaque_cost }}</li>
        <li><b>Total Cost:</b> ${{ result.total_cost }}</li>
        <li><b>Est. Final Weight:</b> {{ result.final_weight }} kg</li>
      </ul>
    </section>
    {% endif %}
  </main>
</body>
</html>"""

def to_float(v):
    if v is None or str(v).strip() == "":
        raise ValueError("Missing value")
    return float(v)

def calculate(form):
    length = to_float(form.get("length")) / 1000
    width  = to_float(form.get("width"))  / 1000
    thick  = to_float(form.get("thickness")) / 1000
    legs   = int(to_float(form.get("legs")))
    leg_w  = to_float(form.get("leg_w")) / 1000
    leg_h  = to_float(form.get("leg_h")) / 1000
    leg_t  = to_float(form.get("leg_t")) / 1000

    top_vol = length * width * thick
    leg_vol = legs * (leg_w * leg_h * leg_t)
    total_vol = top_vol + leg_vol

    kg_per_m3 = 2000.0
    premix_mass = total_vol * kg_per_m3
    bags = premix_mass / 20.0
    premix_cost = bags * 41.25

    backer_bags = bags * 0.7
    fibres_kg = backer_bags * 0.5
    fibres_cost = fibres_kg * 5.0

    oxide_kg = premix_mass * 0.03
    oxide_cost = oxide_kg * 17.29

    resin_cost = 6.0
    packaging_cost = 165.0
    plaque_cost = 100.0

    total_cost = premix_cost + fibres_cost + oxide_cost + resin_cost + packaging_cost + plaque_cost

    return {
        "total_vol": round(total_vol, 4),
        "premix_mass": round(premix_mass, 1),
        "bags": round(bags, 2),
        "premix_cost": round(premix_cost, 2),
        "fibres_kg": round(fibres_kg, 2),
        "fibres_cost": round(fibres_cost, 2),
        "oxide_kg": round(oxide_kg, 2),
        "oxide_cost": round(oxide_cost, 2),
        "resin_cost": resin_cost,
        "packaging_cost": packaging_cost,
        "plaque_cost": plaque_cost,
        "total_cost": round(total_cost, 2),
        "final_weight": round(premix_mass + fibres_kg + oxide_kg, 1),
    }

@app.route("/", methods=["GET", "POST", "HEAD"])
def index():
    if request.method == "HEAD":
        return ("", 200)
    error = None
    result = None
    if request.method == "POST":
        try:
            result = calculate(request.form)
        except Exception as e:
            error = f"Please fill every box with a number. ({e})"
    return render_template_string(PAGE, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
