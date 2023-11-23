import logging
import functools

from backend.configs import (
    change_host_config,
    change_password_config,
    change_admin_db_config,
    CONFIGS,
)
from os import path, makedirs
from datetime import datetime
from tkinter import (
    # simpledialog,
    messagebox,
)
from customtkinter import CTkInputDialog
from typing import Literal


def change_config(config: Literal["host", "password", "adm_db"]) -> None:
    try:
        dialog = CTkInputDialog(text="Informe o novo valor:", title="Novo valor")
        dialog_width, dialog_height = dialog.winfo_width(), dialog.winfo_height()
        dialog.geometry(
            "{}x{}+{}+{}".format(
                dialog_width,
                dialog_height,
                (dialog.winfo_screenwidth() // 2 - dialog_width // 2),
                (dialog.winfo_screenheight() // 2 - dialog_height // 2),
            )
        )
        # v = simpledialog.askstring("Novo valor", prompt="Informe o novo valor:")
        v = dialog.get_input()

        if v is None:
            return

        match config:
            case "host":
                change_host_config(v)
            case "password":
                change_password_config(v)
            case "adm_db":
                change_admin_db_config(v)

    except Exception as e:
        logging.error(f"Could not change configuration {config}. Detail: {e}.")
        messagebox.showerror(
            "Erro ao mudar configuração",
            f"Ocorreu um erro ao mudar o arquivo de configurações. Detalhe: {e}.",
        )
    else:
        messagebox.showinfo(
            "Configuração alterada",
            "A configuração foi alterada com sucesso, reinicie o programa para que as mudanças sejam aplicadas.",
        )


def save_execution_log(file_name: str, log: str) -> None:
    if not path.exists(path.join(CONFIGS["APP"]["log_dir"], "databases")):
        makedirs(path.join(f"{CONFIGS['APP']['log_dir']}", "databases"))

    with open(f"{CONFIGS['APP']['log_dir']}/databases/{file_name}.log", "a") as f:
        f.write(f"[{datetime.now()}] {log}\n")


def read_execution_log(file_name: str) -> str:
    with open(
        path.join(CONFIGS["APP"]["log_dir"], "databases", f"{file_name}.log"), "r"
    ) as f:
        return f.read()


def read_app_log() -> str:
    with open(path.join(CONFIGS["APP"]["log_dir"], "app.log"), "r") as f:
        return f.read()


def centered(cls):
    """Centers a TKinter window on the screen. `cls` should have WIDTH and HEIGHT atributes, which can be None."""

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        wrapper = cls(*args, **kwargs)
        SCRN_WIDTH, SCRN_HEIGHT = (
            wrapper.winfo_screenwidth(),
            wrapper.winfo_screenheight(),
        )
        if not wrapper.WIDTH:
            WIDTH = wrapper.winfo_width()
        else:
            WIDTH = wrapper.WIDTH
        if not wrapper.HEIGHT:
            HEIGHT = wrapper.winfo_height()
        else:
            HEIGHT = wrapper.HEIGHT

        wrapper.geometry(
            "{}x{}+{}+{}".format(
                WIDTH,
                HEIGHT,
                (SCRN_WIDTH // 2 - WIDTH // 2),
                (SCRN_HEIGHT // 2 - HEIGHT // 2),
            )
        )
        return wrapper

    return wrapper
