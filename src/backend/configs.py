import shutil
from os import path

CONFIGS = {}


def read_configs(cfg_path: str = ".") -> None:
    with open(f"{cfg_path}\CONFIG.ini", "r") as cfg_f:
        section = None
        for line in cfg_f:
            # insert empty entries for each section
            if section not in CONFIGS.keys() and section is not None:
                CONFIGS[section] = {}

            # ignore blank lines and comments
            if len((s := line.strip())) < 1 or s.startswith("#"):
                continue

            raw = line.strip().strip("[]")
            data = raw.split("=")

            if line.startswith("[") and line.strip().endswith("]"):
                section = raw
                continue

            if len(data) > 0:
                CONFIGS[section][data[0]] = data[1]


def create_config_file(cfg_path: str = ".") -> None:
    open(path.join(cfg_path, "CONFIG.ini"), "w").close()  # creates the config file
    shutil.copy(
        src=path.join(cfg_path, "CONFIG.ini.example"),
        dst=path.join(cfg_path, "CONFIG.ini"),
    )


def _change_config(new_value: str, section: str, option_name: str, offset: int) -> None:
    with open(".\CONFIG.ini", "r") as config:
        data = config.readlines()

        for i, line in enumerate(data):
            raw = line.strip()

            if raw == section:
                data[i + offset] = f"{option_name}={new_value}\n"

    with open(".\CONFIG.ini", "w") as config:
        config.writelines(data)


def change_host_config(host: str) -> None:
    _change_config(host, section="[DATABASE]", option_name="host", offset=1)


def change_password_config(password: str) -> None:
    _change_config(password, section="[DATABASE]", option_name="password", offset=2)


def change_admin_db_config(admin_db: str) -> None:
    _change_config(admin_db, section="[DATABASE]", option_name="admin_db", offset=3)
