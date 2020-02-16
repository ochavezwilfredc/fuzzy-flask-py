FROM terrillo/python3flask:latest

# rutas ESTÁTICAS para el archivo.
# No use el matraz estático. Nginx es tu amigo
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

# Coloca la aplicación de tu matraz en el servidor
COPY ./app /app
WORKDIR /app

# Instala requerimientos.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# NGINX setup
COPY ./nginx.sh /nginx.sh
RUN chmod +x /nginx.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["/nginx.sh"]
CMD ["/start.sh"]

EXPOSE 80 443
