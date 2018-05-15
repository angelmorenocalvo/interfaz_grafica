#*****IMPORTACIONES NECESARIAS*******

import pygtk
pygtk.require('2.0')
import gtk

from random import randint
from time import time


#********OBJETOS*********

class Celda: #Para mas adelante
    def __init__(self, button, i, j):
        self.i = i
        self.j = j
        self.button = button
        self.mina = False
        self.abierta = False
        self.marcada= False
        
class Buscaminas:
    def __init__(self):
        
        #******LISTA DE IMAGENES********
        
        self.imagenes=[]
        fotos= ["xcelda_cerrada.png","xcelda_marcada.png","xcelda_marcada_error.png","xcelda_question.png","xcelda_mina.png","xcelda_boom.png"]
        
        for i in range(7):
            self.imagenes.append(gtk.gdk.pixbuf_new_from_file("xcelda_" + str(i)+".png")) #0
            
        for i in range(len(fotos)):
            self.imagenes.append(gtk.gdk.pixbuf_new_from_file(fotos[i]))
        #******SELECCION DE DIFICULTAD********
        
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Menu principal")
        self.window.set_border_width(10)
        self.window.set_size_request(200,275)
        self.window.connect("delete_event",self.delete_event)   #Cierra el programa si se pulsa la cruz del marco
        
        tabla=gtk.Table()
        dificultad=gtk.Label("BUSCAMINAS")
        tabla.attach(dificultad,0,3,0,1)
        dificultad.show()
        
        self.button=gtk.Button("Principiante (9x9, 10 minas)")
        self.button.connect("clicked",self.CrearTablero,9,9,10,350,410)
        tabla.attach(self.button,0,1,1,2)
        self.button.show()
        
        self.button=gtk.Button("Intermedio (16x16, 40 minas)")
        self.button.connect("clicked",self.CrearTablero,16,16,40,550,625)
        tabla.attach(self.button,0,1,2,3)
        self.button.show()
        
        self.button=gtk.Button("Experto (16x30, 99 minas)")
        self.button.connect("clicked",self.CrearTablero,30,16,99,1000,625)
        tabla.attach(self.button,0,1,3,4)
        self.button.show()
        
        self.button=gtk.Button("Leer de fichero")
        #self.button.connect("clicked",self.CrearTablero,9,9,10) implementar mas adelante
        tabla.attach(self.button,0,1,4,5)
        self.button.show()
        
        self.button=gtk.Button("Salir")
        self.button.connect("clicked",self.delete_event, None)
        tabla.attach(self.button,0,1,5,6)
        self.button.show()
        
        self.window.add(tabla)
        tabla.show()
        self.window.show()
        
        
#*********EVENTOS*********
    
    def delete_event(self,widget,event,data=None):
        gtk.main_quit()
        return False
    def destroy(self, widget, data=None):
        gtk.main_quit()
       
       
#********FUNCIONES*********
    
    def CrearTablero(self,widget,filas,columnas,minas, ancho, alto):
        self.window.hide()

        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Buscaminas")
        self.window.set_border_width(20)
        self.window.set_size_request(ancho,alto)

        self.window.connect("delete_event",self.delete_event)

        table=gtk.Table(filas+1,columnas) #filas +1 por el boton de quit
        self.window.add(table)
        
        #*******GENERANDO EL TABLERO CON MINAS*********
        
        contadorminas=0
        matrizgeneradora=[]
        
        while contadorminas!=minas:
            #matrizgeneradora=[]
            contadorminas=0
            for i in range(filas):
                matrizgeneradora.append([])
                for j in range (columnas):
                    aux = randint(0,filas*columnas)
                    if aux<=(minas):
                        matrizgeneradora[i].append(1)
                        contadorminas= contadorminas +1
                    else:
                        matrizgeneradora[i].append(0)
        
        matrizbotones=[]
        for i in range(filas):
            matrizbotones.append([])
            for j in range(columnas):
                
                self.button=gtk.Button(None)
                table.attach(self.button,i,i+1,j,j+1)
                self.button.set_image(gtk.Image())
                self.button.set_relief(gtk.RELIEF_NONE)
                self.button.get_image().set_from_pixbuf(self.imagenes[0])
                self.button.show()
                c = Celda(self.button, i, j)
                
                if matrizgeneradora[i][j]==1:
                    c.mina=True
                matrizbotones[i].append(c)
                c.button.connect("clicked",self.Abrir,c)

        
        self.button=gtk.Button("Salir")
        self.button.connect("clicked", self.destroy)
        self.button.connect_object("clicked",gtk.Widget.destroy, self.window)
        table.attach(self.button,0,columnas+2,filas+2,filas+3)
        self.button.show()

        table.show()
        self.window.show()
       
    
    def Abrir(self,widget,celda):
        #mina=celda.mina() 
        if celda.mina==True:
            celda.button.get_image().set_from_pixbuf(self.imagenes[12])
            print "FIN DEL JUEGO "
            
            self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.window.set_title("Fin del juego")
            self.window.set_border_width(20)
            self.window.set_size_request(300,100)
            self.Final=gtk.Label("Fin del juego. Gracias por jugar") #Terminar esta parte
            FinalTab=gtk.Table(1,1)
            FinalTab.attach(self.Final,0,1,0,1)
            self.Final.show()
            FinalTab.show()
            self.window.add(FinalTab)
            self.window.show()

        else:
            celda.button.get_image().set_from_pixbuf(self.imagenes[0])
            print "Ok"
            

    def Cambio(self,widget,mina,button):
        if mina!=2:
            button.get_image().set_from_pixbuf(self.imagenes[0])
            print "Ok"
    
    
    
       
#********PROGRAMA PRINCIPAL*********
def main():
    gtk.main()
    return 0

if __name__=="__main__":
    Buscaminas()
    main()
