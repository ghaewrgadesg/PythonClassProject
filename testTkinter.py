from tkinter import *


def Scankey(event):
	
	val = event.widget.get()
	print(val)
	

	if val == '':
		data = list
	else:
		data = []
		for item in list:
			if val.lower() in item.lower():
				data.append(item)				

	
	Update(data)


def Update(data):
	

	listbox.delete(0, 'end')

	# put new data
	for item in data:
		listbox.insert('end', item)



list = ('C','C++','Java',
	'Python','Perl',
	'PHP','ASP','JS' )

ws = Tk()


entry = Entry(ws)
entry.pack()
entry.bind('<KeyRelease>', Scankey)


listbox = Listbox(ws)
listbox.pack()
Update(list)

ws.mainloop()
