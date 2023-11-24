#!/usr/bin/env python

import logging
from tkinter import messagebox
from os import path, mkdir
from frontend.app import App
from backend.configs import create_config_file, read_configs, CONFIGS

if __name__ == "__main__":
    # read configuration file
    try:
        if not path.exists(path.abspath("./CONFIG.ini")):
            create_config_file()

        read_configs()
    except Exception as e:
        messagebox.showerror(
            "Erro ao ler configurações",
            f"Houve um erro ao ler o arquivo de configurações. Detalhe: {e}",
        )
        exit(1)

    # set up logging
    if not path.exists(CONFIGS["APP"]["log_dir"]):
        mkdir(path.abspath(CONFIGS["APP"]["log_dir"]))

    logging.basicConfig(
        filename=path.join(path.abspath(CONFIGS["APP"]["log_dir"]), "app.log"),
        format="[%(asctime)s]:%(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    logging.info(f"Application initialized")

    app = App()
    app.run()
    logging.info("Apllication terminated")
