from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from models import HiredEmployees, Job, Department, engine

app = Flask(__name__)



# create a test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "test"}), 200


# Endpoint to load hired employees data
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

        return jsonify({"message": "Hired employees data inserted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to load job data
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

        return jsonify({"message": "Job data inserted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to load department data
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

        return jsonify({"message": "Department data inserted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to get employees by department divided by quarter
@app.route('/employees_by_department', methods=['GET'])
def employees_by_department():
    try:
        # Execute the provided SQL query
        Session = sessionmaker(bind=engine)
        session = Session()
        query_result = session.execute(text("""
            SELECT department, job, sum(q1) as q1, sum(q2) as q2, sum(q3) as q3, sum(q4) as q4
            FROM (select department_id, job_id, 
                    case when hire_datetime between '2021-01-01 00:00:00' and '2021-03-31 23:59:59.999' then 1 else 0 end as q1,
                    case when hire_datetime between '2021-04-01 00:00:00' and '2021-06-30 23:59:59.999' then 1 else 0 end as q2,
                    case when hire_datetime between '2021-07-01 00:00:00' and '2021-09-30 23:59:59.999' then 1 else 0 end as q3,
                    case when hire_datetime between '2021-10-01 00:00:00' and '2021-12-31 23:59:59.999' then 1 else 0 end as q4
                  from public.hired_employees
                  where EXTRACT(YEAR FROM hire_datetime) = 2021
                  ) as e
            INNER JOIN departments as d on e.department_id = d.id
            INNER JOIN jobs as j on e.job_id = j.id
            GROUP BY department, job
            ORDER BY department, job
            """))

        result_data = [{'department': item[0], 'job': item[1], 'q1': item[2], 'q2': item[3], 'q3': item[4], 'q4': item[5]} for item in query_result]
        return jsonify({"data": result_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to get the total of employees by department > mean of employees hired
@app.route('/total_of_employees_by_department', methods=['GET'])
def total_of_employees_by_department():
    try:
        # Execute the provided SQL query
        Session = sessionmaker(bind=engine)
        session = Session()
        query_result = session.execute(text("""
            SELECT d.id as id, department, count(1) as "total_hired"
            FROM hired_employees as e
            INNER JOIN departments as d on e.department_id = d.id
            WHERE EXTRACT(YEAR FROM hire_datetime) = 2021
            GROUP BY d.id, department
            HAVING count(1)  > (select avg(total_hired)
                                from (select department_id, count(1) as total_hired 
                                      from hired_employees he 
                                      where EXTRACT(YEAR FROM hire_datetime) = 2021
                                      group by department_id
                                ) as mean) 
            ORDER BY total_hired desc
            """))

        result_data = [{'id': item[0], 'department': item[1], 'total_hired': item[2]} for item in query_result]
        return jsonify({"data": result_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)
