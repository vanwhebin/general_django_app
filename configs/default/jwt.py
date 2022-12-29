import os
from datetime import timedelta
from .common import BASE_DIR


APPEND_SLASH = True
RUNTIME_DIR = os.path.join(BASE_DIR, 'runtime')
BASE_LOG_DIR = os.path.join(RUNTIME_DIR, "log")

REST_FRAMEWORK = {
	# Use Django's standard `django.contrib.auth` permissions,
	# or allow read-only access for unauthenticated users.
	'DEFAULT_PERMISSION_CLASSES': [
		# 'rest_framework.permissions.IsAuthenticated',
		# 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
		# 'rest_framework.permissions.Is',
		'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	],
	'DEFAULT_AUTHENTICATION_CLASSES': [
		# 'rest_framework.authentication.TokenAuthentication',
		'rest_framework_simplejwt.authentication.JWTAuthentication',
		'rest_framework.authentication.SessionAuthentication',
	],
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
		'rest_framework.renderers.BrowsableAPIRenderer',
		# 'rest_framework_csv.renderers.CSVRenderer',
	),

}

SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
	'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
	'SIGNING_KEY': '4ZSsKxb$NWV&V1rd*KS6yJROOh!!!HB3&W!jUTyBc9iOLptwzW*g^3GG*ZDdtJT1',
	'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
	'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}