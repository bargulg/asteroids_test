FROM python:3.10-alpine AS build
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --compile -r requirements.txt && rm -rf /root/.cache
COPY src /app

# Build stage test - run tests
FROM build AS test
CMD python3 -m pytest --html=/output/report.html --self-contained-html --verbose
