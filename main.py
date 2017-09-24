from Tkinter import *

iteratorVal = 0


def iterator():
    global iteratorVal
    iteratorVal += 1
    return iteratorVal - 1


def update_screen():
    acceleration_output.update()


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
    def __init__(self, label, units, root, master, offset):
        self.offset = offset
        self.root = root
        self.inVar = StringVar()
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


root1 = Tk()
panel = Frame(root1).grid()

root1.title('Parameters')

LabelLabel = Label(text='Field').grid(row=iteratorVal,column=0)
InputLabel = Label(text='Value').grid(row=iteratorVal,column=1)
UnitsLabel = Label(text='Units').grid(row=iterator(),column=2)

mass_input = InputStructure('Mass', 'kg', root1, panel, iterator())
force_input = InputStructure('Force', 'N', root1, panel, iterator())

BreakLabel = Label(text='---------').grid(row=iterator(), column=1)

acceleration_output = OutputStructure('Acceleration', 'm/s^2', root1, panel, 4)


def calculate_acceleration(self):
    acceleration = force_input.get_input() / mass_input.get_input()
    return acceleration


acceleration_output.math = calculate_acceleration.__get__(acceleration_output, OutputStructure)

mbutton = Button(panel, text='Update', command=update_screen).grid(columnspan=3)

update_screen()

root1.mainloop()
