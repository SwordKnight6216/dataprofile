FROM python:3

LABEL Author="Gordon Chen"
LABEL Email="GordonChen.GoBlue@gmail.com"

RUN useradd -ms /bin/bash dp_user

USER dp_user
COPY --chown=dp_user . /home/dp_user/datareport
ENV PATH="/home/dp_user/.local/bin:${PATH}"

WORKDIR /home/dp_user/datareport
RUN pip install .

USER root
RUN chmod 300 /bin/bash
USER dp_user

WORKDIR /home/dp_user/data

ENTRYPOINT [ "python", "../datareport/scripts/cli_report.py" ]