# Stage 1 - Build Angular
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
# Stage 2 - Nginx
FROM nginx:alpine
COPY --from=build /app/dist/gcp-login-flow/browser /usr/share/nginx/html
RUN sed -i 's/listen 80;/listen 8080;/g' /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]