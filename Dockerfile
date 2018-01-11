FROM arm64v8/python:3.7.0a4-alpine3.7
WORKDIR /usr/src/app
COPY 
COPY pigpio.py /usr/lib/python3.7/site-packages/pigpio.py
CMD [ "python", "./temp_based_dc_linear_fan_controller.py" ]