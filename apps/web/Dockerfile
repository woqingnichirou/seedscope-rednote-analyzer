FROM node:20-alpine

WORKDIR /app

COPY apps/web/package.json ./apps/web/package.json
COPY package.json ./package.json
RUN npm --prefix apps/web install

COPY apps/web ./apps/web

WORKDIR /app/apps/web
EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]
