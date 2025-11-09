from zoneinfo import ZoneInfo

{% if cookiecutter.use_database == "yes" -%}
from sqlalchemy import URL
{% endif -%}

timezone = ZoneInfo("{{ cookiecutter.timezone }}")

{% if cookiecutter.use_database == "yes" -%}

def build_connection_url(
        driver_name: str,
        username: str,
        password: str,
        host: str,
        port: str | int,
        database: str,
) -> URL:
    return URL.create(
        drivername=driver_name,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )
{% endif -%}
