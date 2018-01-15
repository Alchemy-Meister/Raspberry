FROM arm32v7/python:3.6.4
WORKDIR /usr/src/app
COPY ./requirements.txt ./temp/requirements.txt
RUN pip install -r ./temp/requirements.txt
COPY gpio .
COPY profiles .
COPY temp_based_dc_linear_fan_controller.py .
CMD [ "python", "./temp_based_dc_linear_fan_controller.py" ]
