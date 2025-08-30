from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            # Inputs
            length = float(request.form["length"]) / 1000  # mm → m
            width = float(request.form["width"]) / 1000
            thickness = float(request.form["thickness"]) / 1000
            legs = int(request.form["legs"])
            leg_w = float(request.form["leg_w"]) / 1000
            leg_h = float(request.form["leg_h"]) / 1000
            leg_t = float(request.form["leg_t"]) / 1000

            # Volume calculations
            top_vol = length * width * thickness
            leg_vol = legs * (leg_w * leg_h * leg_t)
            total_vol = top_vol + leg_vol

            # Material & cost assumptions
            kg_per_m3 = 2000.0
            premix_mass = total_vol * kg_per_m3
            bags = premix_mass / 20
            premix_cost = bags * 41.25

            backer_bags = bags * 0.7
            fibres_kg = backer_bags * 0.5
            fibres_cost = fibres_kg * 5.0  # $100/20kg = $5/kg

            oxide_kg = premix_mass * 0.03  # 3% cap
            oxide_cost = oxide_kg * 17.29

            resin_cost = 6.0
            packaging_cost = 165.0
            plaque_cost = 100.0

            total_cost = premix_cost + fibres_cost + oxide_cost + resin_cost + packaging_cost + plaque_cost

            result = {
                "top_vol": round(top_vol, 4),
                "leg_vol": round(leg_vol, 4),
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
                "final_weight": round(premix_mass + fibres_kg + oxide_kg, 1)
            }
        except Exception as e:
            result = {"error": f"Invalid input: {e}"}
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
