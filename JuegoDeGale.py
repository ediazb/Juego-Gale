from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
import random



class VentanaPlay():

    def __init__(self):

        #Para la jugada de la maquina:
        self.jugada = [-1,-1]

        #Opcion para la dificultad
        self.opcion = 0

        # Band para saber si se sigue jugando
        self.band = 0

        # Matriz para usar en Primero el Mejor
        self.matrizMAX = []
        for i in range (0,6):
            self.matrizMAX.append([])
            cont = 6+i
            for j in range ( 0,6):
                self.matrizMAX[i].append(cont)
                cont=cont-1

        # Matriz para usar en la búsqueda MiniMax
        self.matrizMIN = []
        for i in range (0,6):
            self.matrizMIN.append([])
            cont = 6+i
            for j in range ( 0,6):
                val = cont*(-1)
                self.matrizMIN[i].append(val)
                cont=cont-1


        self.all_buttons = []
        self.ventana = Tk()

        self.ventana.title('Juego de Gale')
        rwidth=self.ventana.winfo_screenwidth() - 75
        rheight=self.ventana.winfo_screenheight() - 75
        self.ventana.geometry(("%dx%d")%(rwidth,rheight))


        self.frame=Frame(self.ventana,bg="#666699")
        self.frame.pack(fill=BOTH,expand='yes')

        # Lado izquierdo
        self.frame1=Frame(self.frame)
        self.frame1.pack(side=LEFT,padx=100)

        # Lado derecho
        self.frame2=Frame(self.frame,bg="#666699")
        self.frame2.pack(side=RIGHT,padx=140)

        etiqueta3=Label(self.frame2,text="JUEGO DE GALE",font=("Negrita",30),bg="#666699",fg="#FFCC66")
        etiqueta3.pack(expand='no',side=TOP,fill=BOTH)

        etiqueta2=Label(self.frame2,text="NIVEL",font=("Comic Sans Ms",15),bg="#666699",fg="#FFCC66")
        etiqueta2.pack(padx=20,pady=20)


        global v 
        v=IntVar()
        self.r1=Radiobutton(self.frame2,text="Facil",variable=v,value=1,command=self.funcion)
        self.r2=Radiobutton(self.frame2,text="Intermedio",variable=v,value=2,command=self.funcion)
        self.r3=Radiobutton(self.frame2,text="Dificil",variable=v,value=3,command=self.funcion)
        self.r1.pack(padx=20,pady=20)
        self.r2.pack(padx=20,pady=20)
        self.r3.pack(padx=20,pady=20)
        
        self.combob2=Button(self.frame2,text="JUGAR",width=7, height=2,bg="#FFCC66",font=("",20),command=self.controller)
        self.combob2.pack(padx=20,pady=20,side=TOP)

        self.combob3=Button(self.frame2,text="REINICIAR JUEGO",width=17,height=2,bg="#FFCC66",font=("",20),command=self.controller)
        self.combob3.pack(padx=20,pady=20,side=TOP)

        self.combob4=Button(self.frame2,text="SALIR",width=7, height=2,bg="#FFCC66",font=("",20),command=self.ventana.destroy)
        self.combob4.pack(padx=20,pady=20,side=TOP)

    def funcion(self):
        if v.get()==1:
            self.opcion=1
            print("Selecciono nivel Facil")
        elif v.get()==2:
            self.opcion=2
            print("Selecciono nivel Intermedio")
        elif v.get()==3:
            self.opcion=3
            print("Selecciono nivel Dificil")
            
        
    
    # Funcion que inicializa la matriz, turno y pinta la matriz gráfica
    def controller(self):
        self.band = 1
        self.jugada = [-1,-1]
        messagebox.showinfo(title="Mensaje",message="Juego NUEVO")
        self.all_buttons = []
       
        # Humano:0 Maquina 1
        self.turno = 0
        
        self.matriz = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]
        self.creaMatriz()  
        for q in range(0,6):
            for w in range(0,6):
                self.all_buttons[q][w]['bg']='green'


    def run(self):
        self.ventana.mainloop()


    def creaMatriz(self):
        for i, row in enumerate(self.matriz):
            buttons_row = []
            for j, element in enumerate(row):
                boton =Button(self.frame1,width=10,height=5,bg='green',bd=5,command=lambda a=i,b=j: self.Juego(a,b))
                boton.grid(row=i, column=j,padx=5,pady=5)

                buttons_row.append( boton )

            self.all_buttons.append( buttons_row )

    def FinJuego(self):
        # En esta funcion debe estar El mensaje de Final de Juego y bloqueo de Matriz.
        if self.turno==0:
            messagebox.showinfo(message="GANASTE")
            print("GANASTE!")
        else:
            print("PERDISTE!")
            messagebox.showinfo(message="PERDISTE")
        messagebox.showinfo(message="FINALIZO EL JUEGO")
        self.band= 0
        
    def VoltearFicha(self,x,y):
        # Verde: 0 | Rojo: 1
        for q in [0,1,2,3,4,5]:
            if q>=x:
                for w in [0,1,2,3,4,5]:
                    if w<=y:
                        self.matriz[q][w]=1  # Voltear a 1 en la lista matriz
                        self.all_buttons[q][w]['bg']='red'  # Pinta la ficha en gráfico


        print( "Ficha Jugada: x=%s y=%s" % (x, y) )


    def CambioTurno(self):
        if self.band == 1:
            if self.turno==1:
                self.turno=0
                messagebox.showinfo(message="Turno:Humano")
            else:
                self.turno=1

    def Juego(self, x, y):
        if self.band == 1:
            
            self.combob2.config(state='disabled')
            if self.matriz[x][y] == 0:
                self.VoltearFicha(x,y)
                
                # Muestra la matriz en Consola
                for rec in [0,1,2,3,4,5]:
                    print (self.matriz[rec])


                # Condición de Parada
                if self.matriz[0][5]==1:
                    
                    self.FinJuego()
                    self.combob2.config(state='active')
                elif self.matriz[0][4]==1 & self.matriz[1][5]==1:
                    self.FinJuego()
                    self.combob2.config(state='active')
                else:
                    if self.turno == 0:                    
                        self.CambioTurno()
                        
                        messagebox.showinfo(message="Turno:Maquina")
                        print("********************************")
                        print("Juega la Máquina>>>>")
                        self.jugada = self.JuegoMaquina(self.opcion)
                        self.Juego(self.jugada[0],self.jugada[1])
                        self.CambioTurno()

            else:
             print("Ficha ya jugada!")
             messagebox.showinfo(message="FICHA YA JUGADA")


    def CalcularPosiblesJugadas(self):
        aux = []
        for m in range(0,6):
            for n in range(0,6):
                if self.matriz[m][n]==0:
                    aux.append([m,n])
        aux.remove([0,5])
        return aux

    def BusquedaAleatoria(self,listaposibles):
        jugada = []
        tam = len(listaposibles)
        ram = random.randrange(tam)
        jugada = listaposibles[ram] 
        return jugada


    def Mayor(self,lista):
        may = -99999
        pos = -1
        valIguales =[]  # Lista para valores repetidos al comparar
        for j in range(len(lista)):  
            if(lista[j]>may):  
                may=lista[j]  
                pos = j
        for l in range(len(lista)):
            if (may == lista[l]):
                valIguales.append(l)
        print("El mayor es: "+str(may))  
        if len(valIguales)>1:
            pos = random.randrange(len(valIguales))
        return pos

    def ValorMenor(self,lista):
        men = 99999
        for j in range(len(lista)):  
            if(lista[j]<men):  
                men=lista[j]  
        return men

    def JuegoMaquina(self,opcion):
        posiciones = []
        posiciones = self.CalcularPosiblesJugadas()
        print("Lista de Posibles Jugadas:")
        print(posiciones)

        # Nivel de Dificultad: Fácil ALEATORIO
        if opcion==1:
            nuevajugada = self.BusquedaAleatoria(posiciones)    
                    
        # Nivel de Dificultad: Intermedio PRIMERO EL MEJOR
        elif opcion==2:
            #NUEVA LISTA CON VALORES SEGUN FUCION DE EVALUACION
            evaluacion = []  # Lista para valores de funcion evaluacion 
            
            tam = len(posiciones)

            # Inserta los valores resultantes de funcion evaluacion en una lista por cada posible jugada
            for q in range (0,tam):
                evaluacion.append(self.funcionevaluacion(posiciones[q],1,self.matriz))
            
            print("Valores de Nodos: ")
            print(evaluacion)

            # Posicion del Mayor en la lista de valores evaluados
            pos = self.Mayor(evaluacion)

            # Almacena la nueva jugada
            nuevajugada = posiciones[pos]
            
        # Nivel de Dificultad: Difícil - MINIMAX
        elif opcion==3:
            capa1 = []
            # Crea los valores de funcion de evaluacion para la capa 1
            for i in range ( 0,len(posiciones)):
                capa1.append(self.minimax(posiciones[i]))

            #Elige el mayor (MAX)
            pos = self.Mayor(capa1)
            nuevajugada = posiciones[pos]

            print("Valores de Capa 1:")
            print(capa1)

        return nuevajugada


    def ActualizarMatriz(self,a,b,matriz):
        listamatriz = []
        listamatriz = [x[:] for x in matriz]
        for q in [0,1,2,3,4,5]:
            if q>=a:
                for w in [0,1,2,3,4,5]:
                    if w<=b:
                            listamatriz[q][w]=1
                            
                            
        return listamatriz

    def funcionevaluacion(self,posicion,tipo,matrizz):
        a = posicion[0]
        b = posicion[1]

        temporal = []
        temporal = [x[:] for x in matrizz]
        # Actualiza matriz con la posicion a analizar
        temporal = self.ActualizarMatriz(a,b,matrizz)

        evaluado = 0
        for m in range(0,6):
            for n in range(0,6):
                if temporal[m][n]==0:
                    if tipo==1:  # Para Primero el Mejor
                        evaluado = evaluado + self.matrizMAX[m][n]
                        if temporal[0][4]==1 & temporal[1][5]==1:
                            evaluado = 99999
                    else:  # Para el analisis de MiniMAX
                        evaluado = evaluado + self.matrizMIN[m][n]
                        if temporal[0][4]==1 & temporal[1][5]==1:
                            evaluado = -99999
        return evaluado

    def minimax(self,posicion):
        x = posicion[0]
        y = posicion[1]

        temporal = []
        temporal = [x[:] for x in self.matriz]
        # Actualiza matriz con la posicion a analizar
        temporal = self.ActualizarMatriz(x,y,self.matriz)

        capa2pos = []
        
        for m in range(0,6):
            for n in range(0,6):
                if temporal[m][n]==0:
                    capa2pos.append([m,n])
                        
        capa2pos.remove([0,5])

        capa2eval = []
        for i in range(0,len(capa2pos)):
            capa2eval.append(self.funcionevaluacion(capa2pos[i],2,temporal))
        valor = self.ValorMenor(capa2eval)
        
        return valor


VentanaPlay().run()
