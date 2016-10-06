# -*- coding: utf-8 -*-
import Tkinter as tk
import threading
import matplotlib.pyplot as plt
import serial
import time
import xlwt
import numpy as np
from PIL import Image


class App(threading.Thread):
    
    stop = 1

    def __init__(self):
        
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        label = tk.Button(self.root, text="Parar/Mostrar Dados",
                          command = self.stop)
        label.pack()

        label2 = tk.Button(self.root, text="Mostrar Pisada",
                          command = self.pisada)
        label2.pack()

        self.root.mainloop()

    def stop(self):
        self.stop = 0

    def pisada(self):
        self.pisadas = ["Pronada.jpg", "Neutra.jpg", "Supinada.jpg"]
        self.MedS1 = np.sum(pie1)/len(pie1)
        self.MedS2 = np.sum(pie2)/len(pie2)
        self.MedS3 = np.sum(pie3)/len(pie3)
        self.MedS4 = np.sum(pie4)/len(pie4)
            
        if((self.MedS1+self.MedS2) < (self.MedS3+self.MedS4)):
            img = Image.open(self.pisadas[0])
            img.show()
            
        if((self.MedS1+self.MedS4)/(self.MedS2+self.MedS3) <= 1):
            img = Image.open(self.pisadas[1])
            img.show()

        if((self.MedS2 + self.MedS3) < (self.MedS1 + self.MedS4)):
            img = Image.open(self.pisadas[2])
            img.show()


        else:
           print "Preciso de mais informações!"
           
            
        


app = App()

# Definindo planilha
wb = xlwt.Workbook()
ws = wb.add_sheet('Sequencias')

# Títulos das colunas
titles = ['Tempo','Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4']

# Escrevendo títulos na primeira linha do arquivo
for i in range(len(titles)):
    ws.col(i).width = 3500
    ws.write(0, i, titles[i])


i = 1
ser = 0
count = 0
tempo = []
pie1 = [] #Sensor 1
pie2 = [] #Sensor 2
pie3 = [] #Sensor 3
pie4 = [] #Sensor 4

#Função que escreve os dados na planilha
def plan_write(ct, sen1, sen2, sen3, sen4, i):
    ws.write(i, 0, ct)
    ws.write(i, 1, sen1)
    ws.write(i, 2, sen2)
    ws.write(i, 3, sen3)
    ws.write(i, 4, sen4)
#//////////////////////Fim da função//////////////////////////

#Função que inicia a comunicação serial
def init_serial():
    global ser          
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = "/dev/ttyACM2"   #COM Port
    

    #Especifica o timeout
    ser.timeout = 10
    ser.open()          #Abre SerialPort

    # print port open ou closed
    if ser.isOpen():
        print 'Open: ' + ser.portstr
#//////////////////////Fim da função//////////////////////////
        

#Chama a função init_serial(), começo do main()
init_serial()
time.sleep(1)


try:
    valor = ser.readline()  #Lê a porta serial
    
    SepVal = valor.split("+") #Separa a string valor pelo marcador '+'
    
    t0 = time.time() #Registra o t0

    #Aloca memória e salva os novos valores
    tempo.insert(count, 0)
    pie1.insert(count, float(SepVal[0]))
    pie2.insert(count, float(SepVal[1]))
    pie3.insert(count, float(SepVal[2]))
    pie4.insert(count, float(SepVal[3]))

    #Chama a função que escreve na planilha
    plan_write(0, SepVal[0], SepVal[1], SepVal[2], SepVal[3], i)
    
    count += 1
    i += 1
    
    while app.stop:
        valor = ser.readline()
            
        SepVal = valor.split("+") #Separa a string valor pelo marcador '+'
            
        dt = time.time() - t0   #Calcua o dt

        #Aloca memória e salva novos valores
        tempo.insert(count, dt)
        pie1.insert(count, float(SepVal[0]))
        pie2.insert(count, float(SepVal[1]))
        pie3.insert(count, float(SepVal[2]))
        pie4.insert(count, float(SepVal[3]))

        #Chama a função que escreve a planilha
        plan_write(dt, SepVal[0], SepVal[1], SepVal[2], SepVal[3], i)
            
        count += 1
        i += 1
            
        #print SepVal

    #Plota o gráfico de cada sensor
    plt.plot(tempo,pie1, label= "Sensor 1")
    plt.plot(tempo,pie2, label= "Sensor 2")
    plt.plot(tempo,pie3, label= "Sensor 3")
    plt.plot(tempo,pie4, label= "Sensor 4")
    plt.legend(loc = 4)

    wb.save('Biometria.xls') #Salva a planilha 
        
    plt.show()  #Mostra o gráfico de cada sensor

        
    print "Programa encerrado!"
            

except KeyboardInterrupt:

    #Plota o gráfico de cada sensor
    plt.plot(tempo,pie1)
    plt.plot(tempo,pie2)
    plt.plot(tempo,pie3)
    plt.plot(tempo,pie4)

    wb.save('Biometria.xls') #Salva a planilha 
    
    plt.show()  #Mostra o gráfico de cada sensor

    
    print "Programa encerrado!"


