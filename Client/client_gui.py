import tkinter

serverData = {}
ready = False
exited = False
m = tkinter.Tk()
m.title('Yeet')
tkinter.Label(m, text='IP').grid(row=0)
tkinter.Label(m, text='Port').grid(row=1)
e1 = tkinter.Entry(m)
e2 = tkinter.Entry(m)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e1.insert(0, '')
e2.insert(0, '9999')
var1 = tkinter.IntVar()
tkinter.Checkbutton(m, text='Debug', variable=var1).grid(row=2, column=1)


def startServer():
    global serverData, e1, e2, var1, ready, m
    serverData = {
        'ip': e1.get(),
        'port': int(e2.get()),
        'debug': var1.get() == 1
    }
    ready = True
    m.destroy()


def exit_me():
    global exited, m
    exited = True
    m.destroy()


tkinter.Button(m, text='Start Server', width=25, command=startServer).grid(row=3, column=1)
tkinter.Button(m, text='Exit', width=25, command=exit_me).grid(row=3, column=0)

m.mainloop()
