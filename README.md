# Causas

Web scraper for causes files.

Run redis:

`$ redis-server`

To run celery worker:

`$ celery -A causas worker -l info`

To run celery beat:

`$ celery -A causas beat -l info`

To test the scraper manually:

`$ python3 manage.py run_scraper`

