import os
import json
import pyzipper
import django
import sys
from pathlib import Path

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rdgen.settings')

django.setup()

from django.conf import settings as _settings

pwd = _settings.ZIP_PASSWORD
print('ZIP_PASSWORD_LOADED:', bool(pwd))

os.makedirs(project_root.joinpath('temp_zips'), exist_ok=True)
zip_path = project_root.joinpath('temp_zips', 'secrets_test.zip')
json_path = project_root.joinpath('tmp_test.json')

with open(json_path, 'w') as f:
    json.dump({'foo': 'bar'}, f)

with pyzipper.AESZipFile(str(zip_path), 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
    zf.setpassword(pwd.encode())
    zf.write(str(json_path), arcname='secrets.json')

with pyzipper.AESZipFile(str(zip_path)) as zf:
    zf.setpassword(pwd.encode())
    print('NAMES:', zf.namelist())
    with zf.open('secrets.json') as f:
        print('CONTENT:', f.read())

# cleanup
try:
    os.remove(json_path)
except Exception:
    pass

print('DONE')
