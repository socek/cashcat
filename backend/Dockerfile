FROM python:3.7

RUN pip install pipenv
RUN useradd -U user && mkdir /home/user && chown user:user /home/user

ENV PYTHONUNBUFFERED 1
ENV APP_DIR /code
WORKDIR $APP_DIR
RUN mkdir -p /app.egg-info && ln -s ../app.egg-info cashcat.egg-info && chown user:user /app.egg-info

USER user
COPY --chown=user:user code/Pipfile $APP_DIR
COPY --chown=user:user code/Pipfile.lock $APP_DIR
RUN pipenv install

COPY --chown=user:user code $APP_DIR
RUN pipenv run python setup.py develop

CMD ./scripts/start_webapp

EXPOSE 8000
