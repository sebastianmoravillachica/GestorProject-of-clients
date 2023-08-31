#Contendra la interfaz del proyecto
import os
import helpers
import database as db
def inciar():
    while True:
        helpers.limpiar_pantalla()
        
        print("###########################")
        print("        Bienvenido         ")
        print("###########################")
        print("   [1] Listar los clientes ")
        print("   [2] Buscar cliente      ")
        print("   [3] Añadir un cliente   ")
        print("   [4] Modificar un cliente")
        print("   [5] Borrar cliente      ")
        print("   [6] Cerrar aplicacion   ")
        print("###########################")

        opcion=input("> ")
        helpers.limpiar_pantalla()
        if opcion == "1":
            
            print("Listando los clientes.........\n")
            for cliente in db.Clientes.lista:
                print(cliente)
                
        elif opcion == "2":
            
            print("Buscandon cliente..........\n")
            id=helpers.leer_texto(3,3,"id (2 int y 1 char )").upper()
            cliente=db.Clientes.buscar(id)
            print(cliente)if cliente else print("Cliente no encontrado.")
            
        elif opcion == "3":
            
            print("Añadiendo cliente.........\n")
            id=None
            while True:
                id=helpers.leer_texto(3,3,"id (2 int y 1 char )").upper()
                if helpers.id_valido(id,db.Clientes.lista):
                        break
                    
            nombre=helpers.leer_texto(2,30,"Nombre (de 2 a 30 chars)").capitalize()
            apellido=helpers.leer_texto(2,30,"Apellido(de 2 a 30 chars)").capitalize()
            db.Clientes.crear_cliente(id,nombre,apellido)
            print("Cliente añadido correctamente")
            
        elif opcion == "4":
            
            print("Modificando cliente.........\n")
            id=helpers.leer_texto(3,3,"id (2 int y 1 char )").upper()
            cliente=db.Clientes.buscar(id)
            if cliente:
                nombre=helpers.leer_texto(2,30,f"Nombre (de 2 a 30 chars)[{cliente.nombre}]").capitalize()
                apellido=helpers.leer_texto(2,30,f"Apellido(de 2 a 30 chars)[{cliente.apellido}]").capitalize()
                db.Clientes.modificar_cliente(cliente.id,nombre,apellido)
                print("Cliente modificado correctamente.")
            else:
                print("Cliente no encontrado.")
            
        elif opcion == "5":
            
            print("Borrando cliente.........\n")
            id=helpers.leer_texto(3,3,"id (2 int y 1 char )").upper()
            print("Cliente borrado correctamente")if db.Clientes.borrar_cliente(id) else  print("Cliente no encontradoo")
            
            
            
        elif opcion == "6":
            print("Cerradon.........\n")  
            break
        input("\nPresione ENTER para continuar...")           
