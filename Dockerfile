FROM python:3.6-slim-buster
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /app
ENV FLASK_APP=api
EXPOSE 4001
CMD [ "flask", "run", "--host=0.0.0.0", "--port=4001"]

