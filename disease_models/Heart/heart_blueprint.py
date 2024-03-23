# from flask import Blueprint, render_template
# import joblib
# from flask import request
# import numpy as np
#
# heart_blueprint = Blueprint("heart", __name__, template_folder="templates")
#
# @heart_blueprint.route("/heart")
# def heart():
#     return render_template("heart.html")
#
#
# def ValuePredictor(to_predict_list, size):
#     to_predict = np.array(to_predict_list).reshape(1, size)
#     if (size == 7):
#         loaded_model = joblib.load(r'C:\Users\pradi\PycharmProjects\Health-App-main\disease_models\Heart\heart_model.pkl')
#         result = loaded_model.predict(to_predict)
#     return result[0]
#
#
# @heart_blueprint.route('/predict', methods=["POST"])
# def predict():
#     if request.method == "POST":
#         to_predict_list = request.form.to_dict()
#         to_predict_list = list(to_predict_list.values())
#         to_predict_list = list(map(float, to_predict_list))
#         # diabetes
#         if (len(to_predict_list) == 7):
#             result = ValuePredictor(to_predict_list, 7)
#
#     if (int(result) == 1):
#         prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
#     else:
#         prediction = "No need to fear. You have no dangerous symptoms of the disease"
#     return (render_template("cancerresult.html", prediction_text=prediction))



from flask import Blueprint, render_template
import joblib
from flask import request
import numpy as np
import sqlite3

heart_blueprint = Blueprint("heart", __name__, template_folder="templates")

@heart_blueprint.route("/heart")
def heart():
    return render_template("heart.html")

def insert_heart_data(chest_pain_type, resting_blood_pressure, serum_cholesterol,
                      fasting_blood_sugar, resting_ecg, max_heart_rate_achieved,
                      exercise_induced_angina, result):
    conn = sqlite3.connect('medical_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO heart_predictions (
            chest_pain_type, resting_blood_pressure, serum_cholesterol,
            fasting_blood_sugar, resting_ecg, max_heart_rate_achieved,
            exercise_induced_angina, result
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (chest_pain_type, resting_blood_pressure, serum_cholesterol,
          fasting_blood_sugar, resting_ecg, max_heart_rate_achieved,
          exercise_induced_angina, result))
    conn.commit()
    conn.close()


def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if (size == 7):
        loaded_model = joblib.load(r'C:\Users\Lenovo\Downloads\Health-App-main-Updated\Health-App-main-Updated\disease_models\Heart\heart_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@heart_blueprint.route('/predict', methods=["POST"])
def predict():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        # diabetes
        if (len(to_predict_list) == 7):
            result = ValuePredictor(to_predict_list, 7)
            insert_heart_data(
                to_predict_list[0],
                to_predict_list[1],
                to_predict_list[2],
                to_predict_list[3],
                to_predict_list[4],
                to_predict_list[5],
                to_predict_list[6],
                result
            )

    if (int(result) == 1):
        prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    return (render_template("heartresult.html", prediction_text=prediction))
