from Tkinter import *
from decimal import Decimal


class InputStructure:

    def __init__(self, label, units, default, root, master, offset):
        self.root = root
        self.inVar = StringVar()
        self.hybridVar = 0
        self.hybridLabelVar = StringVar()
        self.inVar.set(default)
        self.panel = master
        vcmd = (root.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        Label(self.panel, text=label).grid(row=offset, column=0)
        self.inputFld = Entry(self.panel, textvariable=self.inVar, validate='key', validatecommand=vcmd)
        self.inputFld.grid(row=offset, column=1)
        Label(self.panel, text=units).grid(row=offset, column=3)
        self.hybridLabel = Label(self.panel, textvariable=self.hybridLabelVar)
        self.hybridLabel.grid(row=offset, column=2)

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

    def set_hybrid(self, hybrid_val):
        self.hybridLabelVar.set("{:.2E}".format(Decimal(hybrid_val)))
        self.hybridVar = hybrid_val

    def get_hybrid(self):
        return self.hybridVar


class OutputStructure:

    def __init__(self, label, units, root, master, offset):
        self.offset = offset
        self.root = root
        self.panel = master
        self.hybridVar = 0
        self.hybridLabelVar = StringVar()
        self.hybridLabelVar.set("ERR")
        self.referenceVar = 0
        self.referenceLabelVar = StringVar()
        self.referenceLabelVar.set("ERR")
        Label(self.panel, text=label).grid(row=offset, column=0)
        self.output_label = Label(self.panel, textvariable=self.referenceLabelVar)
        self.output_label.grid(row=offset, column=1)
        self.hybrid_label = Label(self.panel, textvariable=self.hybridLabelVar)
        self.hybrid_label.grid(row=offset, column=2)
        Label(self.panel, text=units).grid(row=offset, column=3)

    def set_reference(self, reference_val):
        self.referenceLabelVar.set(reference_val)
        self.referenceVar = reference_val

    def get_hybrid(self):
        return self.hybridVar

    def set_hybrid(self, hybrid_val):
        self.hybridLabelVar.set(hybrid_val)
        self.hybridVar = hybrid_val

    def get_hybrid(self):
        return self.hybridVar
