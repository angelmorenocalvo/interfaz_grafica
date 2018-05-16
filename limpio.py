#cosas que corregir
    
    #recurisividad cuando abrimos una bomba, aunque en ese caso de igual porque mostramos tablero final
    #recursividad cuando hay celda marcada cerca que da error
    #no poder marcar una celda abierta
#*****IMPORTACIONES NECESARIAS*******

import pygtk
pygtk.require('2.0')
import gtk
import random
#from random import randint
from time import time
class Celda:
    def __init__(self,boton,imagenes,bomba= None):
        self.imagenes = imagenes
        self.boton = boton
        self.detras = bomba
        self.bombas_alrededor = 0
        self.marcada = False
        self.cerrada = True
        
    
    def abrir(self,widget=None):
        #abrir
        
        if self.marcada == True:
            print 'Accion no valida'
            
        elif self.cerrada == True:
            
            if self.detras == True:
                self.boton.get_image().set_from_pixbuf(self.imagenes[12])
                Ventana_Perdido()
                self.cerrada = False
                #sacar ventana de has perdido
            else:
                self.boton.get_image().set_from_pixbuf(self.imagenes[self.bombas_alrededor])
                self.cerrada = False

    def actualizar(self,widget=None):
        #print "minas alrededor actualizadas" + " " + self.bombas_alrededor
        print 'prueba'
        print self.bombas_alrededor
        if  not self.cerrada:
            if self.bombas_alrededor<0:
                self.boton.get_image().set_from_pixbuf(self.imagenes[10])
            else:
                self.boton.get_image().set_from_pixbuf(self.imagenes[self.bombas_alrededor])
        else:
            if self.marcada:
                self.boton.get_image().set_from_pixbuf(self.imagenes[8])
            else:
                self.boton.get_image().set_from_pixbuf(self.imagenes[7])
#************Tablero utilizado por detras***************
class Tablero:
    def __init__(self,filas,columnas,bombas,widget = None):
        self.imagenes = self.imagenes_importadas()
        self.tabla = [[ Celda(self.crear_boton(),self.imagenes) for i in range (columnas)]for j in range (filas)]
        self.cant_bombas = bombas
        self.bombas_restantes = bombas
        self.filas = filas
        self.columnas = columnas
        
    def imagenes_importadas(self):
        lista = []
        fotos= ["xcelda_cerrada.png","xcelda_marcada.png","xcelda_marcada_error.png","xcelda_question.png","xcelda_mina.png","xcelda_boom.png"]
        
        for i in range(7):
            lista.append(gtk.gdk.pixbuf_new_from_file("xcelda_" + str(i)+".png")) #0
            
        for i in range(len(fotos)):
            lista.append(gtk.gdk.pixbuf_new_from_file(fotos[i]))
        
        return lista
    
    def crear_boton(self):
        boton=gtk.Button()
        boton.set_image(gtk.Image())
        boton.set_relief(gtk.RELIEF_NONE)
        boton.get_image().set_from_pixbuf(self.imagenes[7])
        #boton.connect('clicked', self.movimiento,boton)
        boton.set_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK)
        boton.connect("button-release-event", self.movimiento,boton)
        boton.show()
        return boton

    def bombas_alrededor(self, fila, columna):

        contador = 0
        if fila%2 == 0:
            rango = [(-1, 1),(-1, 0),(0, -1),(0, 1),(1, 1),(1, 0)]#impar
            
        else:
            rango = [(-1, -1),(-1, 0),(0, -1),(0, 1),(1, -1),(1, 0)]#par
            
            
        for a in range(len(rango)):#len(rango)
            if not self.fuera_limites(fila + rango[a][0], columna + rango[a][1]):
                
                if self.tabla[fila + rango[a][0]][columna + rango[a][1]].detras == True:
                    contador+=1
                    
                if self.tabla[fila + rango[a][0]][columna + rango[a][1]].marcada == True:
                    contador-=1
        
        self.tabla[fila][columna].bombas_alrededor = contador
        
    def movimiento(self,widget,event, boton):
        i,j = self.posicion_boton(boton)
        if event.button == 1 and self.tabla[i][j].cerrada:
            if self.tabla[i][j].marcada == False:
                if self.tabla[i][j].bombas_alrededor == 0:
                    self.abrir_alrededor(i,j)
                self.tabla[i][j].abrir()
                
        if event.button == 3:
            self.tabla[i][j].marcada = not self.tabla[i][j].marcada
            if self.todo_marcado(): Ventana_Ganado()
            self.comprobar_alrededor(i,j)
            self.tabla[i][j].actualizar()
            
    def posicion_boton(self,boton):
        a=0
        
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tabla[i][j].boton == boton:
                    return [i,j]
    
    def rellenar_bombas(self):
        minasA = 0
        while(minasA<self.cant_bombas):
            for i in range(self.filas):
                    for j in range(self.columnas):
                        if minasA<self.cant_bombas:
                            a = random.randint(0,self.filas*self.columnas-1)
                            if a == 0:
                                if self.tabla[i][j].detras:
                                    minasA-=1
                                self.tabla[i][j].detras= True
                                minasA+=1
                            elif(self.tabla[i][j].detras != True):
                                self.tabla[i][j].detras= False
    
    def fuera_limites(self,fila,columna):
        return (fila<0 or fila > self.filas-1) or (columna < 0 or columna > self.columnas-1) 
    
    def abrir_alrededor(self,fila,columna):
        self.tabla[fila][columna].abrir()
        if self.tabla[fila][columna].bombas_alrededor == 0 and not self.tabla[fila][columna].detras: #or self.tabla[fila][columna].delante == '?':
            if fila%2 == 0:
                rango = [(-1, 1),(-1, 0),(0, -1),(0, 1),(1, 1),(1, 0)]#impar
            else:
                rango = [(-1, -1),(-1, 0),(0, -1),(0, 1),(1, -1),(1, 0)]#par
                
            for a in range(len(rango)):#len(rango)
                if not self.fuera_limites(fila + rango[a][0],columna + rango[a][1]):
                    if self.tabla[fila + rango[a][0]][columna + rango[a][1]].cerrada == True :
                        self.abrir_alrededor(fila + rango[a][0],columna + rango[a][1])
   
    def comprobar_alrededor(self,fila,columna):
        if fila%2 == 0:
            rango = [(-1, 1),(-1, 0),(0, -1),(0, 1),(1, 1),(1, 0)]#impar
        else:
            rango = [(-1, -1),(-1, 0),(0, -1),(0, 1),(1, -1),(1, 0)]#par        
        for a in range(len(rango)):#len(rango)
            if not self.fuera_limites(fila + rango[a][0],columna + rango[a][1]):
                if self.tabla[fila + rango[a][0]][columna + rango[a][1]].detras != True:
                    self.bombas_alrededor(fila + rango[a][0],columna + rango[a][1])
                if self.tabla[fila + rango[a][0]][columna + rango[a][1]].cerrada == False:
                    self.tabla[fila + rango[a][0]][columna + rango[a][1]].actualizar()
    
    def todo_marcado(self):
        contador = self.cant_bombas
        for i in range(self.filas):
            for j in range(self.columnas):
                #return ( False) if (self.tabla[i][j].detras and not self.tabla[i][j].marcada) else ( True)
                if (self.tabla[i][j].detras and not self.tabla[i][j].marcada):
                    contador-=0
                if contador != 0:
                    return False
        return True
class Buscaminas:
    def __init__(self,widget,filas,columnas,bombas):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.tabla = Tablero(filas,columnas,bombas)
        self.ventana_buscaminas(filas,columnas)


    def ventana_buscaminas(self,filas,columnas):
        ancho = self.tabla.columnas*24
        alto = self.tabla.filas*24
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Buscaminas")
        self.window.set_border_width(20)
        self.window.set_size_request(ancho,alto)
        self.window.connect("delete_event",self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.tabla.rellenar_bombas()

        
        for i in range(self.tabla.filas):
            contador = 0
            for j in range(self.tabla.columnas):
                contador+=1
                #self.tabla.tabla[i][j].bombas_alrededor= contador
                self.tabla.bombas_alrededor(i,j)
        #self.tabla.imprimir_bombas()
        
         # Create a Fixed Container
        self.fixed = gtk.Fixed()
        self.window.add(self.fixed)
        self.fixed.show()

        for i in range(self.tabla.columnas):
            for j in range(self.tabla.filas):
                if j%2==True:
                    self.fixed.put(self.tabla.tabla[j][i].boton, i*19, j*19)                    
                else:
                    self.fixed.put(self.tabla.tabla[j][i].boton, i*19+9, j*19)
        self.window.show()

    def delete_event(self,widget,event,data=None):
        self.window.hide()
        #gtk.main_quit()
        juego = Menu()
        juego.crear_menu()
        return False
    def destroy(self, widget, data=None):
        self.window.hide()
class Menu:
    def __init__(self):
         self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
         #self.ventana_juego = Buscaminas()
    
    def crear_menu(self):
        self.window.set_title("Menu principal")
        self.window.set_border_width(10)
        self.window.set_size_request(200,275)
        self.window.connect("delete_event",self.delete_event)   #Cierra el programa si se pulsa la cruz del marco
        self.window.connect("destroy", self.destroy)
        tabla=gtk.Table()
        dificultad=gtk.Label("BUSCAMINAS")
        tabla.attach(dificultad,0,3,0,1)
        dificultad.show()
        
        self.button=gtk.Button("Principiante (9x9, 10 minas)")
        self.button.connect("clicked",self.crear_buscaminas,9,9,10)
        tabla.attach(self.button,0,1,1,2)
        self.button.show()
        
        self.button=gtk.Button("Intermedio (16x16, 40 minas)")
        self.button.connect("clicked",self.crear_buscaminas,16,16,40)
        tabla.attach(self.button,0,1,2,3)
        self.button.show()
        
        self.button=gtk.Button("Experto (16x30, 99 minas)")
        self.button.connect("clicked",self.crear_buscaminas,16,30,99)
        tabla.attach(self.button,0,1,3,4)
        self.button.show()
        
        self.button=gtk.Button("Leer de fichero")
        #self.button.connect("clicked",self.delete_event) #implementar mas adelante
        tabla.attach(self.button,0,1,4,5)
        self.button.show()
        
        self.button=gtk.Button("Salir")
        self.button.connect("clicked",self.delete_event, None)
        self.button.connect_object("clicked",gtk.Widget.destroy, self.window)
        tabla.attach(self.button,0,1,5,6)
        self.button.show()
        self.window.add(tabla)
        self.window.show()
        tabla.show()
    def delete_event(self,widget,event,data=None):
        gtk.main_quit()
        return False
    
    def crear_buscaminas(self,widget,filas,columnas,bombas):
        self.window.hide()
        Buscaminas(widget,filas,columnas,bombas)

    def destroy(self, widget, data=None):
        gtk.main_quit()
    
class Ventana_Ganado:
    def __init__(self):
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.sacar_pantalla()
    def sacar_pantalla(self):
        self.window.set_title("WIN")
        self.window.set_border_width(20)
        self.window.set_size_request(300,100)
        self.mensaje=gtk.Label("ha ganado. Gracias por jugar") #Terminar esta parte
        WinTab=gtk.Table(1,1)
        WinTab.attach(self.mensaje,0,1,0,1)
        self.mensaje.show()
        WinTab.show()
        self.window.add(WinTab)
        self.window.show()
    def delete_event(self,widget,event,data=None):
        gtk.main_quit()
        return False
    def destroy(self, widget, data=None):
        gtk.main_quit()
class Ventana_Perdido:
    def __init__(self):
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.sacar_pantalla()
    def sacar_pantalla(self):
        self.window.set_title("Fin del juego")
        self.window.set_border_width(20)
        self.window.set_size_request(300,100)
        #self.window.connect("delete_event",self.delete_event)   #Cierra el programa si se pulsa la cruz del marco
        #self.window.connect("destroy", self.destroy)
        self.Final=gtk.Label("Fin del juego. Gracias por jugar") #Terminar esta parte
        FinalTab=gtk.Table(1,1)
        FinalTab.attach(self.Final,0,1,0,1)
        self.Final.show()
        FinalTab.show()
        self.window.add(FinalTab)
        self.window.show()
    def delete_event(self,widget,event,data=None):
        gtk.main_quit()
        return False
    def destroy(self, widget, data=None):
        gtk.main_quit()

        
        
    #*********EVENTOS*********
    '''
    def delete_event(self,widget,event,data=None):
        gtk.main_quit()
        return False
    def destroy(self, widget, data=None):
        gtk.main_quit()
    '''
#********PROGRAMA PRINCIPAL*********

def main():
    gtk.main()
    return 0

if __name__=="__main__":
    jugar = Menu()
    jugar.crear_menu()
    main()
