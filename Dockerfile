FROM python:3.8-slim

# Set up python dependencies
COPY requirements.txt /
RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt

# Set up project files.
COPY app /instance/app
COPY base /instance/base
COPY scripts /instance/scripts
RUN  mkdir /instance/storage
RUN  chmod a+x "/instance/scripts/run_bot.sh"
CMD  ["/instance/scripts/run_bot.sh"]
