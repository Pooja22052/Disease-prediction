# # disease_models/Breast_Cancer/breast_cancer_blueprint.py
# from flask import Blueprint, render_template, request
# import joblib
# import numpy as np
# breast_cancer_blueprint = Blueprint("breast_cancer", __name__, template_folder="templates", static_url_path='/static')
#
# @breast_cancer_blueprint.route("/cancer")
# def cancer():
#     return render_template("cancer.html")
#
#
# def ValuePredictor(to_predict_list, size):
#     to_predict = np.array(to_predict_list).reshape(1, size)
#     if (size == 5):
#         loaded_model = joblib.load(r'C:\Users\pradi\PycharmProjects\Health-App-main\disease_models\Breast_Cancer\cancer_model.pkl')
#         result = loaded_model.predict(to_predict)
#     return result[0]
#
#
# @breast_cancer_blueprint.route('/predict', methods=["POST"])
# def predict():
#     if request.method == "POST":
#         to_predict_list = request.form.to_dict()
#         to_predict_list = list(to_predict_list.values())
#         to_predict_list = list(map(float, to_predict_list))
#         # cancer
#         if (len(to_predict_list) == 5):
#             result = ValuePredictor(to_predict_list, 5)
#
#     if (int(result) == 1):
#         prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
#     else:
#         prediction = "No need to fear. You have no dangerous symptoms of the disease"
#     return (render_template("cancerresult.html", prediction_text=prediction))



# # disease_models/Breast_Cancer/breast_cancer_blueprint.py
# from flask import Blueprint, render_template, request
# import joblib
# import numpy as np
# import mysql.connector
#
# breast_cancer_blueprint = Blueprint("breast_cancer", __name__, template_folder="templates", static_url_path='/static')
#
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',  # Replace with your database password
#     'database': 'skypia_healthcare',
# }
#
# def connect_to_database():
#     try:
#         return mysql.connector.connect(**db_config)
#     except mysql.connector.Error as err:
#         print("Error connecting to the database: {}".format(err))
#         return None
#
#
# def save_to_database(to_predict_list):
#     try:
#         conn = connect_to_database()
#         if conn:
#             cursor = conn.cursor()
#
#             insert_query = "INSERT INTO cancer (concave_points_mean, area_mean, radius_mean, perimeter_mean, concavity_mean) VALUES (%s, %s, %s, %s, %s)"
#
#             # Convert the values to strings as all columns are of type TEXT
#             data = tuple(map(str, to_predict_list))
#
#             cursor.execute(insert_query, data)
#
#             conn.commit()
#
#             cursor.close()
#             conn.close()
#
#             print("Data inserted successfully")
#     except mysql.connector.Error as err:
#         print("Error: {}".format(err))
#
#
# @breast_cancer_blueprint.route("/cancer")
# def cancer():
#     return render_template("cancer.html")
#
# def value_predictor(to_predict_list, size):
#     if size == 5:
#         loaded_model_path = r'C:\Users\pradi\PycharmProjects\Health-App-main\disease_models\Breast_Cancer\cancer_model.pkl'
#         loaded_model = joblib.load(loaded_model_path)
#         to_predict = np.array(to_predict_list).reshape(1, size)
#         result = loaded_model.predict(to_predict)
#         return result[0]
#
# @breast_cancer_blueprint.route('/predict', methods=["POST"])
# def predict():
#     result = None
#     if request.method == "POST":
#         to_predict_list = [float(request.form.get(key)) for key in ['concave_points_mean', 'area_mean', 'radius_mean', 'perimeter_mean', 'concavity_mean']]
#         result = value_predictor(to_predict_list, 5)
#
#         # Save data to the database
#         save_to_database(to_predict_list)
#
#     if result is not None:
#         prediction = "Sorry, you have a risk of the disease. Please consult a doctor immediately." if int(result) == 1 else "No need to fear. You have no dangerous symptoms of the disease."
#         return render_template("cancerresult.html", prediction_text=prediction)
#     else:
#         return "Error in prediction."


# disease_models/Breast_Cancer/breast_cancer_blueprint.py
from flask import Blueprint, render_template, request
import joblib
import numpy as np
import sqlite3

breast_cancer_blueprint = Blueprint("breast_cancer", __name__, template_folder="templates", static_url_path='/static')


@breast_cancer_blueprint.route("/cancer")
def cancer():
    return render_template("cancer.html")


def insert_data(concave_points_mean, area_mean, radius_mean, perimeter_mean, concavity_mean, result):
    conn = sqlite3.connect('medical_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO breast_cancer (concave_points_mean, area_mean, radius_mean, perimeter_mean, concavity_mean, result)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (concave_points_mean, area_mean, radius_mean, perimeter_mean, concavity_mean, result))
    conn.commit()
    conn.close()


def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if (size == 5):
        loaded_model = joblib.load(
            r'C:\Users\Lenovo\Downloads\Health-App-main-Updated\Health-App-main-Updated\disease_models\Breast_Cancer\cancer_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@breast_cancer_blueprint.route('/predict', methods=["POST"])
def predict():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))

        # cancer
        if (len(to_predict_list) == 5):
            result = ValuePredictor(to_predict_list, 5)
            insert_data(
                to_predict_list[0],
                to_predict_list[1],
                to_predict_list[2],
                to_predict_list[3],
                to_predict_list[4],
                result
            )

    if (int(result) == 1):
        prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    return (render_template("cancerresult.html", prediction_text=prediction))
