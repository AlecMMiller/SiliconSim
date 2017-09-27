from Tkinter import *
from gui_elements import InputStructure, OutputStructure

mobility = 0.06
kSilicon = 11.8
kOxide = 3.9
vScaleIndex = 0.5
datum = 0.1
breakdownCo = 8*10**46
breakdownIndex = -33.5
depLayer = 20
trackMultiplier = 50

iteratorVal = 0
print "started"


def iterator():
    global iteratorVal
    iteratorVal += 1
    return iteratorVal - 1


root1 = Tk()
panel = Frame(root1).grid()

root1.title('Parameters')

LabelLabel = Label(text='Field').grid(row=iteratorVal, column=0)
InputLabel = Label(text='Value').grid(row=iteratorVal, column=1)
UnitsLabel = Label(text='Hybrid').grid(row=iteratorVal, column=2)
UnitsLabel = Label(text='Units').grid(row=iterator(), column=3)

k_val = InputStructure('K Value', '', 0.7, root1, panel, iterator())
cdl = InputStructure('CD = L', 'nm', 65, root1, panel, iterator())
ox_thick = InputStructure('Gate ox thickness', 'nm', 1.5, root1, panel, iterator())
poly_sheet = InputStructure('Poly Sheet R', 'ohms/sq', 25, root1, panel, iterator())
sd_sheet = InputStructure('S-D Sheet R', 'ohms/sq', 40, root1, panel, iterator())
metal_sheet = InputStructure('Metal Sheet R', 'ohms/sq', 0.02, root1, panel, iterator())
supply_voltage = InputStructure('Supply Voltage', 'V', 1.5, root1, panel, iterator())
ref_power = InputStructure('Ref Power', 'uW', 1, root1, panel, iterator())

BreakLabel = Label(text='---------').grid(row=iterator(), column=1)

gate_capacitance = OutputStructure('Gate Capacitance', 'fF', root1, panel, iterator())
gate_leakage = OutputStructure('Gate Leakage Current', 'mA/mm^2', root1, panel, iterator())
transistor_gain = OutputStructure('Transistor Gain K', 'mA/V^2', root1, panel, iterator())
poly_rc = OutputStructure('Poly RC Const', 'ps', root1, panel, iterator())
metal_rc = OutputStructure('Metal RC Const', 'ps', root1, panel, iterator())
thresh = OutputStructure('Threshold Voltage', 'V', root1, panel, iterator())
max_idsat = OutputStructure('Max Idsat', 'mA', root1, panel, iterator())
depletion_width = OutputStructure('Depletion Layer Width', 'mm', root1, panel, iterator())
channel_doping_m = OutputStructure('Channel Doping', '1/m^3', root1, panel, iterator())
channel_doping_cm = OutputStructure('Channel Doping', '1/cm^3', root1, panel, iterator())
max_lateral = OutputStructure('Max Lateral Field', 'MV/m', root1, panel, iterator())
max_oxide = OutputStructure('Max Oxide Field', 'MV/m', root1, panel, iterator())
sd_transit = OutputStructure('S-D Transit Time', 'ps', root1, panel, iterator())
on_resistance = OutputStructure('ON Resistance', 'kohm', root1, panel, iterator())
well_breakdown = OutputStructure('Well Breakdown Voltage', 'V', root1, panel, iterator())
max_current = OutputStructure('Max Current/Micron', 'mA/micron', root1, panel, iterator())
power_density = OutputStructure('Power Density', 'MW/m^2', root1, panel, iterator())


def update_screen():
    try:
        kVal = k_val.get_input()
        gVal = kVal ** vScaleIndex
        k_val.set_hybrid(gVal)
        cdl.set_hybrid(cdl.get_input()*kVal)
        ox_thick.set_hybrid(ox_thick.get_input()*kVal)
        poly_sheet.set_hybrid(poly_sheet.get_input()/kVal)
        sd_sheet.set_hybrid(sd_sheet.get_input()/kVal)
        metal_sheet.set_hybrid(metal_sheet.get_input()/kVal)
        supply_voltage.set_hybrid(supply_voltage.get_input()*kVal)
        ref_power.set_hybrid(ref_power.get_input()*gVal**3/kVal)
    except ZeroDivisionError:
        print "zero division occurred"


mbutton = Button(panel, text='Update', command=update_screen).grid(columnspan=4)

update_screen()

root1.mainloop()
