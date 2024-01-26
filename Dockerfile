FROM python:3

COPY . .
RUN pip install bs4
RUN pip install requests
RUN pip install flask
CMD ["python3","run.py"]