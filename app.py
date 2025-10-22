from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_models import predict_demand, optimize_route
import pandas as pd

app = Flask(__name__)
CORS(app)

# Demo data
df = pd.read_csv("demo_data.csv")

@app.route("/api/demand", methods=["GET"])
def demand():
    product = request.args.get("product", "Product A")
    forecast = predict_demand(product)
    return jsonify({"product": product, "forecast": forecast})

@app.route("/api/route", methods=["POST"])
def route():
    data = request.json
    locations = data.get("locations", [[23.8103,90.4125],[23.8110,90.4150]]) # Dhaka demo
    optimized = optimize_route(locations)
    return jsonify({"optimized_route": optimized})

if __name__ == "__main__":
    app.run(debug=True)
