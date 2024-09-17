import logging

from template_project.api.factories import create_api_application

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = create_api_application()
