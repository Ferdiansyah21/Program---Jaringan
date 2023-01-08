#import library yang dibutuhkan
import tkinter  
from tkinter import *
from scapy.layers.l2 import Ether, ARP, srp
import re

#====GUI=====
WINDOW_RESIZEABLE = False
WINDOW_SIZE = (400, 500)

gui = Tk()
gui.title('Network Scanner')
gui.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
gui.resizable(width = WINDOW_RESIZEABLE, height = WINDOW_RESIZEABLE)

#====delete Function====
def delete():
    listbox.delete(0,tkinter.END)

#====scanning Function====
def startScan():
    ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")
    
    while True:
        ip_add_range_entered = L22.get()

        if ip_add_range_pattern.search(ip_add_range_entered):
            l1 = Label(gui, text=f"{ip_add_range_entered} is a valid ip address range           ",font=("Times New Roman", 12))
            l1.place(x=16, y=160)
            break
        else:
            l2 = Label(gui, text=f"{ip_add_range_entered} is NOT a valid ip address range", font=("Times New Roman", 12), fg='red')
            l2.place(x=16, y=160)
            break

    arp = ARP(pdst=ip_add_range_entered)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    clients = []

    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    for client in clients:
        listbox.insert(END, "    {:16}           {}".format(client['ip'], client['mac']))

#===Colors====
m1c ='#00ee00'
bgc ='#222222'
dbg ='#000000'
fgc ='#111111'

gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc, highlightColor=m1c, highlightBackground=m1c)

#===Labels====
L11 = Label(gui, text="Network Scanner", font=("Times New Roman", 16, 'bold'))
L11.place(x=10,y=10)

L21 = Label(gui, text="Target IP  : ", font=("Times New Roman", 12))
L21.place(x=16, y=90)

L22 = Entry(gui, text = "Target IP  : ", font=("Times New Roman", 12))
L22.place(x=100, y=90)
L22.insert(0,"192.168.1.1/24")

L23 = Label(gui,text=" (Contoh : 192.168.1.1/24)", font=("Times New Roman", 10))
L23.place(x=95,y=115)

L24 = Label(gui, text="IP                                MAC", font=("Times New Roman", 12))
L24.place(x=85, y=215)

#====IP results====#
frame = Frame(gui)
frame.place(x=34,y=240, height= 165, width=320)
listbox = Listbox(frame, width=50,height=10, font=("Times New Roman", 12))
listbox.place(x=0,y=0)

#===scroll bar====
scrollbar1 = Scrollbar(frame)
scrollbar1.pack(side=RIGHT,fill=Y)
listbox.config(yscrollcommand=scrollbar1.set)
scrollbar1.config(command=listbox.yview)

scrollbar2 = Scrollbar(frame,orient='horizontal')
scrollbar2.pack(side=BOTTOM,fill=X)
listbox.config(xscrollcommand=scrollbar2.set)
scrollbar2.config(command=listbox.xview)

#====Buttons=======
B11 = Button(gui,text= "Start Scan",font=("Times New Roman", 12),command=startScan)
B11.place(x=16,y=430, width=170)

B11 = Button(gui,text= "Clear",font=("Times New Roman", 12),command=delete)
B11.place(x=200,y=430, width=170)

#=====Start GUI=====
gui.mainloop()