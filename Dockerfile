FROM farrion/python3-ml:latest

LABEL maintainer="Mitesh Patel <mitpatel@redhat.com>"

RUN pip3 install --upgrade pip

RUN pip3 install git+https://github.com/grikbi/infra-adapter#egg=rudra

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

COPY ./recommendation_engine /recommendation_engine
COPY ./entrypoint.sh /bin/entrypoint.sh
RUN chmod 0777 /bin/entrypoint.sh

EXPOSE 6005

ENTRYPOINT ["/bin/bash"]
