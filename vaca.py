#cosas que corregir
    #si la primera es bomba cambiarla por otra que no lo sea
    #volver a crear un tablero con el boton o retornar al mismo si es desde un fichero
    #pasarlo todo a event box


#*****IMPORTACIONES NECESARIAS*******

import pygtk
pygtk.require('2.0')
import gtk
import random
#from random import randint
import time
import gobject
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
            pass
            
        elif self.cerrada == True:
            
            if self.detras == True:
                self.boton.get_image().set_from_pixbuf(self.imagenes[12])
                #Ventana_Perdido()
                self.cerrada = False
                #sacar ventana de has perdido
            else:
                self.boton.get_image().set_from_pixbuf(self.imagenes[self.bombas_alrededor])
                self.cerrada = False

    def actualizar(self,widget=None):
        #print "minas alrededor actualizadas" + " " + self.bombas_alrededor

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
    def __init__(self,filas,columnas,bombas,frase, widget = None):
        self.imagenes = self.imagenes_importadas()
        self.tabla = [[ Celda(self.crear_boton(),self.imagenes) for i in range (columnas)]for j in range (filas)]
        self.cant_bombas = bombas
        self.bombas_restantes = bombas
        self.filas = filas
        self.columnas = columnas
        self.frase = frase
        self.tpo0 = 0
        self.timer = 0
        self.etq_tpo = gtk.Label(' ')
    def imagenes_importadas(self):
        lista = []
        fotos= ["xcelda_cerrada.png","xcelda_marcada.png","xcelda_marcada_error.png","xcelda_question.png","xcelda_mina.png","xcelda_boom.png"]
        
        for i in range(7):
            lista.append(gtk.gdk.pixbuf_new_from_file("xcelda_" + str(i)+".png")) #0
            
        for i in range(len(fotos)):
            lista.append(gtk.gdk.pixbuf_new_from_file(fotos[i]))
        
        return lista
    def click(self):
        dt = int(time.time() - self.tpo0)
        self.etq_tpo.set_label("{0:02}:{1:02}".format(dt/60,dt%60))
        return dt
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
        if event.button == 1:    
            self.frase.set_text(' ')
            if self.tabla[i][j].marcada:
                self.frase.set_text('no se puede abrir una celda marcada')
            else:
                if self.tabla[i][j].bombas_alrededor == 0:
                    self.abrir_alrededor(i,j)
                self.tabla[i][j].abrir()
                if self.comprobar_final():
                
                    self.tablero_final()
                    pass
        

        if event.button == 3:
            self.frase.set_text(' ')
            if not self.tabla[i][j].cerrada:
                self.frase.set_text('esa celda no se puede marcar, esta ya abierta')
            else:
                self.tabla[i][j].marcada = not self.tabla[i][j].marcada
                if self.comprobar_final():
                
                    self.tablero_final()
                    pass
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
        if self.comprobar_final():
                    self.tablero_final()
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
                
                if (self.tabla[i][j].detras and not self.tabla[i][j].marcada):
                    return False
        return True
    def todo_abierto(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if (self.tabla[i][j].cerrada and not self.tabla[i][j].detras):
                    return False
        return True
    def comprobar_final(self):
        #cambiar label
        if self.todo_abierto():
            self.frase.set_text('todas las casillas abiertas, ha ganado')
            return True
        if self.todo_marcado():
            self.frase.set_text('todas las casillas con bomba marcadas,ha ganado, ha ganado')
            return True
        for i in range(self.filas):
            for j in range(self.columnas):
                if (not self.tabla[i][j].cerrada) and self.tabla[i][j].detras:
                    self.frase.set_text('ha abierto una casilla con bomba, ha perdido')
                    return True
        
    def tablero_final(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tabla[i][j].marcada and self.tabla[i][j].detras:
                    pass
                elif  not self.tabla[i][j].cerrada and self.tabla[i][j].detras:
                    self.tabla[i][j].boton.get_image().set_from_pixbuf(self.imagenes[12])
                elif self.tabla[i][j].detras:
                    self.tabla[i][j].boton.get_image().set_from_pixbuf(self.imagenes[11])
                else:
                    self.tabla[i][j].boton.get_image().set_from_pixbuf(self.imagenes[0])

        if self.timer != None:
            gobject.source_remove(self.timer)
            self.timer = None
    def ntablero(self,widget,fichero):
        if fichero:
            for i in range(self.filas):
                for j in range(self.columnas):
                    self.tabla[i][j].marcada = False
                    self.tabla[i][j].cerrada = True
                    self.tabla[i][j].boton.get_image().set_from_pixbuf(self.imagenes[7])
        else:
             for i in range(self.filas):
                for j in range(self.columnas):
                    self.tabla[i][j].marcada = False
                    self.tabla[i][j].cerrada = True
                    self.tabla[i][j].detras = False
                    self.tabla[i][j].boton.get_image().set_from_pixbuf(self.imagenes[7])
             self.rellenar_bombas()
             for i in range(self.filas):
                for j in range(self.columnas):
                    self.bombas_alrededor(i,j)
class Buscaminas:
    def __init__(self):
        self.menu = self.menu()
        self.ventana_juego = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.fin = self.fin_juego()
        self.tabla = None
        self.Frase=gtk.Label(' ')
        
    def menu(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Menu principal")
        window.set_border_width(10)
        window.set_size_request(200,275)
        window.connect("delete_event",self.delete_event)   #Cierra el programa si se pulsa la cruz del marco
        window.connect("destroy", self.destroy)
        tabla=gtk.Table()
        dificultad=gtk.Label("BUSCAMINAS")
        tabla.attach(dificultad,0,3,0,1)
        dificultad.show()
        
        button=gtk.Button("Principiante (9x9, 10 minas)")
        button.connect("clicked",self.rellenar_ventana,9,9,10)
        tabla.attach(button,0,1,1,2)
        button.show()
        
        button=gtk.Button("Intermedio (16x16, 40 minas)")
        button.connect("clicked",self.rellenar_ventana,16,16,40)
        tabla.attach(button,0,1,2,3)
        button.show()
        
        button=gtk.Button("Experto (16x30, 99 minas)")
        button.connect("clicked",self.rellenar_ventana,16,30,99)
        tabla.attach(button,0,1,3,4)
        button.show()
        
        button=gtk.Button("Leer de fichero")
        button.connect("clicked",self.elegir_Fichero) #implementar mas adelante
        tabla.attach(button,0,1,4,5)
        button.show()
        
        button=gtk.Button("Salir")
        button.connect("clicked",self.delete_event, None)
        button.connect_object("clicked",gtk.Widget.destroy, window)
        tabla.attach(button,0,1,5,6)
        button.show()
        window.add(tabla)
        window.show()
        tabla.show()

        return window

    def rellenar_ventana(self,widget,filas,columnas,bombas,fichero=None):

        self.Frase.set_text(' ')
        self.menu.hide()
        if fichero == None:
            self.tabla = Tablero(filas,columnas,bombas,self.Frase) if fichero == None else self.abrir_fichero(fichero)
            a = False
        else:
            self.tabla = self.abrir_fichero(fichero)
            a = True
        #tiempo
        self.tabla.tpo0 = time.time()
        self.tabla.timer = gobject.timeout_add(1000, self.tabla.click)
        ancho = self.tabla.columnas*24
        alto = self.tabla.filas*24
        
        self.ventana_juego.set_title("Buscaminas")
        self.ventana_juego.set_border_width(20)
        self.ventana_juego.set_size_request(ancho,alto)
        self.ventana_juego.connect("delete_event",self.cerrar_ventjuego)
        #self.ventana_juego.connect("destroy",)

        self.tabla.rellenar_bombas()

        
        #rellenar por primera vez las minas de alrededor
        for i in range(self.tabla.filas):
            for j in range(self.tabla.columnas):
                self.tabla.bombas_alrededor(i,j)

         # Create a Fixed Container
        fixed = gtk.Fixed()
        self.ventana_juego.add(fixed)
        fixed.show()

        for i in range(self.tabla.columnas):
            for j in range(self.tabla.filas):
                if j%2==True:
                    fixed.put(self.tabla.tabla[j][i].boton, i*19, j*19)                    
                else:
                    fixed.put(self.tabla.tabla[j][i].boton, i*19+9, j*19)
        
        
        self.Frase.show()
        fixed.put(self.Frase,self.tabla.columnas,self.tabla.filas*19+30)
        
        button=gtk.Button("Salir")
        button.connect("clicked",self.cerrar_ventjuego)
        fixed.put(button,self.tabla.columnas,self.tabla.filas*19+40)
        button.show()
        button=gtk.Button("Actualizar")
        button.connect("clicked",self.tabla.ntablero,a)
        fixed.put(button,self.tabla.columnas+60,self.tabla.filas*19+40)
        button.show()
        self.tabla.etq_tpo.show()
        fixed.put(self.tabla.etq_tpo,self.tabla.columnas+150,self.tabla.filas*19+45)
        self.ventana_juego.show()
        
    
    def abrir_fichero (self,nomfich):
        fich = open(nomfich)
        a = fich.readline()
        [fila,columna]= a.split(' ')
        fich.close()
        fich = open(nomfich)
        hola = fich.read()
        txt = hola.split('\n')
        fich.close()
        [nf,nc] = map(int, txt[0].split(' '))
        posicion_bombas = [(f,c) for (f,lin) in zip(range(nf),txt[1:])
            for (c,ch) in zip(range(nc),lin)
            if ch == "*"]
        t = Tablero(int(fila),int(columna),0,self.Frase)
        for i in range(len(posicion_bombas)):
            t.tabla[posicion_bombas[i][0]][posicion_bombas[i][1]].detras = True
        return t

    def fin_juego(self):
        pass
    def reiniciar_tablero(self,widget):
        pass
    #eventos salida programa
    def delete_event(self,widget,event,data=None):
        gtk.main_quit()
        return False
    def destroy(self, widget, data=None):
        gtk.main_quit()
    def cerrar_ventjuego(self,widget,data = None):
        self.ventana_juego.hide()
        self.menu.show()
    def elegir_Fichero(self,widget=None):
        dlg = gtk.FileChooserDialog("Abrir fichero",self.menu,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        if dlg.run() == gtk.RESPONSE_OK:
            nombre = dlg.get_filename()
        else:
            nombre = None
        print nombre
        
        dlg.destroy()
        self.rellenar_ventana(None,0,0,0,nombre)
        
    

def main():
    gtk.main()
    return 0

if __name__=="__main__":
    jugar = Buscaminas()
    jugar.menu.show()
    main()