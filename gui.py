import tkinter as tk
from scan import scan_host

WIDTH = 500
HEIGHT = 250

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.grid()

        self.host_entry = tk.Entry(self.master)
        self.port_entry = tk.Entry(self.master)


        self.create_widgets()

    def create_widgets(self):

        #Host/network selection
        self.host_label = tk.Label(self.master, text = "Host: ")
        self.host_label.grid(row=0, column=0)

        self.host = tk.StringVar()
        self.host_entry["textvariable"] = self.host
        self.host_entry.grid(row=0, column=1)
        # self.host_entry.bind('<Key-Return>',
        #                       self.print_contents)

        self.tcp_udp = tk.IntVar()
        tk.Checkbutton(self.master, text="UDP", variable=self.tcp_udp).grid(row=3, column=0)


                        
        #Port selection
        self.port_label = tk.Label(self.master, text = "Port: ")
        self.port_label.grid(row=0, column=3, columnspan=1)
        
        self.port = tk.StringVar()
        self.port_entry["textvariable"] = self.port
        self.port_entry.grid(row=0, column=4)
        # self.port_entry.bind('<Key-Return>',
        #                       self.print_contents)


        self.scan = tk.Button(self.master, text="Scan", fg="black",
                              command=self.start_scan)
        self.scan.grid(row=5, column=0)       

        self.quit = tk.Button(self.master, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=5, column=2)

    def start_scan(self):
        # print(self.tcp_udp.get())
        scan_host(self.host.get(), self.port.get(), self.tcp_udp.get())

root = tk.Tk()
app = Application(master=root)
app.mainloop()
