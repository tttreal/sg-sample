FROM nginx:1.27-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY conf/* /etc/nginx/conf.d/
#COPY conf/include /etc/nginx/conf.d/
#COPY conf/include/* /etc/nginx/conf.d/include/
