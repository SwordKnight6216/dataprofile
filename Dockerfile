FROM python:3.7-slim

LABEL Author="Gordon Chen"
LABEL Email="GordonChen.GoBlue@gmail.com"

RUN useradd -ms /bin/bash dp_user

USER dp_user
COPY --chown=dp_user . /home/dp_user/dataprofile
ENV PATH="/home/dp_user/.local/bin:${PATH}"

WORKDIR /home/dp_user
RUN pip install ./dataprofile
RUN rm -rf /home/dp_user/dataprofile

USER root
RUN chmod 300 /bin
USER dp_user

WORKDIR /home/dp_user/data

ENTRYPOINT [ "python", "-m", "dataprofile.cli_report" ]