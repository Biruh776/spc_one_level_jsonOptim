FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

CMD [ "python", "./spc_app.py" ]