from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
import serial
import sys
import glob
import serial.tools.list_ports


ser_in = serial.Serial()
ser_out = serial.Serial()

serial_parity = {
    "None": 'N',
    "Even": 'E',
    "Odd": 'O'
}

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def list_ports():
    ports = serial.tools.list_ports.comports()

    pts = []
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        pts.append(port)

    return pts

def fahrenheit_to_celsius(fahrenheit):
    """Convert the value for Fahrenheit to Celsius and insert the
    result into lbl_result.
    """
    celsius = (5/9) * (float(fahrenheit) - 32)
    return celsius
    
def convert_clicked():
    fahrenheit = ent_temperature.get()
    temp_celsius = fahrenheit_to_celsius(fahrenheit)
    lbl_result["text"] = f"{round(temp_celsius, 2)} \N{DEGREE CELSIUS}"

def check_comm_state():
    if ser_in.is_open or ser_out.is_open:
        btn_connect["state"] = DISABLED
        btn_disconnect["state"] = NORMAL
    else:
        btn_connect["state"] = NORMAL
        btn_disconnect["state"] = DISABLED


def __comm_connect():
    #ser_in  = serial.Serial(cbx_port_in.get(), cbx_baud.get(), timeout=0, parity=serial_parity.get(cbx_parity.get()), rtscts=1)
    ser_in.port = cbx_port_in.get()
    ser_in.baudrate = cbx_baud.get()
    ser_in.parity = serial_parity.get(cbx_parity.get())

    ser_out.port = cbx_port_in.get()
    ser_out.baudrate = cbx_baud.get()
    ser_out.parity = serial_parity.get(cbx_parity.get())

    try:
        ser_out.open()
        ser_in.open()
    except:
        tbx_log.insert(sys.exc_info()[0])
        print("Unexpected error:", sys.exc_info()[0])

    check_comm_state()

    #ser_in.write(b'Hello there!')
    
def __comm_disconnect():
    ser_in.close()
    check_comm_state()

def __comm_send():
    res = "Welcome to " + txt.get()
    #tbx_log.configure(text= res)
    #print(list_ports())
    print(cbx_port_in.get(), cbx_baud.get(), serial_parity.get(cbx_parity.get()))
    ser_in.write(b'Hello there!')
    #print(ser_in.read(2))

def __comm_reiceive():
    while True:
        bytesToRead = ser_in.inWaiting()
        ser_in.read(bytesToRead)

window = Tk()
window.title("SerMan - Serial Manipulator")

# Comm settings
lbl_port_in = Label(window, text="Port In")
lbl_port_in.grid(column=0, row=0, padx=0, pady=5)

cbx_port_in = Combobox(window, width=6)
cbx_port_in.grid(column=1, row=0, padx=0)
cbx_port_in['values'] = list_ports()
cbx_port_in.current(2)

lbl_port_out = Label(window, text="Port Out")
lbl_port_out.grid(column=2, row=0, padx=0)

cbx_port_out = Combobox(window, width=6)
cbx_port_out.grid(column=3, row=0, padx=0)
cbx_port_out['values'] = list_ports()
cbx_port_out.current(3)

lbl_baud = Label(window, text="Baudrate")
lbl_baud.grid(column=4, row=0, padx=0)

cbx_baud = Combobox(window, width=6)
cbx_baud.grid(column=5, row=0, padx=0)
cbx_baud['values'] = (1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, "Other, plz enter")
cbx_baud.current(0)

lbl_parity = Label(window, text="Parity")
lbl_parity.grid(column=6, row=0, padx=0)

cbx_parity = Combobox(window, width=6)
cbx_parity.grid(column=7, row=0, padx=0)
cbx_parity['values'] = list(serial_parity.keys())
cbx_parity.current(0)

#current_combo_style = cbx_baud.cget('style') or "TCombobox"
#style_name = current_combo_style
#style = ttk.Style()
#style.configure(style_name, postoffset=(0,0,width,0))
#cbx_baud.configure(style=style_name)

btn_connect = Button(window, text="Connect", command=__comm_connect)
btn_connect.grid(column=8, row=0)

btn_disconnect = Button(window, text="Disconnect", command=__comm_disconnect)
btn_disconnect.grid(column=9, row=0)
btn_disconnect["state"] = NORMAL
check_comm_state()

txt = Entry(window,width=10)
#txt.grid(column=0, row=0)
txt.focus()


btn_send = Button(window, text="Send", command=__comm_send)
btn_send.grid(column=0, row=2)

btn_receive = Button(window, text="Receive", command=__comm_reiceive)
btn_receive.grid(column=1, row=2)

ent_temperature = Entry(window, width=10)
ent_temperature.grid(column=0, row=3)

btn_convert = Button(window, text="Convert", command=convert_clicked)
btn_convert.grid(column=1, row=3)

lbl_result = Label(window,width=10)
lbl_result.grid(column=2, row=3)



tbx_log = Text()
tbx_log.grid(column=0, row=5, columnspan=10, padx=5, pady=5)
#tbx_log.pack()
#tbx_log.place(x=0, y=150, height=250, width=600)


window.geometry('800x600')
window.mainloop()

