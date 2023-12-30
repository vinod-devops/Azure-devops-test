
from pathlib import Path
from typing import Dict
from src.connectors.constants import DbTypes
from sqlmodel import create_engine
from yaml import safe_load


def read_config(filepath: Path) -> Dict[str, str]:
    try:
        with open(filepath, "r") as file:
            setup_yaml = safe_load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"{filepath} is not a valid DB config filepath, {error}"
        )
    return setup_yaml


class BaseEngine:
    def __init__(self, authentication):
        config = read_config(authentication)
        self.user = config["user"]
        self.passd = config["password"]
        self.host = config["host"]
        self.port = config["port"]
        self.service = config["service"]
        self.encoding = config["encoding"]

    def get_engine(self):
        raise NotImplementedError(f"Engine not implemented")


class OracleEngine(BaseEngine):
    def __init__(self, authentication):
        super().__init__(authentication)

    def get_engine(self):
        return create_engine(
            f"oracle+cx_oracle://{self.user}:{self.passd}@{self.host}:{self.port}/?service_name={self.service}&{self.encoding}"
        )


class EngineFactory:
    _engines = {
        DbTypes.ORACLE: OracleEngine,
    }

    @classmethod
    def from_database_type(cls, db_type: DbTypes):
        if type in cls._engines:
            return cls._engines[db_type]

        raise NotImplementedError(f"Engine type {db_type} not implemented")