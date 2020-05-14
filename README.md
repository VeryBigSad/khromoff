# khrmff.ru
My site, live <a href="https://khrmff.ru">here</a> (russian language alert).

If you want to run this on your machine, then type this in terminal:

```
git clone https://github.com/mikhailkhromov/khromoff
cd khromoff
pip install -r requirments.txt
python manage.py makemigrations && python manage.py migrate
```
Then, specify DEBUG mode in khromoff/settings.py, and create 
`secrets.py` with database connection data, logging Telegram bot token
(`bot_token` var) and list people who need to get notifications on
http500 errors and when someone sends a bugreport (`STAFF_TELEGRAM_IDS` var)

And, finally, `python manage.py manage.py runserver`. Will be there on localhost:8080.

If you find any bugs, please open an Issue.

