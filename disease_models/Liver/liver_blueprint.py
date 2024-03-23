# from flask import Blueprint, render_template
# import joblib
# from flask import request
# import numpy as np
#
# liver_blueprint = Blueprint("liver", __name__, template_folder="templates")
#
# @liver_blueprint.route("/liver")
# def liver():
#     return render_template("liver.html")
#
#
# def ValuePredictor(to_predict_list, size):
#     to_predict = np.array(to_predict_list).reshape(1, size)
#     if (size == 7):
#         loaded_model = joblib.load(
#             r'C:\Users\pradi\PycharmProjects\Health-App-main\disease_models\Liver\liver_model.pkl')
#         result = loaded_model.predict(to_predict)
#     return result[0]
#
#
# @liver_blueprint.route('/predict', methods=["POST"])
# def predict():
#     if request.method == "POST":
#         to_predict_list = request.form.to_dict()
#         to_predict_list = list(to_predict_list.values())
#         to_predict_list = list(map(float, to_predict_list))
#         # liver
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

liver_blueprint = Blueprint("liver", __name__, template_folder="templates")

@liver_blueprint.route("/liver")
def liver():
    return render_template("liver.html")

def insert_liver_data(total_bilirubin, direct_bilirubin, alkaline_phosphotase,
                      alamine_aminotransferase, total_proteins, albumin,
                      albumin_and_globulin_ratio, result):
    conn = sqlite3.connect('medical_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO liver_predictions (
            total_bilirubin, direct_bilirubin, alkaline_phosphotase,
            alamine_aminotransferase, total_proteins, albumin,
            albumin_and_globulin_ratio, result
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (total_bilirubin, direct_bilirubin, alkaline_phosphotase,
          alamine_aminotransferase, total_proteins, albumin,
          albumin_and_globulin_ratio, result))
    conn.commit()
    conn.close()

def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if (size == 7):
        loaded_model = joblib.load(
            r'C:\Users\Lenovo\Downloads\Health-App-main-Updated\Health-App-main-Updated\disease_models\Liver\liver_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@liver_blueprint.route('/predict', methods=["POST"])
def predict():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        # liver
        if (len(to_predict_list) == 7):
            result = ValuePredictor(to_predict_list, 7)
            insert_liver_data(
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
    return (render_template("liverresult.html", prediction_text=prediction))
