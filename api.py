from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import HiredEmployees, Job, Department, engine

app = Flask(__name__)



# create a test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "test"}), 200


@app.route('/load_hired_employees', methods=['POST'])
def load_hired_employees():
    try:
        url = 'https://raw.githubusercontent.com/mnapal/files/main/hired_employees.csv'
        column_names = ['id', 'name', 'hire_datetime', 'department_id', 'job_id']
        # Read CSV from url into a DataFrame
        df = pd.read_csv(url, names=column_names, header=0)
        # Replace null values by 'No name'
        df['name'] = df['name'].fillna('No Name')
        # Drop duplicate rows
        df = df.drop_duplicates()
        # Drop rows with null values
        df = df.dropna()
        # Convert column to datetime
        df['hire_datetime'] = pd.to_datetime(df['hire_datetime'], errors='coerce')
        # Convert column to numeric
        df['id'] = pd.to_numeric(df['id'], errors='coerce')
        df['job_id'] = pd.to_numeric(df['job_id'], errors='coerce')
        df['department_id'] = pd.to_numeric(df['department_id'], errors='coerce')
        # Convert DataFrame to list of dictionaries
        data_to_insert = df.to_dict(orient='records')
        # Save data to db
        Session = sessionmaker(bind=engine)
        session = Session()
        session.bulk_insert_mappings(HiredEmployees, data_to_insert)
        session.commit()

        return jsonify({"message": "Hired employee's data inserted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/load_jobs', methods=['POST'])
def load_jobs():
    try:
        url = 'https://raw.githubusercontent.com/mnapal/files/main/jobs.csv'
        column_names = ['id', 'job']
        # Read CSV from url into a DataFrame
        df = pd.read_csv(url, names=column_names, header=0)
        # Drop duplicate rows
        df = df.drop_duplicates()
        # Drop rows with null values
        df = df.dropna()
        # Convert column to numeric
        df['id'] = pd.to_numeric(df['id'], errors='coerce')
        # Convert DataFrame to list of dictionaries
        data_to_insert = df.to_dict(orient='records')
        # Save data to db
        Session = sessionmaker(bind=engine)
        session = Session()
        session.bulk_insert_mappings(Job, data_to_insert)
        session.commit()

        return jsonify({"message": "Job's data inserted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/load_departments', methods=['POST'])
def load_departments():
    try:
        url = 'https://raw.githubusercontent.com/mnapal/files/main/departments.csv'
        column_names = ['id', 'department']
        # Read CSV from url into a DataFrame
        df = pd.read_csv(url, names=column_names, header=0)
        # Drop duplicate rows
        df = df.drop_duplicates()
        # Drop rows with null values
        df = df.dropna()
        # Convert column to numeric
        df['id'] = pd.to_numeric(df['id'], errors='coerce')
        # Convert DataFrame to list of dictionaries
        data_to_insert = df.to_dict(orient='records')
        # Save data to db
        Session = sessionmaker(bind=engine)
        session = Session()
        session.bulk_insert_mappings(Department, data_to_insert)
        session.commit()

        return jsonify({"message": "Department's data inserted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(port=5050, debug=True)
