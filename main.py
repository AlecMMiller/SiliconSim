from Tkinter import *
from gui_elements import InputStructure, OutputStructure
from math import log10

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
        supply_voltage.set_hybrid(supply_voltage.get_input()*gVal)
        ref_power.set_hybrid(ref_power.get_input()*gVal**3/kVal)

        gate_capacitance.set_reference(1000000000*kOxide*0.0000000000089*(cdl.get_input()*0.000001)**2/(ox_thick.get_input()*0.000000001))
        gate_leakage.set_reference(datum*10**(1.5-ox_thick.get_input()))
        transistor_gain.set_reference(1000*kOxide*0.0000000000089*mobility/(ox_thick.get_input()*0.000000001))

        poly_rc.set_reference(trackMultiplier*gate_capacitance.get_reference()*poly_sheet.get_input()/1000)
        metal_rc.set_reference(gate_capacitance.get_reference()*metal_sheet.get_input()*trackMultiplier)

        thresh.set_reference(supply_voltage.get_input()/4)
        max_idsat.set_reference(0.5*transistor_gain.get_reference()*(supply_voltage.get_input()-thresh.get_reference())**2)
        depletion_width.set_reference(cdl.get_input()*depLayer/100)
        channel_doping_m.set_reference(kSilicon*0.0000000000089*(supply_voltage.get_input()+0.025)/(1.6*10**-19*(depletion_width.get_reference()*0.000000001)**2))
        channel_doping_cm.set_reference(channel_doping_m.get_reference()*0.000001)
        max_lateral.set_reference(1000*(supply_voltage.get_input()-thresh.get_reference())/depletion_width.get_reference())
        max_oxide.set_reference(1000*supply_voltage.get_input()/ox_thick.get_input())
        sd_transit.set_reference(0.000001*cdl.get_input()**2/(supply_voltage.get_input()*mobility))
        on_resistance.set_reference(1/(transistor_gain.get_reference()*(supply_voltage.get_input()-thresh.get_reference())))
        well_breakdown.set_reference(breakdownCo*log10(channel_doping_m.get_reference())**breakdownIndex)
        max_current.set_reference(1000*max_idsat.get_reference()/cdl.get_input())
        power_density.set_reference(0.000001*ref_power.get_input()*0.000001/(cdl.get_input()*0.000000001)**2)

        # Hybrids

        gate_capacitance.set_hybrid(gate_capacitance.get_reference()*kVal)
        gate_leakage.set_hybrid(gate_leakage.get_reference()*10**(5*(ox_thick.get_input()-ox_thick.get_hybrid())))
        transistor_gain.set_hybrid(transistor_gain.get_reference() / kVal)

        poly_rc.set_hybrid(trackMultiplier*gate_capacitance.get_hybrid()*poly_sheet.get_hybrid()/1000)
        metal_rc.set_hybrid(gate_capacitance.get_hybrid()*metal_sheet.get_hybrid()*trackMultiplier)

        thresh.set_hybrid(thresh.get_reference()*gVal)
        h_volt_diff = supply_voltage.get_hybrid() - thresh.get_hybrid()
        max_idsat.set_hybrid(0.5*transistor_gain.get_hybrid()*h_volt_diff**2)
        depletion_width.set_hybrid(cdl.get_hybrid()*depLayer/100)
        channel_doping_m.set_hybrid(kSilicon * 0.0000000000089 * (supply_voltage.get_hybrid() + 0.025) / (1.6 * 10 ** -19 * (depletion_width.get_hybrid() * 0.000000001) ** 2))
        channel_doping_cm.set_hybrid(channel_doping_m.get_hybrid() * 0.000001)
        max_lateral.set_hybrid(1000 * (supply_voltage.get_hybrid() - thresh.get_hybrid()) / depletion_width.get_hybrid())
        max_oxide.set_hybrid(1000 * supply_voltage.get_hybrid() / ox_thick.get_hybrid())
        sd_transit.set_hybrid(0.000001 * cdl.get_hybrid() ** 2 / (supply_voltage.get_hybrid() * mobility))
        on_resistance.set_hybrid(1 / (transistor_gain.get_hybrid() * (supply_voltage.get_hybrid() - thresh.get_hybrid())))
        well_breakdown.set_hybrid(breakdownCo * log10(channel_doping_m.get_hybrid()) ** breakdownIndex)
        max_current.set_hybrid(1000 * max_idsat.get_hybrid() / cdl.get_hybrid())
        power_density.set_hybrid(0.000001 * ref_power.get_hybrid() * 0.000001 / (cdl.get_hybrid() * 0.000000001) ** 2)
    except ZeroDivisionError:
        print "zero division occurred"


mbutton = Button(panel, text='Update', command=update_screen).grid(columnspan=4)

update_screen()

root1.mainloop()
