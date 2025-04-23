FROM python:3.11-slim

LABEL Author="Gordon Chen"
LABEL Email="GordonChen.GoBlue@gmail.com"

RUN useradd -ms /bin/bash dp_user

USER dp_user
COPY --chown=dp_user . /home/dp_user/dataprofile
ENV PATH="/home/dp_user/.local/bin:${PATH}"

WORKDIR /home/dp_user
RUN pip install --no-cache-dir ./dataprofile
RUN rm -rf /home/dp_user/dataprofile

WORKDIR /home/dp_user/data

ENTRYPOINT [ "python", "-m", "dataprofile.cli_report" ]
