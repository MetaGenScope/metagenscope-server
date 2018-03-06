"""Environment configurations."""

# pylint: disable=invalid-name

import os

# Base configuration
config = {
    'broker_url': os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
    'result_backend': os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379'),
    'result_expires': 3600,     # Expire results after one hour
    'result_cache_max': None,   # Do not limit cache
}

# Configuration for Development
development_config = dict(config)

# Configuration for Testing, with a separate test database.
testing_config = dict(config)
testing_config['broker_url'] = os.environ.get('CELERY_BROKER_TEST_URL')
testing_config['result_backend'] = os.environ.get('CELERY_RESULT_TEST_BACKEND')

# Configuration for Staging
staging_config = dict(config)

# Configurations for Production
production_config = dict(config)
# Set these explicitly just to be extra safe
production_config['broker_url'] = os.environ.get('CELERY_BROKER_URL')
production_config['result_backend'] = os.environ.get('CELERY_RESULT_BACKEND')

# pylint: disable=invalid-name
app_config = {
    'development': development_config,
    'testing': testing_config,
    'staging': staging_config,
    'production': production_config,
}
