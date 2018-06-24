FROM python:3.6

RUN useradd -U user

ENV PYTHONUNBUFFERED 1
ENV APP_DIR /code
WORKDIR $APP_DIR
RUN mkdir -p /app.egg-info && ln -s ../app.egg-info PROJECT.egg-info

COPY code/requirements.txt $APP_DIR
RUN pip install -r requirements.txt --no-cache-dir

COPY --chown=user:user code $APP_DIR
RUN python setup.py develop

CMD ./scripts/start_webapp

USER user
EXPOSE 8000

