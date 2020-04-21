FROM python:3.7

RUN mkdir /root/.config

COPY . .

RUN python setup.py install

ENTRYPOINT [ "ricksay", "kek" ]
