# iWater Web app

Initiative Water Web Interface.

## Quick Start

### Install Python (version recommended: 3.8)

### Install MySQL

### Install Dependency
```shell
pip3 install -r  requirements.txt
```

### Configure
```shell
cd init_water_app
touch .env
```

Values specific to your environment
```ini
SECRET_KEY=
DEBUG=

DATABASE_NAME=iwater
DATABASE_USER=
DATABASE_PASS=
DATABASE_HOST=
DATABASE_PORT=

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=587

BRAND_NAME=Initiative Water
SUPPORT_EMAIL=
SUPPORT_PHONE=
```

## Migrate db

```bash
python3 manage.py makemigrations iwater
python3 manage.py migrate
```

## Run development server

```bash
python3 manage.py runserver <ip>:<port>
```