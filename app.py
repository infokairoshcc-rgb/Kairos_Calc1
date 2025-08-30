import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    return jsonify(status="ok")

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Kairos Calculator</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body{font-family:Arial,Helvetica,sans-serif;background:#111;color:#eee;margin:0;padding:24px;}
  h1{color:#c9a646;margin:0 0 16px;}
  form{background:#1c1c1c;padding:16px;border-radius:8px;max-width:520px}
  label{display:block;margin:10px 0 6px}
  input{width:100%;padding:8px;background:#333;color:#fff;border:1px solid #555;border-radius:4px}
  button{margin-top:14px;padding:10px 14px;background:#c9a646;color:#111;font-weight:bold;border:0;border-radius:4px;cursor:pointer;width:100%}
  .card{background:#1c1c1c;margin-top:16px;padding:16px;border-radius:8px;max-width:520px}
  .err{color:#ff6b6b;font-weight:bold}
</style></head>
<body>
<h1>𐌊 KAIROS — Artifact Calculator</h1>

<form method="POST" novalidate>
  <label>Top Length (mm)</label><input type="number" name="length" required>
  <label>Top Width (mm)</label><input type="number" name="width" required>
  <label>Top Thickness (mm)</label><input type="number" name="thickness" required>

  <label># Legs</label><input type="number" name="legs" required>
  <label>Leg Width (mm)</label><input type="number" name="leg_w" required>
  <label>Leg Height (mm)</label><input type="number" name="leg_h" required>
  <label>Leg Thickness (mm)</label><input type="number" name="leg_t" required>

  <button type="submit">Calculate</button>
</form>

{% if error %}
  <div class="card"><p class="err">{{ error }}</p></div>
{% endif %}

{% if result %}
<div class="card">
  <h3>Results</h3>
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
</div>
{% endif %}
</body></html>"""

def to_float(v):
    if v is None or str(v).strip() == "":
        raise ValueError("Missing value")
    return float(v)

def calculate(form):
    # Inputs (mm → m)
    length = to_float(form.get("length")) / 1000
    width  = to_float(form.get("width"))  / 1000
    thick  = to_float(form.get("thickness")) / 1000
    legs   = int(to_float(form.get("legs")))
    leg_w  = to_float(form.get("leg_w")) / 1000
    leg_h  = to_float(form.get("leg_h")) / 1000
    leg_t  = to_float(form.get("leg_t")) / 1000

    # Volumes
    top_vol = length * width * thick
    leg_vol = legs * (leg_w * leg_h * leg_t)
    total_vol = top_vol + leg_vol

    # Materials & costs
    kg_per_m3 = 2000.0
    premix_mass = total_vol * kg_per_m3
    bags = premix_mass / 20.0
    premix_cost = bags * 41.25

    backer_bags = bags * 0.7
    fibres_kg = backer_bags * 0.5
    fibres_cost = fibres_kg * 5.0  # $100/20 kg

    oxide_kg = premix_mass * 0.03  # 3% cap
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