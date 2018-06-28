FROM kennethreitz/pipenv

COPY . /app

RUN pipenv update

CMD pipenv run python3 src/main.py