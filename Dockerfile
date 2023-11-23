FROM python:3.12
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install flask
RUN pip install flask_smorest
RUN pip install python-dotenv
RUN pip install flask-sqlalchemy
RUN pip install flask-jwt-extended
RUN pip install passlib
RUN pip install flask_migrate
COPY . .
CMD ["flask","run","--host","0.0.0.0"]