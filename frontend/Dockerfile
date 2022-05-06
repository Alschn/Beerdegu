# Use an official node runtime as a parent image
FROM node:14.17.5-alpine

WORKDIR /app/frontend

# Install dependencies
COPY package.json .

# install dependencies and avoid `node-gyp rebuild` errors
RUN apk add --virtual .gyp python make g++ bash && \
    npm install && \
    apk del .gyp

# Add rest of the client code
COPY . .

EXPOSE 3000

CMD ["npm", "start"]
