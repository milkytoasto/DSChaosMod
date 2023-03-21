import os
import tkinter as tk
import tkinter.ttk as ttk

import toml


class EffectsTab(ttk.Frame):
    def __init__(self, master=None, config_path="", save_handler=None, **kwargs):
        super().__init__(master, **kwargs)
        self._config_path = config_path

        self.master_config_file = os.path.join(
            os.path.dirname(config_path), "config.toml"
        )
        self.master_config = toml.load(self.master_config_file)

        self.config_file = ""
        self.config = None

        self.left_frame = ttk.Frame(self)
        self.right_frame = ttk.Frame(self)

        self.vsb = ttk.Scrollbar(self.left_frame, orient="vertical")
        self.tree = ttk.Treeview(
            self.left_frame,
            columns=("enabled", "channel_point_alias"),
            selectmode="browse",
            yscrollcommand=self.vsb.set,
        )
        self.vsb.config(command=self.tree.yview)
        self.tree.pack(side="left", fill="both")
        self.vsb.pack(side="left", fill="y", anchor="w")

        self.tree.heading("#0", text="Key")
        self.tree.heading("enabled", text="Enabled", anchor="center")
        self.tree.heading(
            "channel_point_alias", text="Channel Point Alias", anchor="center"
        )
        self.tree.column("#0", width=150, anchor="center")
        self.tree.column("enabled", width=100, anchor="center")
        self.tree.column("channel_point_alias", width=200, anchor="center")
        self.tree.bind("<<TreeviewSelect>>", self.show_config)

        self.actions = ttk.Frame(self.right_frame)

        self._selected_game = tk.StringVar()
        self.game_configs_dropdown = ttk.Combobox(
            self.right_frame,
            state="readonly",
            values=list(self.master_config["GAME_CONFIGS"].keys()),
            textvariable=self._selected_game,
            width=50,
        )
        self.game_configs_dropdown.pack(
            side="top", anchor="n", fill="x", expand=False, padx=8, pady=8
        )
        self.game_configs_dropdown.bind("<<ComboboxSelected>>", self.load_game)

        # Pack the frames
        s = ttk.Style()
        self.actions.pack(side="top", fill="both", expand=True)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.right_frame.pack(side="right", fill="both", expand=True)

    def load_game(self, event):
        self.config_file = os.path.join(
            os.path.dirname(self._config_path),
            self.master_config["GAME_CONFIGS"][self._selected_game.get()],
        )
        self.config = toml.load(self.config_file)
        self.create_widgets()

    def create_widgets(self):
        self.tree.delete(*self.tree.get_children())

        for section in self.config:
            self.tree.insert("", "end", section, text=section)
            for key in self.config[section]:
                values = self.config[section][key]
                self.tree.insert(
                    section,
                    "end",
                    key,
                    text=key,
                    values=(
                        values.get("enabled", ""),
                        values.get("channel_point_alias", ""),
                    ),
                )

        self.enabled_var = tk.BooleanVar()
        self.enabled_label = ttk.Label(self.actions, text="Enabled:", anchor="ne")
        self.enabled_cb = ttk.Checkbutton(
            self.actions, variable=self.enabled_var, command=self.update_enabled
        )
        self.channel_point_alias_label = ttk.Label(
            self.actions, text="Channel Point Alias:", anchor="ne"
        )
        self.channel_point_alias_entry = ttk.Entry(self.actions)

        self.channel_point_alias_entry.bind(
            "<KeyRelease>", self.update_channel_point_alias
        )

    def update_enabled(self):
        item = self.tree.selection()[0]
        is_branch_node = bool(
            self.tree.get_children(item)
        )  # indicates if the node is a branch or leaf

        if not is_branch_node:
            section = self.tree.parent(item)
            key = item

            self.config[section][key]["enabled"] = self.enabled_var.get()
            self.tree.set(key, "enabled", str(self.enabled_var.get()))
        else:
            children = self.tree.get_children(item)
            for child in children:
                section = self.tree.parent(child)
                key = child
                self.config[section][key]["enabled"] = self.enabled_var.get()
                self.tree.set(child, "enabled", str(self.enabled_var.get()))

        with open(self.config_file, "w") as f:
            toml.dump(self.config, f)

    def update_channel_point_alias(self, event):
        item = self.tree.selection()[0]
        if self.tree.parent(item):
            section = self.tree.parent(item)
            key = item

            self.config[section][key][
                "channel_point_alias"
            ] = self.channel_point_alias_entry.get()
            with open(self.config_file, "w") as f:
                toml.dump(self.config, f)
            self.refresh_treeview_values(section, key)

    def show_config(self, event):
        item = self.tree.selection()[0]
        self.enabled_label.grid(row=0, column=0, sticky="ne", padx=5, pady=5)
        self.enabled_cb.grid(row=0, column=1, sticky="nw", padx=5, pady=5)

        if self.tree.parent(item):
            section = self.tree.parent(item)
            key = item
            values = self.config[section][key]
            self.enabled_var.set(values.get("enabled", False))

            self.channel_point_alias_entry.delete(0, tk.END)
            self.channel_point_alias_entry.insert(
                0, str(values.get("channel_point_alias", ""))
            )
            self.channel_point_alias_label.grid(
                row=1, column=0, sticky="ne", padx=5, pady=5
            )
            self.channel_point_alias_entry.grid(
                row=1, column=1, sticky="nw", padx=5, pady=5
            )
        else:
            children = self.tree.get_children(item)

            self.enabled_var.set(True)
            for child in children:
                section = self.tree.parent(child)
                key = child
                if not self.config[section][key]["enabled"]:
                    self.enabled_var.set(False)
                    break
            self.channel_point_alias_entry.delete(0, tk.END)
            self.channel_point_alias_label.grid_remove()
            self.channel_point_alias_entry.grid_remove()

    def save_config(self):
        for section in self.config:
            for key in self.config[section]:
                item = self.tree.item(key)
                self.config[section][key]["enabled"] = item["values"][0]
                self.config[section][key]["channel_point_alias"] = item["values"][1]
        with open(self.config_file, "w") as f:
            toml.dump(self.config, f)

    def refresh_treeview_values(self, section, key):
        values = self.config[section][key]
        self.tree.set(key, "enabled", str(values.get("enabled", False)))
        self.tree.set(key, "channel_point_alias", values.get("channel_point_alias", ""))
