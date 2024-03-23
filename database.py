import sqlite3

conn = sqlite3.connect('medical_data.db')

cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_data (
               id INTEGER PRIMARY KEY,
               username TEXT NOT NULL,
               email TEXT NOT NULL,
               password_hash TEXT NOT NULL )
''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS breast_cancer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concave_points_mean REAL NOT NULL,
            area_mean REAL NOT NULL,
            radius_mean REAL NOT NULL,
            perimeter_mean REAL NOT NULL,
            concavity_mean REAL NOT NULL,
            result INTEGER
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS diabetes_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregnancies INTEGER NOT NULL,
            glucose REAL NOT NULL,
            blood_pressure REAL NOT NULL,
            bmi REAL NOT NULL,
            diabetes_pedigree_function REAL NOT NULL,
            age INTEGER NOT NULL,
            result INTEGER
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS heart_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chest_pain_type INTEGER NOT NULL,
            resting_blood_pressure REAL NOT NULL,
            serum_cholesterol REAL NOT NULL,
            fasting_blood_sugar INTEGER NOT NULL,
            resting_ecg INTEGER NOT NULL,
            max_heart_rate_achieved REAL NOT NULL,
            exercise_induced_angina INTEGER NOT NULL,
            result INTEGER
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS kidney_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blood_pressure REAL NOT NULL,
            specific_gravity REAL NOT NULL,
            albumin INTEGER NOT NULL,
            blood_sugar_level INTEGER NOT NULL,
            red_blood_cells_count INTEGER NOT NULL,
            pus_cell_count INTEGER NOT NULL,
            pus_cell_clumps INTEGER NOT NULL,
            result INTEGER
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS liver_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_bilirubin REAL NOT NULL,
            direct_bilirubin REAL NOT NULL,
            alkaline_phosphotase REAL NOT NULL,
            alamine_aminotransferase REAL NOT NULL,
            total_proteins REAL NOT NULL,
            albumin REAL NOT NULL,
            albumin_and_globulin_ratio REAL NOT NULL,
            result INTEGER
        )
    ''')

conn.commit()
conn.close()