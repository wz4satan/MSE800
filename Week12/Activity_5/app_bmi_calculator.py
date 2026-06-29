from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def bmi_calculator():
    bmi = None
    category = None

    if request.method == "POST":
        try:
            weight = float(request.form.get("weight", "0"))
            height = float(request.form.get("height", "0"))

            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be greater than zero.")

            bmi = round(weight / (height**2), 2)

            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 24:
                category = "Normal weight"
            elif 24 <= bmi < 28:
                category = "Overweight"
            else:
                category = "Obese"
        except ValueError as e:
            bmi = f"Invalid input: {e}"

    return render_template("index.html", bmi=bmi, category=category)
    # Render the 'index.html' template, passing the calculated 'bmi' and 'category' values from Python to the HTML variables for displaying the results.


if __name__ == "__main__":
    app.run(debug=True, port=5002)
