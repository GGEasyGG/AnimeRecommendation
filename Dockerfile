FROM python:3.10

RUN mkdir /root/Recsys

WORKDIR /root/Recsys

COPY Pipfile Pipfile.lock flask_app.py anime.csv dataset.csv model_knn.pkl ./

RUN mkdir ./templates

COPY ./templates ./templates/

RUN pip install pipenv

RUN pipenv install --system --deploy --dev

EXPOSE 8000

ENTRYPOINT ["python", "flask_app.py"]
