FROM node:22-alpine AS build

WORKDIR /src

RUN npm install -g html-minifier-terser

COPY index.html .
RUN mkdir /out && html-minifier-terser --collapse-whitespace --minify-css true --minify-js true -o /out/index.html index.html

FROM nginxinc/nginx-unprivileged:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /out/index.html /usr/share/nginx/html/index.html

EXPOSE 8080