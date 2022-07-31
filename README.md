# Martailer

Fetching videos for a certain channel of a youtube channel

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/ejaj/martailer-task.git
$ cd martailer-task
```

Then, active a virtual environment:

```sh
$ source venv/bin/activate
```

Create an .env file and paste all the variables from .env.keep file and set the value for them for example database
name, password, host etc.

### Run the project on localhost.

Then run these command. Create a log directory

```sh
mkdir log
```

Make sure log folder has write permission

For migrations

```sh
python manage.py migrate
```

For fetching youtube videos

```sh
python manage.py videofetching
```

For running project.

```sh
python manage.py runserver
```

Now you can browse: http://127.0.0.1:8000/admin

For api's operation, you can see
[ api documentation doc](API documentation.pdf)

### Cron job

Run these commands

For adding cron job

```sh
python manage.py crontab add
```

For showing cron job

```sh
python manage.py crontab show
```

For removing cron job

```sh
python manage.py crontab remove
```

Generally, Celery and Redis/Rabbitmq are best for any periodically or background task of application. In this project, I
have use a small python library for periodically task which is run by django application itself.

### Dependencies

```sh
- Database: MySQL
```

You can see the all kinds of log from project log folder.

### If you face any problems with MySQL database, while inserting emoji.

Please follow these commands

```sh
mysql -u root -p
ALTER DATABASE database_name CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
use database_name;
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE table_name MODIFY field_name VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

NB: 3 number option, 2nd option (b) can't fully understand. Therefore, it did not complete.
