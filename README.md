# How to run your own primary

This code has been set-up for and tested on the Heroku platform.
We recommmend you stick to Heroku cause it's awesome.

1. Install postgres, setup DATABASE_URL

2. `pip install -r requirements.txt`

3. Customize primary/fixtures/

4. `python manage.py migrate`

5. `python manage.py loaddata primary/fixtures/regions.yaml`

6. `python manage.py loaddata primary/fixtures/candidates.yaml`

7. Install the summary view via psql, find definition in primary/models.py (`create view..`)

8. `python manage.py run`

9. Find people to vote
