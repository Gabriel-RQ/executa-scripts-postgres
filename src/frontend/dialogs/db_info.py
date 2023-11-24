from customtkinter import CTkInputDialog, CTkLabel, CTkEntry, CTkButton
from frontend.util import centered


@centered
class DIALOG_database_info(CTkInputDialog):
    def __init__(self):
        self.WIDTH, self.HEIGHT = 320, 350

        super().__init__(
            title="Informações da base de dados",
            text="Informe os dados para conexão com o BD postgres:",
        )

        self._db_host = self._db_password = self._db_admin = None

    def _create_widgets(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        # title label
        CTkLabel(
            master=self,
            width=300,
            wraplength=300,
            fg_color="transparent",
            text_color=self._text_color,
            text=self._text,
            font=self._font,
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # host entry
        CTkLabel(
            master=self,
            width=300,
            wraplength=300,
            fg_color="transparent",
            text_color=self._text_color,
            text="HOST:",
            font=self._font,
        ).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self._db_host_entry = CTkEntry(
            master=self,
            width=230,
            fg_color=self._entry_fg_color,
            border_color=self._entry_border_color,
            text_color=self._entry_text_color,
            font=self._font,
        )
        self._db_host_entry.grid(
            row=2, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="ew"
        )
        self._db_host_entry.insert(0, "localhost")

        # password entry
        CTkLabel(
            master=self,
            width=300,
            wraplength=300,
            fg_color="transparent",
            text_color=self._text_color,
            text="SENHA:",
            font=self._font,
        ).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self._db_password_entry = CTkEntry(
            master=self,
            width=230,
            fg_color=self._entry_fg_color,
            border_color=self._entry_border_color,
            text_color=self._entry_text_color,
            font=self._font,
            show="*",
        )
        self._db_password_entry.grid(
            row=4, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="ew"
        )

        # admin db entry
        CTkLabel(
            master=self,
            width=300,
            wraplength=300,
            fg_color="transparent",
            text_color=self._text_color,
            text="BD ADMINISTRATIVO:",
            font=self._font,
        ).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self._db_admin_entry = CTkEntry(
            master=self,
            width=230,
            fg_color=self._entry_fg_color,
            border_color=self._entry_border_color,
            text_color=self._entry_text_color,
            font=self._font,
        )
        self._db_admin_entry.grid(
            row=6, column=0, columnspan=2, padx=5, pady=(0, 10), sticky="ew"
        )
        self._db_admin_entry.insert(0, "postgres")

        # buttons
        self._ok_button = CTkButton(
            master=self,
            width=100,
            border_width=0,
            fg_color=self._button_fg_color,
            hover_color=self._button_hover_color,
            text_color=self._button_text_color,
            text="Ok",
            font=self._font,
            command=self._ok_event,
        )
        self._ok_button.grid(
            row=7, column=0, columnspan=1, padx=(10, 20), pady=20, sticky="ew"
        )

        self._cancel_button = CTkButton(
            master=self,
            width=100,
            border_width=0,
            fg_color=self._button_fg_color,
            hover_color=self._button_hover_color,
            text_color=self._button_text_color,
            text="Cancel",
            font=self._font,
            command=self._cancel_event,
        )
        self._cancel_button.grid(
            row=7, column=1, columnspan=1, padx=(10, 20), pady=20, sticky="ew"
        )

        self._db_host_entry.after(150, lambda: self._db_host_entry.focus())

    def _ok_event(self, event=None):
        self._db_host = self._db_host_entry.get()
        self._db_password = self._db_password_entry.get()
        self._db_admin = self._db_admin_entry.get()
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._db_host, self._db_password, self._db_admin
