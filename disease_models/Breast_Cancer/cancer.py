import mysql.connector
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__, template_folder='templates')

# Replace the following database credentials with your own
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'cancer',
}


def connect_to_database():
    return mysql.connector.connect(**db_config)


def save_to_database(to_predict_list):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        insert_query = "INSERT INTO cancer (concave_points_mean, area_mean, radius_mean, perimeter_mean, concavity_mean) VALUES (%s, %s, %s, %s, %s)"
        data = tuple(to_predict_list)

        cursor.execute(insert_query, data)

        conn.commit()

        cursor.close()
        conn.close()

        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print("Error: {}".format(err))


def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if size == 5:
        loaded_model = joblib.load('cancer_model.pkl')
        result = loaded_model.predict(to_predict)
        return result[0]


@app.route("/")
@app.route("/cancer")
def cancer():
    return render_template("cancer.html")


@app.route('/predict', methods=["POST"])
def predict():
    if request.method == "POST":
        to_predict_list = [float(request.form['concave_points_mean']),
                           float(request.form['area_mean']),
                           float(request.form['radius_mean']),
                           float(request.form['perimeter_mean']),
                           float(request.form['concavity_mean'])]

        # Save form data to the MySQL database
        save_to_database(to_predict_list)

        # Perform cancer prediction based on the form data
        result = ValuePredictor(to_predict_list, 5)

        prediction_text = "Sorry, you have a high risk of breast cancer. Please consult a doctor immediately." if int(
            result) == 1 else "No need to fear. You have no dangerous symptoms of breast cancer."

        return jsonify({'prediction_text': prediction_text})


if __name__ == "__main__":
    app.run(debug=True)
