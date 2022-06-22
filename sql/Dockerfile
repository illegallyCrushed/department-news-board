FROM news-board-base

RUN mkdir /backups

RUN apt-get update -y && apt-get install cron -y && apt-get install -y mariadb-client -y

COPY cron-backup /etc/cron.d/cron-backup
COPY cron_script.py /cron_script.py

RUN chmod 0644 /etc/cron.d/cron-backup
RUN chmod 0744 /cron_script.py

RUN crontab /etc/cron.d/cron-backup
RUN touch /backups/log.txt

CMD cron && tail -f /backups/log.txt