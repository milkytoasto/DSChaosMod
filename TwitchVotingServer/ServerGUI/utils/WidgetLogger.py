import logging
import tkinter as tk


class WidgetLogger(logging.Handler):
    """
    This implementation is based on the solutions
    provided at this stackoverflow question:

    https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget
    """

    def __init__(self, widget, level=logging.INFO):
        logging.Handler.__init__(self)
        self.setLevel(level)
        self.setFormatter(
            logging.Formatter(
                "[%(asctime)s] %(levelname)s %(module)s - %(funcName)s: %(message)s",
                datefmt="%d-%b-%y %H:%M:%S",
            )
        )
        self.widget = widget
        self.widget.config(state="disabled")
        self.widget.tag_config("INFO", foreground="white")
        self.widget.tag_config("DEBUG", foreground="white", background="grey")
        self.widget.tag_config("WARNING", foreground="orange")
        self.widget.tag_config("ERROR", foreground="red")
        self.widget.tag_config("CRITICAL", foreground="red", underline=1)
        self.red = self.widget.tag_configure("red", foreground="red")

    def emit(self, record):
        self.widget.config(state="normal")
        # Append message (record) to the widget
        self.widget.insert(
            tk.END,
            self.format(record) + "\n",
            record.levelname,
        )
        self.widget.see(tk.END)  # Scroll to the bottom
        self.widget.config(state="disabled")
        self.widget.update()  # Refresh the widget
