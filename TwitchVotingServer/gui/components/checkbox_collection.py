import tkinter as tk
import tkinter.ttk as ttk


class CheckboxCollectionStore:
    def __init__(self):
        self.trees = dict()

    def to_dict(self):
        result = dict()
        for tree in self.trees:
            result[tree] = self.trees[tree].to_dict()
        return result

    def add(self, tree_name, tree):
        tree.root = self
        self.trees[tree_name] = tree


class CheckboxTreeStore:
    def __init__(self, name):
        self.parent = None
        self.tree_name = name
        self.sections = dict()

    def to_dict(self):
        result = dict()
        for section in self.sections:
            result[section] = self.sections[section].option_vars
        return result

    def add(self, section_name, section):
        section.tree = self
        self.sections[section_name] = section


class CheckboxSectionStore:
    def __init__(self, name):
        self.tree = None
        self.section_name = name
        self.section_var = None
        self.option_vars = dict()

    def __checkbox_section_select(self):
        value = self.section_var.get()
        for option in self.option_vars:
            self.option_vars[option].set(value)

    def create_section_var(self, root):
        self.section_var = tk.BooleanVar(root, value=True)
        for option in self.option_vars.values():
            if option.get() == False:
                self.section_var.set(False)
                return self.section_var
        return self.section_var

    def create_button(self, root):
        self.button = ttk.Checkbutton(
            root,
            cursor="hand2",
            text=f"{self.section_name.upper().replace('_', ' ')}",
            variable=self.section_var,
            command=self.__checkbox_section_select,
        )
        return self.button
