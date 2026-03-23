FROM node:16-bullseye

WORKDIR /home/nodbrary

COPY package.json ./
RUN npm install --omit=dev --legacy-peer-deps

COPY . .

ENV NODE_ENV=production

CMD ["npm", "run", "start"]
