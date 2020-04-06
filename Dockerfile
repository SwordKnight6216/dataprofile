FROM python:3

LABEL Author="Gordon Chen"
LABEL Email="GordonChen.GoBlue@gmail.com"

RUN useradd -ms /bin/bash dp_user

USER dp_user
COPY --chown=dp_user . /home/dp_user/datareport
ENV PATH="/home/dp_user/.local/bin:${PATH}"

WORKDIR /home/dp_user/datareport
RUN pip install .
RUN rm -r /home/dp_user/datareport/dataprofile
RUN rm -r /home/dp_user/datareport/Dockerfile

USER root
RUN chmod 300 /bin/bash
RUN chmod 300 /bin/sh
USER dp_user

WORKDIR /home/dp_user/data

ENTRYPOINT [ "python", "../datareport/scripts/cli_report.py" ]