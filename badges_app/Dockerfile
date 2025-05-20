FROM ubuntu:18.04

RUN apt update && \
    apt install -y wget bash python3.6-venv python3.6-dev python3-pip build-essential inkscape unzip librsvg2-bin poppler-utils

ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN wget --header 'Host: dl.dafont.com' --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' --header 'Accept-Language: en-US,en;q=0.5' --referer 'https://www.dafont.com/sansation.font' --header 'Upgrade-Insecure-Requests: 1' 'https://dl.dafont.com/dl/?f=sansation' --output-document 'sansation.zip' && \
    unzip sansation.zip -d /usr/local/share/fonts && \
    fc-cache -f -v

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
