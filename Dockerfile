FROM python:3.6.4-alpine3.7
RUN apk --no-cache add --virtual .fetch-deps \
        gcc \
        linux-headers \
        musl-dev
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
RUN apk del .fetch-deps
WORKDIR /urs/src/app
COPY . .
CMD [ "python", "./temp_based_dc_linear_fan_controller.py" ]