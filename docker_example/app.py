import numpy as np
import joblib
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# california.joblib should be in the same folder as app.py
obj = joblib.load("california.joblib")

model = obj["model"]
cols = obj["columns"]


@app.route("/")
def home():
    return render_template("index.html", columns=cols)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if data is None:
            data = request.form.to_dict()

        values = []

        for col in cols:
            value = data.get(col)

            if value is None or str(value).strip() == "":
                return jsonify({
                    "success": False,
                    "error": f"Missing value for: {col}"
                }), 400

            try:
                values.append(float(value))
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": f"Invalid number for: {col}"
                }), 400

        input_data = np.array([values], dtype=float)

        output = model.predict(input_data)

        prediction = float(output[0])

        return jsonify({
            "success": True,
            "prediction": prediction
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)