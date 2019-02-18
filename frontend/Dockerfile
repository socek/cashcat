FROM node:8.15.0 as builder
RUN mkdir -p /code
ENV PATH="${HOME}/.yarn/bin:${HOME}/.config/yarn/global/node_modules/.bin:${PATH}"

WORKDIR /code

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install -y google-chrome-stable

RUN curl --compressed -o- -L https://yarnpkg.com/install.sh | bash

ADD code/package.json .
RUN yarn install
RUN yarn add @babel/runtime
COPY code /code
CMD npm run dev

FROM builder AS frontend

RUN yarn build --force

FROM nginx:1.15.7-alpine
WORKDIR /usr/share/nginx/html

COPY --from=frontend /code/dist .
RUN find .

