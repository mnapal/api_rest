# api_rest
## Flask API for Loading Data in a Data Base from CSV files


This endpoint (`/load_departments`) is designed to load department data from a CSV file into a database. 

This endpoint (`/load_jobs`) is designed to load job data from a CSV file into a database. 

This endpoint (`/load_hired_employees`) is designed to load department data from a CSV file into a database. 

This endpoint (`/employees_by_department`) is designed to return the number of employees hired for each job and department in 2021 divided by quarter.

This endpoint (`/total_of_employees_by_department`) is designed to return a list of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments.





## Building and Running the Application

### Build the App Image
To build the application image, clone the repository using the following command:

```bash
git clone https://github.com/mnapal/api_rest.git
```

Navigate to the root directory and execute the command:

```bash
docker build -t flask-appi .
```

### Run the Application Container
Run the container for the application using the following command:

```bash
docker run --name flask-app-name --network flask_net flask-appi
```

### Access the App
Access the running app by visiting the following URL: 

`http://HOST:4001/test`

Replace HOST with the actual host where the application is running.


