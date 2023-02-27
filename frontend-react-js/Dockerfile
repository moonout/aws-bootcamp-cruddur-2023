FROM node:16.19.1
ENV PORT=3000
EXPOSE ${PORT}


WORKDIR /frontend-react-js
COPY package.json .
RUN npm install


RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache

COPY . .

CMD ["npm", "run", "start"]
