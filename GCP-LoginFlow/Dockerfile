# Build Angular
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
# Runtime
FROM nginx:alpine
COPY --from=build /app/dist/gcp-login-flow/browser /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
RUN printf 'server {\n\
listen 8080;\n\
server_name _;\n\
root /usr/share/nginx/html;\n\
index index.html;\n\
location / {\n\
try_files $uri $uri/ /index.html;\n\
}\n\
}\n' > /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx","-g","daemon off;"]