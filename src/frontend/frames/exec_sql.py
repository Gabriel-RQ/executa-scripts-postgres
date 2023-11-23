import logging, threading
from tkinter import (
    # Frame,
    # Button,
    # Label,
    Misc,
    messagebox,
)
from customtkinter import CTkFrame, CTkButton, CTkLabel
from frontend.util import save_execution_log
from backend.db import Postgres
from backend.configs import CONFIGS


class FRAME_exec_sql(CTkFrame):
    def __init__(self, master: Misc | None = None) -> None:
        super().__init__(master)

        CTkButton(
            self,
            text="Executar",
            command=self._exec_sql,
            width=124,
            height=52,
        ).pack(anchor="center", expand=True, pady=12)

        self._scripts_executed_success_label = CTkLabel(
            self, text=f"Arquivos executados com sucesso: 0"
        )
        self._scripts_executed_label = CTkLabel(self, text=f"Arquivos executados: 0")

        self._scripts_executed_success_label.pack(anchor="center", expand=True)
        self._scripts_executed_label.pack(anchor="center", expand=True)

    def _exec_sql(self) -> None:
        if threading.active_count() > 1:
            messagebox.showwarning(
                "Aguarde",
                "Espere até que a execução dos arquivos SQL já selecionados termine.",
            )
            return

        t = ExecSQLThread()
        t.setDaemon(True)
        t.set_label_config_callback(
            callback_executed=lambda n: self._scripts_executed_label.configure(
                text=f"Arquivos executados: {n}"
            ),
            callback_successfull=lambda n: self._scripts_executed_success_label.configure(
                text=f"Arquivos executados com sucesso: {n}"
            ),
        )
        t.start()

        logging.info(
            f"Starting thread to execute SQL files in the background. Active threads: {threading.active_count()}"
        )


class ExecSQLThread(threading.Thread):
    def set_label_config_callback(
        self, callback_executed, callback_successfull
    ) -> None:
        self.config_label_executed = callback_executed
        self.config_label_successfull = callback_successfull

    def _exec_sql(self) -> None:
        db_conn = Postgres(
            database=CONFIGS["RUNNING"]["selected_database"],
            password=CONFIGS["DATABASE"]["password"],
            host=CONFIGS["DATABASE"]["host"],
        )

        db_conn.connect()
        db_conn.transaction()

        n = 0

        for executed, sql in enumerate(CONFIGS["RUNNING"]["sql_files"]):
            try:
                with open(sql, "r", encoding="utf-8-sig") as f:
                    db_conn.query(f.read())
            except Exception as e:
                db_conn.rollback()
                save_execution_log(
                    CONFIGS["RUNNING"]["selected_database"],
                    f"SQL {sql} ERROR : {e}",
                )
            else:
                n += 1
                self.config_label_successfull(n)
                db_conn.commit()
                save_execution_log(
                    CONFIGS["RUNNING"]["selected_database"], f"SQL {sql} OK"
                )

            self.config_label_executed(executed + 1)

        save_execution_log(
            CONFIGS["RUNNING"]["selected_database"],
            f"INFO : Succesfully executed {n} SQL files from {len(CONFIGS['RUNNING']['sql_files'])} selected",
        )
        db_conn.close()

    def run(self) -> None:
        try:
            self._exec_sql()
        except Exception as e:
            logging.error(
                f"Exception running thread. Could not execute the SQL files. Detail: {e}."
            )
            messagebox.showerror(
                "Erro ao executar SQL",
                f"Ocorreu um erro ao executar os arquivos SQL. Detalhe: {e}.",
            )
        else:
            messagebox.showinfo(
                "Sucesso!", "A execução dos arquivos finalizou com sucesso."
            )
