from pydantic import BaseModel

{% if cookiecutter.use_database == "yes" -%}

class Status(BaseModel):
    database: bool | None = None
{% endif -%}


class HealthResponse(BaseModel):
    name: str
    version: str
{% if cookiecutter.use_database == "yes" -%}
    status: Status
{% endif -%}
