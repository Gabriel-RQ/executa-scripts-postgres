import atexit
import logging
from tkinter import (
    messagebox,
    Misc,
)

from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkFont,
    CTkOptionMenu,
    StringVar,
)
from backend.configs import CONFIGS
from backend.db import get_all_database_names, Postgres


class FRAME_select_database(CTkFrame):
    def __init__(self, master: Misc | None = None) -> None:
        super().__init__(master)

        # connect to admin database
        self._admin_conn = Postgres(
            database=CONFIGS["DATABASE"]["admin_db"],
            password=CONFIGS["DATABASE"]["password"],
            host=CONFIGS["DATABASE"]["host"],
        )

        try:
            self._admin_conn.connect()
        except Exception as e:
            logging.critical(
                f"Could not connect to administrative database. Detail: {e}."
            )
            messagebox.showerror(
                "Erro ao conectar BD administrativo",
                f"Não foi possível estabelecer conexão com a base de dados administrativa, verifique os dados. Detalhe: {e}",
            )
        else:
            logging.info("Connected to administrative database")
            atexit.register(self._admin_conn.close)

        wrapper_frame = CTkFrame(self)
        wrapper_frame.pack(anchor="center", expand=True, ipadx=8, ipady=8)
        # display
        CTkLabel(
            wrapper_frame, text="Selecione a base de dados:", font=CTkFont(size=16)
        ).pack(anchor="center")

        host_info_label = CTkLabel(
            wrapper_frame,
            text=f"[HOST DA BASE DE DADOS: {CONFIGS['DATABASE']['host']}]",
        )
        host_info_label.pack(anchor="center", pady=4)
        host_info_label.cget("font").configure(size=12, weight="bold")

        # combo frame
        combo_frame = CTkFrame(wrapper_frame)
        combo_frame.pack(anchor="center")

        self._selected_db_var = StringVar(combo_frame)
        self._db_combo = CTkOptionMenu(
            combo_frame,
            variable=self._selected_db_var,
            width=240,
            command=lambda _: self._set_selected_database(),
        )
        self._update_combo_values()
        self._db_combo.pack(anchor="center", side="top", pady=2, ipady=6)

    def _set_selected_database(self) -> None:
        CONFIGS["RUNNING"]["selected_database"] = self._selected_db_var.get()

    def _update_combo_values(self) -> None:
        databases = sorted(get_all_database_names(self._admin_conn))

        if len(databases) == 0:
            messagebox.showwarning(
                "Atenção!",
                "Houve um problema ao buscar pelas bases de dados na conexão informada, verifique os dados de configuração e tente novamente.",
            )
            databases.append("Nenhuma base de dados encontrada!")
            self._db_combo.configure(state="disabled")
        else:
            self._db_combo.configure(values=databases)

        self._selected_db_var.set(databases[0])
