# # disease_models/Diabetes/diabetes_blueprint.py
# from flask import Blueprint, render_template
# import joblib
# from flask import request
# import numpy as np
#
# diabetes_blueprint = Blueprint("diabetes", __name__, template_folder="templates")
#
# @diabetes_blueprint.route("/diabetes")
# def diabetes():
#     return render_template("diabetes.html")
#
#
# def ValuePredictor(to_predict_list, size):
#     to_predict = np.array(to_predict_list).reshape(1, size)
#     if (size == 6):
#         loaded_model = joblib.load(r'C:\Users\pradi\PycharmProjects\Health-App-main\disease_models\Diabetes\diabetes_model.pkl')
#         result = loaded_model.predict(to_predict)
#     return result[0]
#
#
# @diabetes_blueprint.route('/predict', methods=["POST"])
# def predict():
#     if request.method == "POST":
#         to_predict_list = request.form.to_dict()
#         to_predict_list = list(to_predict_list.values())
#         to_predict_list = list(map(float, to_predict_list))
#         # diabetes
#         if (len(to_predict_list) == 6):
#             result = ValuePredictor(to_predict_list, 6)
#
#     if (int(result) == 1):
#         prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
#     else:
#         prediction = "No need to fear. You have no dangerous symptoms of the disease"
#     return (render_template("cancerresult.html", prediction_text=prediction))



# disease_models/Diabetes/diabetes_blueprint.py
from flask import Blueprint, render_template
import joblib
from flask import request
import numpy as np
import sqlite3

diabetes_blueprint = Blueprint("diabetes", __name__, template_folder="templates")

@diabetes_blueprint.route("/diabetes")
def diabetes():
    return render_template("diabetes.html")

def insert_diabetes_data(pregnancies, glucose, blood_pressure, bmi, diabetes_pedigree_function, age, result):
    conn = sqlite3.connect('medical_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO diabetes_predictions (pregnancies, glucose, blood_pressure, bmi, diabetes_pedigree_function, age, result)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (pregnancies, glucose, blood_pressure, bmi, diabetes_pedigree_function, age, result))
    conn.commit()
    conn.close()



def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if (size == 6):
        loaded_model = joblib.load(r'C:\Users\Lenovo\Downloads\Health-App-main-Updated\Health-App-main-Updated\disease_models\Diabetes\diabetes_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@diabetes_blueprint.route('/predict', methods=["POST"])
def predict():                                                                       
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        # diabetes
        if (len(to_predict_list) == 6):
            result = ValuePredictor(to_predict_list, 6)
            insert_diabetes_data(
                to_predict_list[0],
                to_predict_list[1],
                to_predict_list[2],
                to_predict_list[3],
                to_predict_list[4],
                to_predict_list[5],
                result
            )

    if (int(result) == 1):
        prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    return (render_template("diabetesresult.html", prediction_text=prediction))
