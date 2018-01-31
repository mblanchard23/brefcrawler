import os
from raven import Client

try:
	logging_uri = os.environ['SENTRY_LOGGING_URI']
	log_client = Client(logging_uri)

except:
	print('SENTRY_LOGGING_URI environment variable required') 


def test_logging():
	try:
		1 / 0
	except ZeroDivisionError:
		log_client.captureException()