FROM node:8.1.3
RUN mkdir -p /code
ENV PATH="/data/node_modules/.bin:${PATH}"

WORKDIR /code
RUN mkdir -p ../node_modules && \
  ln -s ../node_modules && \
  apt-get update && \
  apt-get install apt-transport-https && \
  curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
  apt-get update && apt-get install yarn

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install -y google-chrome-stable

ADD code/package.json .
RUN yarn install -g
CMD npm run dev
