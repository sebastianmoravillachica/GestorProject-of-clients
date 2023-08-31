#Controlara los datos y tendra el CREAR,MODIFICAR Y BORRAR la informacion
#Donde se crean los clientes
import csv
import config
class Cliente:
    def __init__(self,id,nombre,apellido):
        self.id=id
        self.nombre=nombre
        self.apellido=apellido
    def __str__(self):
        return f"({self.id}){self.nombre}{self.apellido}"    
#Donde se almacenan los clientes     
class Clientes:
    
    lista=[]
    with open(config.DATABASE_PATH,newline='\n') as fichero:
        reader=csv.reader(fichero,delimiter=';')
        for id,nombre,apellido in reader:
            cliente=Cliente(id,nombre,apellido)
            lista.append(cliente)
    #En el metodo estatico permite tomar solo el resultado de las funciones sin necesidad de llamar a la funcion
    #Metodo estatico
    @staticmethod
    
    #Recorre la lista para buscar un en especifico
    
    def buscar(id):
        for cliente in  Clientes.lista:
            if cliente.id == id:
                return cliente
            
    @staticmethod
    def crear_cliente(id,nombre,apellido):
        cliente=Cliente(id,nombre,apellido)
        Clientes.lista.append(cliente) 
        Clientes.guardar_cliente()
        return cliente
    
    @staticmethod
    def modificar_cliente(id,nombre,apellido):
        #Se recorre pero enumerado para recivir los indices
        for indice,cliente in  enumerate(Clientes.lista):
            if cliente.id == id:
                #Hace referencia al indice y la posicion
                Clientes.lista[indice].nombre=nombre
                Clientes.lista[indice].apellido=apellido
                #Nos devuelve la posicion del cliente
                Clientes.guardar_cliente()
                return Clientes.lista[indice]
            
    @staticmethod
    def borrar_cliente(id):
        for indice,cliente in enumerate(Clientes.lista):     
                if cliente.id == id:
                    cliente=Clientes.lista.pop(indice)
                    Clientes.guardar_cliente() 
                    return cliente
    @staticmethod
    def guardar_cliente():
        with open(config.DATABASE_PATH,'w',newline='\n') as fichero:
            writer=csv.writer(fichero,delimiter=';')
            for cliente in Clientes.lista:
                writer.writerow((cliente.id,cliente.nombre,cliente.apellido))