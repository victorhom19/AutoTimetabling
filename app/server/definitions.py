import os

import dotenv

dotenv.load_dotenv()

ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER_ROOT = os.path.join(ROOT, 'server/main')

api_origin = os.environ['ATIMETABLE_API_ORIGIN']
frontend_origin = os.environ['ATIMETABLE_FRONTEND_ORIGIN']

db_user = os.environ['ATIMETABLE_DATABASE_USER']
db_password = os.environ['ATIMETABLE_DATABASE_PASSWORD']
db_url = os.environ['ATIMETABLE_DATABASE_URL']
db_name = os.environ['ATIMETABLE_DATABASE_NAME']