from Tkinter import *


class InputStructure:
    def __init__(self, label, units, root, master, offset):
        self.root = root
        self.inVar = StringVar()
        self.panel = master
        vcmd = (root.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.label = Label(self.panel, text=label).grid(row=offset, column=0)
        self.inputFld = Entry(self.panel, textvariable=self.inVar, validate='key', validatecommand=vcmd)
        self.inputFld.grid(row=offset, column=1)
        self.label = Label(self.panel, text=units).grid(row=offset, column=2)

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-':
            if value_if_allowed == "" or value_if_allowed == "-":
                return True
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def get_input(self):
        try:
            return float(self.inputFld.get())
        except ValueError:
            return 0


class OutputStructure:
    registry = []

    def __init__(self, label, units, root, master, offset):
        self.registry.append(self)
        self.offset = offset
        self.root = root
        self.panel = master
        self.outputVar = StringVar()
        self.outputVar.set("ERR")
        Label(self.panel, text=label).grid(row=offset, column=0)
        self.output_label = Label(self.panel, textvariable=self.outputVar)
        self.output_label.grid(row=offset, column=1)
        Label(self.panel, text=units).grid(row=offset, column=2)

    def math(self):
        print "Error, unset function"
        return 0

    def update(self):
        try:
            value = self.math()
            self.outputVar.set(value)
        except ZeroDivisionError:
            self.outputVar.set('NaN')