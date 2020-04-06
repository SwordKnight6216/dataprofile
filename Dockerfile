FROM python:3

LABEL Author="Gordon Chen"
LABEL Email="GordonChen.GoBlue@gmail.com"

RUN useradd -ms /bin/bash dp_user

USER dp_user
COPY --chown=dp_user . /home/dp_user/dataprofile
ENV PATH="/home/dp_user/.local/bin:${PATH}"

WORKDIR /home/dp_user/dataprofile
RUN pip install .
RUN rm -r /home/dp_user/dataprofile/dataprofile
RUN mv /home/dp_user/dataprofile/scripts/cli_report.py /home/dp_user/dataprofile/
RUN rm -r /home/dp_user/dataprofile/scripts
RUN rm -r /home/dp_user/dataprofile/Dockerfile

USER root
RUN chmod 300 /bin/bash
RUN chmod 300 /bin/sh
RUN chmod 311 /home/dp_user/dataprofile
RUN chmod 311 /home/dp_user/.local
USER dp_user

WORKDIR /home/dp_user/data

ENTRYPOINT [ "python", "../dataprofile/cli_report.py" ]