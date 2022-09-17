import logging
import websockets
import asyncio
from async_tkinter_loop import async_handler, async_mainloop
import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.ttk as ttk
import configparser
from utils.TwitchBot import TwitchBot

config = configparser.ConfigParser()
config.read("config.ini")

BOT = False
RUNNING = False
PORT = config["WEBSOCKET"]["PORT"]
VOTING_ENABLED = config["VOTING"].getboolean("INITIAL_STATE")
VOTING_ENABLED_PERIOD = config["VOTING"].getint("VOTING_PERIOD")
VOTING_DISABLED_PERIOD = config["VOTING"].getint("VOTING_INTERVAL")
VOTING_PERIOD = VOTING_ENABLED_PERIOD if VOTING_ENABLED else VOTING_DISABLED_PERIOD
COUNTDOWN = VOTING_PERIOD
TOKEN = config["TWITCH"]["TMI_TOKEN"]
CHANNEL = config["TWITCH"]["CHANNEL"]
CLIENTS = set()

async def handler(websocket, path):
    debug_logger = logging.getLogger("debug")
    debug_logger.info(f"Websocket Handler: Client just connected.")
    CLIENTS.add(websocket)

    try:
        async for message in websocket:
            debug_logger.info(
                f"Websocket Handler: Received message from client: {message} {path}"
            )
            for connection in CLIENTS:
                if connection != websocket:
                    await connection.send(f"Websocket Handler: Someone said: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        debug_logger.info(f"Websocket Handler: A client has lost connection.")
    finally:
        CLIENTS.remove(websocket)


async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass


def broadcast(message):
    for websocket in CLIENTS:
        asyncio.create_task(send(websocket, message))


async def voting_controller():
    global VOTING_ENABLED, VOTING_PERIOD, COUNTDOWN

    while RUNNING:
        broadcast(f"{VOTING_ENABLED} Time remaining {COUNTDOWN}")
        await asyncio.sleep(1)
        if COUNTDOWN == 0:
            VOTING_ENABLED = ~VOTING_ENABLED
            VOTING_PERIOD = (
                VOTING_ENABLED_PERIOD if VOTING_ENABLED else VOTING_DISABLED_PERIOD
            )
            COUNTDOWN = VOTING_PERIOD
        COUNTDOWN -= 1


def stop():
    global RUNNING
    RUNNING = False


async def start():
    global RUNNING
    debug_logger = logging.getLogger("debug")
    chat_logger = logging.getLogger("chat")

    if RUNNING:
        debug_logger.error("Already running, dumbass.")
        return

    RUNNING = True

    bot = TwitchBot(
        token=TOKEN,
        channel=CHANNEL,
        debug_logger=debug_logger,
        chat_logger=chat_logger,
        messageHandler=broadcast,
    )

    loop = asyncio.get_event_loop()
    twitch_task = loop.create_task(bot.start())
    voting_task = loop.create_task(voting_controller())

    tasks = [twitch_task, voting_task]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for p in pending:
        debug_logger.info(f"{len(done)} tasks exited. Cancelling {len(pending)} tasks ")
        p.cancel()


async def websocket_server():
    logger = logging.getLogger("debug")
    logger.info(f"Websocket Server: Listening on port {PORT}")
    await websockets.serve(handler, "localhost", PORT)


class WidgetLogger(logging.Handler):
    """
    This implementation is based on:
    https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget
    """

    def __init__(self, widget, level=logging.INFO):
        logging.Handler.__init__(self)
        self.setLevel(level)
        self.setFormatter(
            logging.Formatter("[%(asctime)s]: %(message)s", datefmt="%d-%b-%y %H:%M:%S")
        )
        self.widget = widget
        self.widget.config(state="disabled")
        self.widget.tag_config("INFO", foreground="black")
        self.widget.tag_config("DEBUG", foreground="black", background="grey")
        self.widget.tag_config("WARNING", foreground="orange")
        self.widget.tag_config("ERROR", foreground="red")
        self.widget.tag_config("CRITICAL", foreground="red", underline=1)
        self.red = self.widget.tag_configure("red", foreground="red")

    def emit(self, record):
        self.widget.config(state="normal")
        # Append message (record) to the widget
        self.widget.insert(tk.END, self.format(record) + "\n", record.levelname)
        self.widget.see(tk.END)  # Scroll to the bottom
        self.widget.config(state="disabled")
        self.widget.update()  # Refresh the widget


class ServerGUI:
    def __init__(self, title):
        root = tk.Tk()
        root.title(title)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        width = 600
        height = 350
        
        root.geometry(f'{width}x{height}')
        root.minsize(width, height)

        self.root = root

        self.__initFrames()
        self.__initButtons()
        self.__initTabs()
        self.__initLoggingTab(self.debug_tab, "debug")
        self.__initLoggingTab(self.chat_tab, "chat")

    def __ws_button_press(self):
        self.wsButton["state"] = "disabled"

    def __initFrames(self):
        self.top_frame = tk.Frame(self.root, width=450, height=50, pady=8, padx=8)
        self.top_frame.grid(row=0, sticky=tk.W)

        self.bottom_frame = tk.Frame(self.root, pady=8, padx=8)
        self.bottom_frame.grid(row=1, sticky=tk.E+tk.W+tk.N+tk.S)

    def __initButtons(self):
        self.wsButton = ttk.Button(
            self.top_frame,
            text="Initiate Websocket Server",
            command=lambda: [
                self.__ws_button_press(),
                async_handler(websocket_server)(),
            ],
        )
        self.wsButton.grid(row=0, column=0)
        self.twButton = ttk.Button(
            self.top_frame, text="Connect to Twitch", command=async_handler(start)
        ).grid(row=0, column=1, padx=8)
        self.stButton = ttk.Button(self.top_frame, text="Stop", command=stop).grid(
            row=0, column=2
        )

    def __initTabs(self):
        self.tabControl = ttk.Notebook(self.bottom_frame)
        self.debug_tab = ttk.Frame(self.tabControl)
        self.chat_tab = ttk.Frame(self.tabControl)
        self.settings_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.debug_tab, text="Debugging")
        self.tabControl.add(self.chat_tab, text="Chat")
        self.tabControl.add(self.settings_tab, text="Settings")
        self.tabControl.pack(expand=1, fill="both")

    def __initLoggingTab(self, tab, name=""):
        # Logging configuration
        logging.basicConfig(
            format="[%(asctime)s]: %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.INFO,
        )

        text = st.ScrolledText(tab, height=15)
        text.configure(state="disabled")
        text.pack(fill="both", expand="true")

        logger = logging.getLogger(name)
        text_handler = WidgetLogger(text)
        logger.addHandler(text_handler)


if __name__ == "__main__":
    gui = ServerGUI("Dark Souls Chaos Server")
    async_mainloop(gui.root)
