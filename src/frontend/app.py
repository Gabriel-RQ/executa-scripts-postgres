import logging

from tkinter import Menu, messagebox
from customtkinter import CTk, CTkLabel

from frontend.dialogs.db_info import DIALOG_database_info
from frontend.frames.select_database import FRAME_select_database
from frontend.frames.exec_sql import FRAME_exec_sql
from frontend.frames.select_sql import FRAME_select_sql
from frontend.windows import read_database_log
from frontend.windows import read_app_log
from frontend.util import change_config, centered
from backend.configs import CONFIGS


@centered
class App(CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Executa Scripts")
        self.resizable(False, False)

        self.WIDTH, self.HEIGHT = 400, 550

        # if first time running the app, ask for database information
        if CONFIGS["APP"]["first_use"] == "true":
            try:
                db_info_dialog = DIALOG_database_info()
                db_host, db_password, db_admin = db_info_dialog.get_input()
                CONFIGS["DATABASE"]["host"] = db_host
                CONFIGS["DATABASE"]["password"] = db_password
                CONFIGS["DATABASE"]["admin_db"] = db_admin

                if not (db_host and db_password and db_admin):
                    raise TypeError("Dados de conexão não informados!")

                # fills the prompted info in the config file
                with open("./CONFIG.ini", "r") as config:
                    data = config.readlines()

                    for i, line in enumerate(data):
                        raw = line.strip()

                        if raw == "[APP]":
                            data[i + 1] = "first_use=false\n"
                        if raw == "[DATABASE]":
                            data[i + 1] = f"host={db_host}\n"
                            data[i + 2] = f"password={db_password}\n"
                            data[i + 3] = f"admin_db={db_admin}\n"

                with open("./CONFIG.ini", "w") as config:
                    config.writelines(data)
            except Exception as e:
                logging.error(
                    f"Error saving database configuration on CONFIG file. Detail: {e}"
                )
                messagebox.showwarning(
                    "Erro ao salvar configurações",
                    f"Ocorreu um erro ao salvar as configurações. Detalhe: {e}.",
                )

        # set up the menubar
        menubar = Menu(self)
        self.config(menu=menubar)

        options_submenu = Menu(menubar, tearoff=False)
        options_submenu.add_command(
            label="Mudar configuração de HOST", command=lambda: change_config("host")
        )
        options_submenu.add_command(
            label="Mudar configuração de SENHA DO BD",
            command=lambda: change_config("password"),
        )
        options_submenu.add_command(
            label="Mudar configuração de BD ADMINISTRATIVO",
            command=lambda: change_config("adm_db"),
        )
        options_submenu.add_command(
            label="Ler log para base de dados selecionada",
            command=lambda: read_database_log.create_window(self),
        )
        options_submenu.add_command(
            label="Ler log da aplicação",
            command=lambda: read_app_log.create_window(self),
        )

        menubar.add_cascade(label="Opções", menu=options_submenu)
        menubar.add_separator()
        menubar.add_command(label="Sair", command=self.destroy)

        # title
        CTkLabel(self, text="EXECUTA SCRIPTS", font=("Helvetica", 24, "bold")).pack(
            anchor="center", pady=16
        )

        # frames
        FRAME_select_database(self).pack(anchor="center", ipady=12, ipadx=16)
        FRAME_select_sql(self).pack(anchor="center", pady=12, ipady=12, ipadx=16)
        FRAME_exec_sql(self).pack(anchor="center", pady=12, ipady=12, ipadx=16)

    def run(self) -> None:
        self.mainloop()
