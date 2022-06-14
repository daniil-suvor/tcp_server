FROM python:3.9
RUN pip install --upgrade pip && pip install sockets
COPY . .
EXPOSE 51413
CMD ["python3", "tcp_server.py"]
