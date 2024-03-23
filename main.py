from flask import Flask, render_template
from disease_models.Breast_Cancer.breast_cancer_blueprint import breast_cancer_blueprint
from disease_models.Diabetes.diabetes_blueprint import diabetes_blueprint
from disease_models.Heart.heart_blueprint import heart_blueprint
from disease_models.Kidney.kidney_blueprint import kidney_blueprint
from disease_models.Liver.liver_blueprint import liver_blueprint



# Import other Blueprints as needed
app = Flask(__name__)

# Register Blueprints for each disease model
app.register_blueprint(breast_cancer_blueprint, url_prefix="/cancer")
app.register_blueprint(diabetes_blueprint, url_prefix='/diabetes')
app.register_blueprint(heart_blueprint, url_prefix='/heart')
app.register_blueprint(kidney_blueprint, url_prefix='/kidney')
app.register_blueprint(liver_blueprint, url_prefix='/liver')



# Register other Blueprints as needed
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
