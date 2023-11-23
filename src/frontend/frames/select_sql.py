from tkinter import (
    # Frame,
    # Label,
    # Button,
    Misc,
    filedialog,
    # font,
)
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkFont
from backend.configs import CONFIGS


class FRAME_select_sql(CTkFrame):
    def __init__(self, master: Misc | None = None) -> None:
        super().__init__(master)

        title_label = CTkLabel(
            self, text="Arquivos SQL:", font=CTkFont(size=16, weight="bold")
        )
        title_label.pack(anchor="center")

        CTkButton(
            self,
            text="Selecionar arquivos SQL",
            command=self._prompt_for_sql_files,
            height=36,
        ).pack(anchor="center", pady=6)

        self._selected_files_label = CTkLabel(self, text="Nenhum arquivo selecionado")
        self._selected_files_label.pack(anchor="center")

    def _prompt_for_sql_files(self) -> None:
        sql_files = filedialog.askopenfilenames()
        CONFIGS["RUNNING"]["sql_files"] = sql_files
        self._selected_files_label.configure(
            text=f"{len(sql_files)} arquivos selecionados"
        )
