import logging
from os import path
from tkinter import (
    messagebox,
    Misc,
    END,
)
from customtkinter import (
    CTkToplevel,
    CTkLabel,
    CTkFont,
    CTkButton,
    CTkFrame,
    CTkTextbox,
)
from backend.configs import CONFIGS
from frontend.util import read_execution_log


class WINDOW_read_database_log(CTkToplevel):
    def __init__(
        self,
        master: Misc | None = None,
    ) -> None:
        super().__init__(master)

        SCRN_WIDTH, SCRN_HEIGHT = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )

        width, height = int(SCRN_WIDTH * 0.75), int(SCRN_HEIGHT * 0.65)

        self.geometry(
            "{}x{}+{}+{}".format(
                width,
                height,
                (SCRN_WIDTH // 2 - width // 2),
                (SCRN_HEIGHT // 2 - height // 2),
            )
        )
        self.resizable(False, False)
        self.title("Ler log")

        title_frame = CTkFrame(self)
        title_frame.pack(anchor="center", fill="both")
        title_label = CTkLabel(
            title_frame,
            text=f"LOG da base de dados {CONFIGS['RUNNING']['selected_database']}",
            font=CTkFont(size=16, weight="bold"),
        )
        title_label.pack(anchor="center", pady=20)

        CTkButton(title_frame, text="Resetar Log", command=self._reset_log).place(
            anchor="center", relx=0.9, rely=0.5
        )

        self._log_text = CTkTextbox(
            self,
            font=CTkFont(size=14),
            spacing1=6,
            spacing2=16,
            spacing3=6,
            bg_color="#27292e",
            text_color="#e6e6e8",
        )
        self._log_text.pack(anchor="center", fill="both", expand=True)

        self._fill_log()

    def _reset_log(self) -> None:
        if messagebox.askyesno("Tem certeza?", "Tudo no arquivo de log será apagado"):
            f = open(
                path.join(
                    CONFIGS["APP"]["log_dir"],
                    "databases",
                    f"{CONFIGS['RUNNING']['selected_database']}.log",
                ),
                "w",
            )
            f.flush()
            f.close()
            self._log_text.configure(state="normal")
            self._log_text.delete(1.0, END)
            self._log_text.configure(state="disabled")

    def _fill_log(self) -> None:
        try:
            self._log_text.insert(
                END, read_execution_log(CONFIGS["RUNNING"]["selected_database"])
            )
            self._log_text.configure(state="disabled")
        except Exception as e:
            logging.error(
                f"Could not read log file for database {CONFIGS['RUNNING']['selected_database']}. Detail: {e}."
            )
            messagebox.showerror(
                "Erro ao ler log",
                f"Ocorreu um erro ao ler o log da base de dados {CONFIGS['RUNNING']['selected_database']}. Detalhe: {e}.",
            )


def create_window(master) -> None:
    if not path.exists(
        path.join(
            CONFIGS["APP"]["log_dir"],
            "databases",
            f"{CONFIGS['RUNNING']['selected_database']}.log",
        )
    ):
        messagebox.showwarning(
            "Nenhum log encontrado",
            f"Nenhum log encontrado para a base de dados {CONFIGS['RUNNING']['selected_database']}",
        )
        return

    WINDOW_read_database_log(master)
