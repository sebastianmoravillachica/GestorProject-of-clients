import unittest
import database as db
import copy
import helpers
import config
import csv


class TestData(unittest.TestCase):
    def setUp(self):
#Antes de ejecutar un prueba se le pasar por medio de una lista un serie de clientes
#|MOCKUP| Aprueba los clientes ingrasados
        db.Clientes.lista=[
            db.Cliente('13A','Marta','Sanchez'),
            db.Cliente('22E','Jose','Lopez'),
            db.Cliente('11O','Sebastian','Mora')
]   
    def test_buscar_cliente(self):
        cliente_existente=db.Clientes.buscar('13A')
        cliente_inexistente=db.Clientes.buscar('17B')
        
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)
    
    def test_crear_cliente(self):
        nuevo_cliente=db.Clientes.crear_cliente('34L','Alejandro','Cruz')
        self.assertEqual(len(db.Clientes.lista),4)
        self.assertEqual(nuevo_cliente.id,'34L')
        self.assertEqual(nuevo_cliente.nombre,'Alejandro')
        self.assertEqual(nuevo_cliente.apellido,'Cruz')
        
    def test_modificar_cliente(self):
            mod_cliente=copy.copy(db.Clientes.buscar('13A'))
            cliente_modificado=db.Clientes.modificar_cliente('13A','Maria','Sanchez')   
            self.assertEqual(mod_cliente.nombre,'Marta')
            self.assertEqual(cliente_modificado.nombre,'Maria')
    
    def test_eliminar_cliente(self):
        cliente_eli=db.Clientes.borrar_cliente('13A')
        cliente_rebuscado=db.Clientes.buscar('13A')
        
        self.assertEqual(cliente_eli.id,'13A')
        self.assertIsNone(cliente_rebuscado)
        
    def test_id_valido(self):
        self.assertTrue(helpers.id_valido('22P',db.Clientes.lista))
        self.assertFalse(helpers.id_valido('22Pfresdgwadscxfd',db.Clientes.lista))
        self.assertFalse(helpers.id_valido('P22',db.Clientes.lista))
        self.assertFalse(helpers.id_valido('22E',db.Clientes.lista))
        
    def test_escritura_csv(self):
        db.Clientes.borrar_cliente('13A')
        db.Clientes.borrar_cliente('22E')
        db.Clientes.modificar_cliente('11O','Claudio','Mora')
        
        id,nombre,apellido=None,None,None
        
        with open(config.DATABASE_PATH,newline='\n') as fichero:
            reader=csv.reader(fichero,delimiter=';')
            id,nombre,apellido=next(reader)
        
        self.assertEqual(id,'11O')
        self.assertEqual(nombre,'Claudio')
        self.assertEqual(apellido,'Mora')
