FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pymysql -i https://mirror-pypi.runflare.com/simple/ --trusted-host mirror-pypi.runflare.com

COPY main.py .

CMD ["python", "-u", "main.py"]
