FROM python:3

LABEL Author="Gordon Chen"
LABEL Email="GordonChen.GoBlue@gmail.com"

RUN useradd -ms /bin/bash dp_user

USER dp_user
COPY --chown=dp_user . /home/dp_user/datareport
ENV PATH="/home/dp_user/.local/bin:${PATH}"

WORKDIR /home/dp_user/datareport
RUN pip install .

WORKDIR /home/dp_user/data

CMD [ "python", "../datareport/scripts/cli_report.py" ]