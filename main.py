from Tkinter import *
from gui_elements import InputStructure, OutputStructure

iteratorVal = 0


def iterator():
    global iteratorVal
    iteratorVal += 1
    return iteratorVal - 1


def update_screen():
    for output in OutputStructure.registry:
        output.update()


root1 = Tk()
panel = Frame(root1).grid()

root1.title('Parameters')

LabelLabel = Label(text='Field').grid(row=iteratorVal, column=0)
InputLabel = Label(text='Value').grid(row=iteratorVal, column=1)
UnitsLabel = Label(text='Units').grid(row=iterator(), column=2)

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
