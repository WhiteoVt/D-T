FROM node:18-alpine as BUILD_IMAGE

WORKDIR /react_app

COPY package.json .

RUN npm install

COPY . .

RUN npm run build



FROM node:18-alpine as PRODUCTION_IMAGE

WORKDIR /react_app

COPY --from=BUILD_IMAGE /react_app/dist/ /react_app/dist/
EXPOSE 3000

COPY package.json .
COPY vite.config.ts .

RUN npm install typescript

EXPOSE 3000
CMD ["npm", "run", "preview"]
