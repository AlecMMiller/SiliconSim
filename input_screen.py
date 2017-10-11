from Tkinter import *
from gui_elements import InputStructure, OutputStructure
from math import log10
import interlock
import threading

iteratorVal = 0


def iterator():
    global iteratorVal
    iteratorVal += 1
    return iteratorVal - 1


class Input:
    mobility = 0.06
    kSilicon = 11.8
    kOxide = 3.9
    vScaleIndex = 0.5
    datum = 0.1
    breakdownCo = 8*10**46
    breakdownIndex = -33.5
    depLayer = 20
    trackMultiplier = 50

    def __init__(self):
        print "input started"
        self.root1 = Tk()
        self.panel = Frame(self.root1).grid()

        self.root1.title('Parameters')

        Label(text='Field').grid(row=iteratorVal, column=0)
        Label(text='Value').grid(row=iteratorVal, column=1)
        Label(text='Hybrid').grid(row=iteratorVal, column=2)
        Label(text='Units').grid(row=iterator(), column=3)

        self.k_val = InputStructure('K Value', '', 0.7, self.root1, self.panel, iterator())
        self.cdl = InputStructure('CD = L', 'nm', 65, self.root1, self.panel, iterator())
        self.ox_thick = InputStructure('Gate ox thickness', 'nm', 1.5, self.root1, self.panel, iterator())
        self.poly_sheet = InputStructure('Poly Sheet R', 'ohms/sq', 25, self.root1, self.panel, iterator())
        self.sd_sheet = InputStructure('S-D Sheet R', 'ohms/sq', 40, self.root1, self.panel, iterator())
        self.metal_sheet = InputStructure('Metal Sheet R', 'ohms/sq', 0.02, self.root1, self.panel, iterator())
        self.supply_voltage = InputStructure('Supply Voltage', 'V', 1.5, self.root1, self.panel, iterator())
        self.ref_power = InputStructure('Ref Power', 'uW', 1, self.root1, self.panel, iterator())

        Label(text='---------').grid(row=iterator(), column=1)

        self.gate_capacitance = OutputStructure('Gate Capacitance', 'fF', self.root1, self.panel, iterator())
        self.gate_leakage = OutputStructure('Gate Leakage Current', 'mA/mm^2', self.root1, self.panel, iterator())
        self.transistor_gain = OutputStructure('Transistor Gain K', 'mA/V^2', self.root1, self.panel, iterator())
        self.poly_rc = OutputStructure('Poly RC Const', 'ps', self.root1, self.panel, iterator())
        self.metal_rc = OutputStructure('Metal RC Const', 'ps', self.root1, self.panel, iterator())
        self.thresh = OutputStructure('Threshold Voltage', 'V', self.root1, self.panel, iterator())
        self.max_idsat = OutputStructure('Max Idsat', 'mA', self.root1, self.panel, iterator())
        self.depletion_width = OutputStructure('Depletion Layer Width', 'mm', self.root1, self.panel, iterator())
        self.channel_doping_m = OutputStructure('Channel Doping', '1/m^3', self.root1, self.panel, iterator())
        self.channel_doping_cm = OutputStructure('Channel Doping', '1/cm^3', self.root1, self.panel, iterator())
        self.max_lateral = OutputStructure('Max Lateral Field', 'MV/m', self.root1, self.panel, iterator())
        self.max_oxide = OutputStructure('Max Oxide Field', 'MV/m', self.root1, self.panel, iterator())
        self.sd_transit = OutputStructure('S-D Transit Time', 'ps', self.root1, self.panel, iterator())
        self.on_resistance = OutputStructure('ON Resistance', 'kohm', self.root1, self.panel, iterator())
        self.well_breakdown = OutputStructure('Well Breakdown Voltage', 'V', self.root1, self.panel, iterator())
        self.max_current = OutputStructure('Max Current/Micron', 'mA/micron', self.root1, self.panel, iterator())
        self.power_density = OutputStructure('Power Density', 'MW/m^2', self.root1, self.panel, iterator())

    def update_screen(self):
        try:
            kVal = self.k_val.get_input()
            gVal = kVal ** self.vScaleIndex
            self.k_val.set_hybrid(gVal)
            self.cdl.set_hybrid(self.cdl.get_input()*kVal)
            self.ox_thick.set_hybrid(self.ox_thick.get_input()*kVal)
            self.poly_sheet.set_hybrid(self.poly_sheet.get_input()/kVal)
            self.sd_sheet.set_hybrid(self.sd_sheet.get_input()/kVal)
            self.metal_sheet.set_hybrid(self.metal_sheet.get_input()/kVal)
            self.supply_voltage.set_hybrid(self.supply_voltage.get_input()*gVal)
            self.ref_power.set_hybrid(self.ref_power.get_input()*gVal**3/kVal)

            self.gate_capacitance.set_reference(
                1000000000*self.kOxide*0.0000000000089*(self.cdl.get_input()*0.000001)**2/
                (self.ox_thick.get_input()*0.000000001))
            self.gate_leakage.set_reference(self.datum*10**(1.5-self.ox_thick.get_input()))
            self.transistor_gain.set_reference(
                1000*self.kOxide*0.0000000000089*self.mobility/(self.ox_thick.get_input()*0.000000001))

            self.poly_rc.set_reference(self.trackMultiplier*self.gate_capacitance.get_reference()*self.poly_sheet.get_input()/1000)
            self.metal_rc.set_reference(self.gate_capacitance.get_reference()*self.metal_sheet.get_input()*self.trackMultiplier)

            self.thresh.set_reference(self.supply_voltage.get_input()/4)
            self.max_idsat.set_reference(0.5*self.transistor_gain.get_reference()*(self.supply_voltage.get_input()-self.thresh.get_reference())**2)
            self.depletion_width.set_reference(self.cdl.get_input()*self.depLayer/100)
            self.channel_doping_m.set_reference(self.kSilicon*0.0000000000089*(self.supply_voltage.get_input()+0.025)/(1.6*10**-19*(self.depletion_width.get_reference()*0.000000001)**2))
            self.channel_doping_cm.set_reference(self.channel_doping_m.get_reference()*0.000001)
            self.max_lateral.set_reference(1000*(self.supply_voltage.get_input()-self.thresh.get_reference())/self.depletion_width.get_reference())
            self.max_oxide.set_reference(1000*self.supply_voltage.get_input()/self.ox_thick.get_input())
            self.sd_transit.set_reference(0.000001*self.cdl.get_input()**2/(self.supply_voltage.get_input()*self.mobility))
            self.on_resistance.set_reference(1/(self.transistor_gain.get_reference()*(self.supply_voltage.get_input()-self.thresh.get_reference())))
            self.well_breakdown.set_reference(self.breakdownCo*log10(self.channel_doping_m.get_reference())**self.breakdownIndex)
            self.max_current.set_reference(1000*self.max_idsat.get_reference()/self.cdl.get_input())
            self.power_density.set_reference(0.000001*self.ref_power.get_input()*0.000001/(self.cdl.get_input()*0.000000001)**2)

            # Hybrids

            self.gate_capacitance.set_hybrid(self.gate_capacitance.get_reference()*kVal)
            self.gate_leakage.set_hybrid(self.gate_leakage.get_reference()*10**(5*(self.ox_thick.get_input()-self.ox_thick.get_hybrid())))
            self.transistor_gain.set_hybrid(self.transistor_gain.get_reference() / kVal)

            self.poly_rc.set_hybrid(self.trackMultiplier*self.gate_capacitance.get_hybrid()*self.poly_sheet.get_hybrid()/1000)
            self.metal_rc.set_hybrid(self.gate_capacitance.get_hybrid()*self.metal_sheet.get_hybrid()*self.trackMultiplier)

            self.thresh.set_hybrid(self.thresh.get_reference()*gVal)
            h_volt_diff = self.supply_voltage.get_hybrid() - self.thresh.get_hybrid()
            self.max_idsat.set_hybrid(0.5*self.transistor_gain.get_hybrid()*h_volt_diff**2)
            self.depletion_width.set_hybrid(self.cdl.get_hybrid()*self.depLayer/100)
            self.channel_doping_m.set_hybrid(self.kSilicon * 0.0000000000089 * (self.supply_voltage.get_hybrid() + 0.025) / (1.6 * 10 ** -19 * (self.depletion_width.get_hybrid() * 0.000000001) ** 2))
            self.channel_doping_cm.set_hybrid(self.channel_doping_m.get_hybrid() * 0.000001)
            self.max_lateral.set_hybrid(1000 * (self.supply_voltage.get_hybrid() - self.thresh.get_hybrid()) / self.depletion_width.get_hybrid())
            self.max_oxide.set_hybrid(1000 * self.supply_voltage.get_hybrid() / self.ox_thick.get_hybrid())
            self.sd_transit.set_hybrid(0.000001 * self.cdl.get_hybrid() ** 2 / (self.supply_voltage.get_hybrid() * self.mobility))
            self.on_resistance.set_hybrid(1 / (self.transistor_gain.get_hybrid() * (self.supply_voltage.get_hybrid() - self.thresh.get_hybrid())))
            self.well_breakdown.set_hybrid(self.breakdownCo * log10(self.channel_doping_m.get_hybrid()) ** self.breakdownIndex)
            self.max_current.set_hybrid(1000 * self.max_idsat.get_hybrid() / self.cdl.get_hybrid())
            self.power_density.set_hybrid(0.000001 * self.ref_power.get_hybrid() * 0.000001 / (self.cdl.get_hybrid() * 0.000000001) ** 2)
        except ZeroDivisionError:
            print "zero division occurred"

    def run(self):

        Button(self.panel, text='Update', command=self.update_screen).grid(columnspan=4)

        self.update_screen()

        interlock.animation_ready = True

        while interlock.animation_ready:
            try:
                self.root1.update()
            except TclError:
                interlock.animation_ready = False
                pass


input_screen = Input()


class UpdateThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        input_screen.run()


input_thread = UpdateThread(2)


def start():
    input_thread.start()
