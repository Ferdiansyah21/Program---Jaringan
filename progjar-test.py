#import library yang dibutuhkan
import speedtest
import threading
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from psutil import net_io_counters

#atur window size
WINDOW_SIZE = (400, 500)  

#atur agar ukuran window tetap konstan, tidak bisa diresize
WINDOW_RESIZEABLE = False 

#membuat main window
window = tk.Tk()

#membuat judul window
window.title("Network Management")

#atur window geometry berdasarkan value pada WINDOW_SIZE
window.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")

#atur window resizable berdasarkan value pada WINDOW_RESIZABLE
window.resizable(width = WINDOW_RESIZEABLE, height = WINDOW_RESIZEABLE)

#membuat frame
frame = tk.Frame(window)
frame.pack()

#membuat function menu untuk pilihan menu program yang ingin digunakan
def menu():  
    
    #menghapus widgets sebelumnya setelah update window
    for widgets in frame.winfo_children():
        widgets.destroy()
        
    #atur judul window
    window.title("Network Management")
    
    #membuat label kosong untuk menambah baris kosong
    label_kosong = tk.Label(frame, text="").pack()
    
    #membuat label pilihan
    label_pilihan = tk.Label(frame, text = "Silahkan Pilih Menu :", font = "Quicksand 16 bold")
    label_pilihan.pack(pady=5)

    #inisialisasi variabel global untuk button
    global speedtest_button, bandwidth_button
    
    label_kosong = tk.Label(frame, text="").pack()
    
    #membuat button untuk pilihan program yang ingin digunakan
    speedtest_button = tk.Button(frame, text = 'Speedtest', width='100', height='2', font='Quicksand 12 bold',command=speedtestdef).pack(side = TOP)
    bandwidth_button = tk.Button(frame, text = 'Bandwidth Monitor', width='100', height='2', font='Quicksand 12 bold',command=bandwidthdef).pack(side = TOP)
    
#membuat function untuk program bandwidth
def bandwidthdef():    
    
    #menghapus widgets sebelumnya setelah update window
    for widgets in frame.winfo_children():
        widgets.destroy()
    
    #membuat variabel yang akan digunakan pada function size()    
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776
    
    #membuat variabel global
    global last_upload, last_download, upload_speed, down_speed
    last_upload, last_download, upload_speed, down_speed = 0, 0, 0, 0

    #membuat function size
    def size(B):
        B = float(B)
        if B < KB: return f"{B} Bytes"
        elif KB <= B < MB: return f"{B/KB:.2f} KB"
        elif MB <= B < GB: return f"{B/MB:.2f} MB"
        elif GB <= B < TB: return f"{B/GB:.2f} GB"
        elif TB <= B: return f"{B/TB:.2f} TB"

    #membuat window update delay selama 1 detik / 1000ms
    REFRESH_DELAY = 1000
    
    #atur judul window
    window.title("Bandwidth Monitor")
    
    #membuat label untuk judul program
    label_kosong = tk.Label(frame, text="").pack()
    label_judul = tk.Label(frame, text = "Bandwidth Monitor", font = "Quicksand 16 bold").pack(pady=5)
    label_kosong = tk.Label(frame, text="").pack()
    
    #membuat label untuk total upload
    label_total_upload_header = tk.Label(frame, text = "Total Upload:", font = "Quicksand 12 bold")
    label_total_upload_header.pack()
    label_total_upload = tk.Label(frame, text = "Calculating...", font = "Quicksand 12")
    label_total_upload.pack()

    #membuat label untuk total download
    label_total_download_header = tk.Label(frame, text = "Total Download:", font = "Quicksand 12 bold")
    label_total_download_header.pack()
    label_total_download = tk.Label(frame, text = "Calculating...", font = "Quicksand 12")
    label_total_download.pack()

    #membuat label untuk total usage
    label_total_usage_header = tk.Label(frame, text = "Total Usage:", font = "Quicksand 12 bold")
    label_total_usage_header.pack()
    label_total_usage = tk.Label(frame, text = "Calculating...", font = "Quicksand 12")
    label_total_usage.pack()

    #membuat label untuk upload
    label_upload_header = tk.Label(frame, text = "Upload:", font = "Quicksand 12 bold")
    label_upload_header.pack()
    label_upload = tk.Label(frame, text = "Calculating...", font = "Quicksand 12")
    label_upload.pack()

    #membuat label untuk download
    label_download_header = tk.Label(frame, text = "Download:", font = "Quicksand 12 bold")
    label_download_header.pack()
    label_download = tk.Label(frame, text = "Calculating...", font = "Quicksand 12")
    label_download.pack()

    #membuat function update
    def update():
        
        #membuat variabel global
        global last_upload, last_download, upload_speed, down_speed
        counter = net_io_counters()

        upload = counter.bytes_sent
        download = counter.bytes_recv
        total = upload + download

        #decision untuk tiap kondisi variabel setiap kali update
        if last_upload > 0:
            if upload < last_upload:
                upload_speed = 0
            else:
                upload_speed = upload - last_upload

        if last_download > 0:
            if download < last_download:
                down_speed = 0
            else:
                down_speed = download - last_download

        #update value dari tiap variabel setiap function update berjalan
        last_upload = upload
        last_download = download
        
        label_total_upload["text"] = f"{size(upload)}"
        label_total_download["text"] = f"{size(download)}"
        label_total_usage["text"] = f"{size(total)}\n"
        
        label_upload["text"] = size(upload_speed)
        label_download["text"] = size(down_speed)
        
        #menampilkan label
        label_total_upload.pack()
        label_total_download.pack()
        label_total_usage.pack()
        label_upload.pack()
        label_download.pack()
        
        #refresh window dengan function update
        window.after(REFRESH_DELAY, update)
    
    window.after(REFRESH_DELAY, update)
    
    #membuat button kembali dan keluar
    label_kosong = tk.Label(frame, text="").pack(pady=10)
    button_back = tk.Button(frame, text = 'Kembali', fg ='red', width='10', height='2',command=menu).pack(side=LEFT)
    button_quit = tk.Button(frame, text = 'Keluar', fg ='red', width='10', height='2',command=quit).pack(side=RIGHT)

    #infinite looping selama program berjalan / tidak dikeluarkan    
    window.mainloop()
    
#membuat function untuk speedtest    
def speedtestdef():
    
    #atur judul window
    window.title("Internet Speedtest")
    
    #menghapus widgets sebelumnya setelah update window
    for widgets in frame.winfo_children():
        widgets.destroy()
   
    #membuat function untuk check speed jaringan internet
    def check_speed():
        global up_speed, dl_speed, ping
        test = speedtest.Speedtest()
        
        upload = test.upload()
        download = test.download()
        
        dl_speed = round(download / (10 ** 6), 2)
        up_speed = round(upload / (10 ** 6), 2)
    
        servernames = []
        test.get_servers(servernames)
        ping = test.results.ping
        
    #membuat function untuk update text setelah di check speed
    def update_text():
        
        #membuat label judul program
        label_kosong = tk.Label(frame, text="").pack()
        label_judul = tk.Label(frame, text = "Internet Speedtest", font = "Quicksand 16 bold").pack(pady=5)
        label_kosong = tk.Label(frame, text="").pack() 
        
        #membuat thread untuk memanggil function check_speed()
        thread=threading.Thread(target=check_speed, args=())
        thread.start()        
        
        #membuat progressbar untuk menampilkan bar proses
        progress=Progressbar(frame, orient=HORIZONTAL, length=160, mode='determinate')
        progress.pack()
        progress.start()
        while thread.is_alive():
            window.update()
            pass
        
        #membuat label untuk PING
        ping_label_header = tk.Label(frame, text="PING : ", font = 'Quicksand 12 bold')
        ping_label_header.pack()
        ping_label = tk.Label(frame, text="Calculating...", font = 'Quicksand 12')
        ping_label.pack()
        label_kosong = tk.Label(frame, text="").pack()
        
        #membuat label untuk download
        down_label_header = tk.Label(frame, text="Download Speed : ", font = 'Quicksand 12 bold')
        down_label_header.pack()
        down_label = tk.Label(frame, text="Calculating...", font = 'Quicksand 12')
        down_label.pack()
        label_kosong = tk.Label(frame, text="").pack()
        
        #membuat label untuk upload
        up_label_header = tk.Label(frame, text="Upload Speed : ", font = 'Quicksand 12 bold')
        up_label_header.pack()
        up_label = tk.Label(frame, text="Calculating...", font = 'Quicksand 12')
        up_label.pack()
        label_kosong = tk.Label(frame, text="").pack()
        
        #update value pada label dengan data dari function check_speed()
        down_label.config(text = str(dl_speed)+" Mbps")
        up_label.config(text = str(up_speed)+" Mbps")
        ping_label.config(text = str(ping)+" ms")

        #menghapus progressbar
        progress.stop()
        progress.destroy()

    #menjalankan function update_text()
    update_text()
    
    #membuat button kembali dan keluar
    label_kosong = tk.Label(frame, text="", height='6').pack()
    button_back = tk.Button(frame, text = 'Kembali', fg ='red', width='10', height='2',command=menu).pack(side=LEFT)
    button_quit = tk.Button(frame, text = 'Keluar', fg ='red', width='10', height='2',command=quit).pack(side=RIGHT)
    
    #infinite looping selama program berjalan / tidak dikeluarkan
    window.mainloop()

#memanggil function menu()        
menu()

#infinite looping selama program berjalan / tidak dikeluarkan
window.mainloop()