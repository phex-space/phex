FROM node:lts

WORKDIR /opt/app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "start"]
