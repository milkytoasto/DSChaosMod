import logging
import tkinter as tk

from gui.styles.colors import DarkColors, LightColors


class WidgetLogger(logging.Handler):
    """
    This implementation is based on the solutions
    provided at this stackoverflow question:

    https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget
    """

    def __init__(self, widget, level=logging.INFO, theme="dark"):
        logging.Handler.__init__(self)
        self.setLevel(level)
        self.setFormatter(
            logging.Formatter("[%(asctime)s]: %(message)s", datefmt="%d-%b-%y %H:%M:%S")
        )
        self.widget = widget
        self.widget.config(state="disabled")
        self.theme = theme
        self._set_colors()
        self._configure_style()

    def toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
        else:
            self.theme = "dark"

        self._set_colors()
        self._configure_style()

    def _set_colors(self):
        if self.theme == "dark":
            self.colors = DarkColors
        else:
            self.colors = LightColors

    def _configure_style(self):
        self.widget.tag_config("INFO", foreground=self.colors.Logging.INFO_TEXT)
        self.widget.tag_config("DEBUG", foreground=self.colors.Logging.DEBUG_TEXT)
        self.widget.tag_config("WARNING", foreground=self.colors.Logging.WARNING_TEXT)
        self.widget.tag_config("ERROR", foreground=self.colors.Logging.ERROR_TEXT)
        self.widget.tag_config(
            "CRITICAL", foreground=self.colors.Logging.CRITICAL_TEXT, underline=1
        )

    def emit(self, record):
        self.widget.config(state="normal")
        # Append message (record) to the widget
        self.widget.insert(tk.END, self.format(record) + "\n", record.levelname)
        self.widget.see(tk.END)  # Scroll to the bottom
        self.widget.config(state="disabled")
        self.widget.update()  # Refresh the widget
