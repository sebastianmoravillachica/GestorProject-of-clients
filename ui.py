import database  as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel,WARNING 
import helpers

#Se usa esta clase para poder centrar lo demas
class centeWidgetMixin:
    def centrar(self):
        self.update()
        w=self.winfo_width()
        h=self.winfo_height()
        ws=self.winfo_screenwidth()
        hs=self.winfo_screenheight()
        #Se encuntra el punto central
        x=int(ws/2 - w/2)
        y=int(hs/2 - h/2)
        
        #WIDTHxHEIGHT+OFFESET_X+OFFSET_Y
        self.geometry(f"{w}x{h}+{x}+{y}") 
class creatClientWindow(Toplevel,centeWidgetMixin):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Crear cliente")
        self.build()
        self.centrar()
        self.transient(parent)
        self.grab_set()
    def build(self):
        frame=Frame(self)
        frame.pack(padx=20,pady=10)
        Label(frame,text="ID(2 ints y 1 char)").grid(row=0,column=0)   
        Label(frame,text="Nombre(de 2 a 30 chars)").grid(row=0,column=1)  
        Label(frame,text="Apellido(de 2 a 30 chars)").grid(row=0,column=2)  
        
        id=Entry(frame)
        id.grid(row=1,column=0)
        id.bind("<KeyRelease>",lambda event:self.validate(event,0))
        nombre=Entry(frame)
        nombre.grid(row=1,column=1)
        nombre.bind("<KeyRelease>",lambda event:self.validate(event,1))
        apellido=Entry(frame)
        apellido.grid(row=1,column=2)
        apellido.bind("<KeyRelease>",lambda event:self.validate(event,2))
        
        frame=Frame(self)
        frame.pack(pady=10)
        
        crear=Button(frame,text="Crear",command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0,column=0)
        Button(frame,text="Cancelar",command=self.close).grid(row=0,column=1,padx=10,pady=5)
        
        self.validaciones=[0,0,0]
        
        self.crear=crear
        
        self.id=id
        
        self.nombre=nombre
        
        self.apellido=apellido
        
    def create_client(self):
            self.master.treeview.insert(
                parent='',index='end',iid=self.id.get(),
                values=(self.id.get(),self.nombre.get(),self.apellido.get()))
            db.Clientes.crear_cliente(self.id.get(),self.nombre.get(),self.apellido.get())
            self.close()
            
    def close(self):
        self.destroy()
        self.update()
            
    def validate(self,event,index):
        valor=event.widget.get()
        valido=helpers.id_valido(valor,db.Clientes.lista) if index == 0 \
                                else(valor.isalpha() and len(valor)>=2 and len(valor)<=30)
        event.widget.configure({"bg":"Green" if valido else "Red"})  
        
        #Cambiar el estado del boton en base a las validaciones
        self.validaciones[index]=valido 
        self.crear.config(state=NORMAL if self.validaciones==[1,1,1] else DISABLED)                     

class EditClientWindow(Toplevel,centeWidgetMixin):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Modificar cliente")
        self.build()
        self.centrar()
        self.transient(parent)
        self.grab_set()
        
    def build(self):
        frame=Frame(self)
        frame.pack(padx=20,pady=10)
        Label(frame,text="ID(No editable)").grid(row=0,column=0)   
        Label(frame,text="Nombre(de 2 a 30 chars)").grid(row=0,column=1)  
        Label(frame,text="Apellido(de 2 a 30 chars)").grid(row=0,column=2)  
        
        id=Entry(frame)
        id.grid(row=1,column=0)
        nombre=Entry(frame)
        nombre.grid(row=1,column=1)
        nombre.bind("<KeyRelease>",lambda event:self.validate(event,0))
        apellido=Entry(frame)
        apellido.grid(row=1,column=2)
        apellido.bind("<KeyRelease>",lambda event:self.validate(event,1))
        
        cliente=self.master.treeview.focus()
        campos=self.master.treeview.item(cliente,'values')
        id.insert(0,campos[0])
        id.config(state=DISABLED)
        nombre.insert(0,campos[1])
        apellido.insert(0,campos[2])
        
        
        frame=Frame(self)
        frame.pack(pady=10)
        
        modificar=Button(frame,text="Modificar",command=self.edit_client)
        modificar.configure(state=DISABLED)
        modificar.grid(row=0,column=0)
        Button(frame,text="Cancelar",command=self.close).grid(row=0,column=1,padx=10,pady=5)
        
        self.validaciones=[1,1]
        
        self.modificar=modificar
        
        self.id=id
        
        self.nombre=nombre
        
        self.apellido=apellido
        
    def edit_client(self):
        cliente=self.master.treeview.focus()
        self.master.treeview.item(cliente,values=(self.id.get(),self.nombre.get(),self.apellido.get()))
        db.Clientes.modificar_cliente(self.id.get(),self.nombre.get(),self.apellido.get())
        
        self.close()
            
            
    def close(self):
        self.destroy()
        self.update()
            
    def validate(self,event,index):
        valor=event.widget.get()
        valido=(valor.isalpha() and len(valor)>=2 and len(valor)<=30)
        event.widget.configure({"bg":"Green" if valido else "Red"})  
        
        #Cambiar el estado del boton en base a las validaciones
        self.validaciones[index]=valido 
        self.modificar.config(state=NORMAL if self.validaciones==[1,1] else DISABLED)                     


class MainWindow(Tk,centeWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gester de clietes")
        self.build()
        self.centrar()
    
    #Counstruccion de lo visible
    def build(self):
        frame=Frame(self)
        frame.pack()
        
        treeview=ttk.Treeview(frame)
        treeview['columns']=('ID','Nombre','Apellido')
        
        
        treeview.column('#0',width=0,stretch=NO)
        treeview.column('ID',anchor=CENTER)
        treeview.column('Nombre',anchor=CENTER)
        treeview.column('Apellido',anchor=CENTER)
        
        treeview.heading('ID',text="ID",anchor=CENTER)
        treeview.heading('Nombre',text="Nombre",anchor=CENTER)
        treeview.heading('Apellido',text="Apellido",anchor=CENTER)
        
        scrollbar=Scrollbar(frame)
        scrollbar.pack(side="right",fill=Y)
        
        treeview['yscrollcommand']=scrollbar.set
        
        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='',index='end',iid=cliente.id,
                values=(cliente.id,cliente.nombre,cliente.apellido))
        treeview.pack()
        
        frame=Frame(self)
        frame.pack(padx=20,pady=25)  
        
        Button(frame,text="Crear",command=self.create).grid(row=0,column=0,padx=10,pady=5)  
        Button(frame,text="Modificar",command=self.edit).grid(row=0,column=1,padx=10,pady=5)
        Button(frame,text="Borrar",command=self.delete).grid(row=0,column=2,padx=10,pady=5)
        
        self.treeview=treeview
    def delete(self):
        #Recupera los datos
        cliente=self.treeview.focus()
        if cliente:
            campo=self.treeview.item(cliente,'values')
            confirmar=askokcancel(
                title="Confirmar borrado",
                message=f"¿Borrar a {campo[1]}{campo[2]}?",
                icon=WARNING 
            )
            if confirmar:
                self.treeview.delete(cliente)    
                db.Clientes.borrar_cliente(campo[0])
                
    def create(self):
        creatClientWindow(self)
    def edit(self):
        if self.treeview.focus():
            
            EditClientWindow(self)          