FROM python:3.9 as chrome-stage

RUN apt update && \
    apt install -y unzip wget && \
    wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"

FROM python:3.9

COPY --from=chrome-stage google-chrome-stable_current_amd64.deb /

RUN apt update && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY src . 

COPY src/modules .

ENTRYPOINT ["python",  "main.py"]