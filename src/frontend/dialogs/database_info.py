# old version, not in use

import logging
from tkinter import (
    Event,
    Frame,
    Misc,
    simpledialog,
    Label,
    Entry,
    StringVar,
    messagebox,
)
from backend.configs import CONFIGS
from typing import Optional


class DIALOG_database_info(simpledialog.Dialog):
    def __init__(self, parent: Misc | None, title: str | None = None) -> None:
        super().__init__(parent, title)

        self.db_host = None
        self.db_password = None
        self.db_admin = None  # admin database, most always, postgres

    def body(self, master: Frame) -> Misc | None:
        Label(
            master,
            # width=50,
            justify="left",
            wraplength=200,
            text="Parece que é a primeira vez que você utiliza o app. Informe os seguintes campos relacionados ao banco de dados:",
        ).pack(anchor="center")

        Label(master, text="Host").pack(anchor="w")
        default_host_var = StringVar(master, value="localhost")
        self.db_host_entry = Entry(master, width=25, textvariable=default_host_var)
        self.db_host_entry.pack(anchor="center", pady=2, ipady=4)

        Label(master, text="Senha").pack(anchor="w")
        self.db_password_entry = Entry(master, width=25, show="*")
        self.db_password_entry.pack(anchor="center", pady=2, ipady=4)

        Label(master, text="Banco de dados administrativo").pack(anchor="w")
        default_admin_db = StringVar(master, value="postgres")
        self.db_admin_entry = Entry(master, width=25, textvariable=default_admin_db)
        self.db_admin_entry.pack(
            anchor="center",
            pady=2,
            ipady=4,
        )

    def ok(self, event: Optional[Event] = None) -> None:
        try:
            self.db_host = self.db_host_entry.get()
            self.db_password = self.db_password_entry.get()
            self.db_admin = self.db_admin_entry.get()

            # fills the prompted info in the config file
            with open("./CONFIG.ini", "r") as config:
                data = config.readlines()

                for i, line in enumerate(data):
                    raw = line.strip()

                    if raw == "[APP]":
                        data[i + 1] = "first_use=false\n"
                    if raw == "[DATABASE]":
                        data[i + 1] = f"host={self.db_host}\n"
                        data[i + 2] = f"password={self.db_password}\n"
                        data[i + 3] = f"admin_db={self.db_admin}\n"

            with open("./CONFIG.ini", "w") as config:
                config.writelines(data)

            CONFIGS["DATABASE"]["host"] = self.db_host
            CONFIGS["DATABASE"]["password"] = self.db_password
            CONFIGS["DATABASE"]["admin_db"] = self.db_admin
        except Exception as e:
            logging.error(f"Could not save database info. Detail: {e}.")
            messagebox.showerror(
                "Erro ao gravar dados",
                f"Ocorreu um erro ao gravar os dados informados. Detalhe: {e}.",
            )
        finally:
            self.destroy()

    def cancel(self, event: Optional[Event] = None) -> None:
        return super().cancel(event)
