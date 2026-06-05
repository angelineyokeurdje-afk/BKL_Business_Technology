import os
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bklbusiness.settings')

from django.conf import settings
from django.core.management import call_command
import django

django.setup()

sqlite_path = Path(os.getcwd()) / 'db.sqlite3'
if not sqlite_path.exists():
    raise FileNotFoundError(f'SQLite file not found: {sqlite_path}')

settings.DATABASES['sqlite'] = settings.DATABASES['default'].copy()
settings.DATABASES['sqlite'].update({
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': str(sqlite_path),
})

dump_file = Path('sqlite_dump.json')
print('Exporting data from SQLite:', sqlite_path)
with dump_file.open('w', encoding='utf-8') as f:
    call_command(
        'dumpdata',
        '--database=sqlite',
        '--natural-foreign',
        '--natural-primary',
        '--indent',
        '2',
        '--exclude=sessions',
        stdout=f,
    )

print('Filtering out django.migrations records from dump')
import json
with dump_file.open('r', encoding='utf-8') as f:
    data = json.load(f)
filtered = [obj for obj in data if obj.get('model') != 'django.migrations']
with dump_file.open('w', encoding='utf-8') as f:
    json.dump(filtered, f, indent=2, ensure_ascii=False)

print('Importing data into PostgreSQL default database')
call_command('loaddata', str(dump_file))
print('Data restore completed.')
