#!/usr/bin/python3

import serial               # Biblioteca serial para comunicação USB
import cv2                  # Biblioteca de visão computacional OpenCV2
import numpy as np          # Biblioteca de lgica númerica
from time import time,sleep # Biblioteca de tempo do sistema
from tracker import *       # Biblioteca desenvolvida para identificar e seguir os objetos
import threading            # Biblioteca utilizada para contagem de linhas tempo

'''
###################################
        Variáveis globais
###################################
'''

ContadorSaidas = 0              # Variável para contar os objetos verdes que passaram pela zona de detecção
ContadorSaidasGreen = 0         # Variável para contar os objetos vermelhos que passaram pela zona de detecção
AreaContornoLimiteMin = 30      # Valor da area mínima para detectar contorno
OffsetLinhaSaida = 60           # Valor para posicionar a linha de saída
AreaCount = 10                  # Valor em pixel da área para detectar o contorno
AreaMinY = 140                  # Determina a posição da linha que começa a detectar objeto
AreaMaxY = 310                  # Determina a posição da linha que deixa de detectar objetos
CoordenadaYLinhaSaida = 0       # Coordenada da linha que detecta objeto
CoordenadaXLeft = 0             # Coordenada da linha vertical esquerda que divide a seção 1 e 2
CoordenadaXCenter = 0           # Coordenada da linha vertical central que divide a seção 2 e 3
CoordenadaXRight = 0            # Coordenada da linha vertical direita que divide a seção 3 e 4
ContadorQuad1 = 0               # Variável para contagem de objetos VM da seção 1
ContadorQuad2 = 0               # Variável para contagem de objetos VM da seção 2
ContadorQuad3 = 0               # Variável para contagem de objetos VM da seção 3
ContadorQuad4 = 0               # Variável para contagem de objetos VM da seção 4
idTempQ1 = 65535                # Variável para guardar um ID detectado e contar apenas uma vez na seção 1
idTempQ2 = 65535                # Variável para guardar um ID detectado e contar apenas uma vez na seção 2
idTempQ3 = 65535                # Variável para guardar um ID detectado e contar apenas uma vez na seção 3
idTempQ4 = 65535                # Variável para guardar um ID detectado e contar apenas uma vez na seção 4
count_p = 0                     # Variável incremental para identificar disparos de tempo inícial e final

'''
###################################
        Funções Auxiliares
###################################
'''
    
# Função para verificar se o objeto está passando no quadrante 1 da linha de saída monitorada
def TestaQuad1(idQ1,y, c_y_out):
    global idTempQ1

    DiferencaAbsoluta = abs(y - c_y_out)
    if(DiferencaAbsoluta <= AreaCount):
        if idQ1 != idTempQ1:
            idTempQ1 = idQ1
            return 1
        else:
            return 0
    else:
        return 0

# Função para verificar se o objeto está passando no quadrante 2 da linha de saída monitorada
def TestaQuad2(idQ2,y, c_y_out):
    global idTempQ2
    DiferencaAbsoluta = abs(y - c_y_out)
    if (DiferencaAbsoluta <= AreaCount):
        if idQ2 != idTempQ2:
            idTempQ2 = idQ2
            return 1
        else:
            return 0
    else:
        return 0

# Função para verificar se o objeto está passando no quadrante 3 da linha de saída monitorada
def TestaQuad3(idQ3,y, c_y_out):
    global idTempQ3
    DiferencaAbsoluta = abs(y - c_y_out)
    if(DiferencaAbsoluta <= AreaCount):
        if(idQ3 != idTempQ3):
            idTempQ3 = idQ3
            return 1
        else:
            return 0
    else:
        return 0

# Função para verificar se o objeto está passando no quadrante 4 da linha de saída monitorada
def TestaQuad4(idQ4,y,c_y_out):
    global idTempQ4
    DiferencaAbsoluta = abs(y - c_y_out)
    if(DiferencaAbsoluta <= AreaCount):
        if(idQ4 != idTempQ4):
            idTempQ4 = idQ4
            return 1
        else:
            return 0
    else:
        return 0

# Função de retorno da chamada do threading.timer com argumentos de comando, configuração serial e status
def TimerP (*args):
    cmd = args[0]
    serialUSB = args[1]
    print("Count_F"+str(args[3])+" "+str(args[2])+" "+str(cmd)+" "+str(time()))
    serialUSB.write(bytes(cmd, 'utf-8'))

# Função para marcar os contornos, verificar posicionamento, realizar contagem e iniciar tempo de disparo do comando para o robô
def CntsOutputTest(Frame,x, y, w, h, idOut,colorId,CoordYSaida,CoordXLeft,CoordXCenter,CoordXRight,serialUSB,width):
    global ContadorSaidas
    global ContadorSaidasGreen
    global ContadorQuad1
    global ContadorQuad2
    global ContadorQuad3
    global ContadorQuad4
    global count_p

    # Verifica a cor do objeto detectado e faz um retangulo ao redor
    if colorId:      # Verifica se é vermelho
        colorRet = (40,180,255)
    else:
        colorRet = (255,180,20)
    cv2.rectangle(Frame, (x, y), (x + w, y + h), colorRet, 2)

    # Determina o ponto central do contorno e desenha um circulo para indicar
    CoordenadaXCentroContorno = int((x+x+w)/2)
    CoordenadaYCentroContorno = int((y+y+h)/2)
    PontoCentralContorno = (CoordenadaXCentroContorno,CoordenadaYCentroContorno)
    cv2.circle(Frame, PontoCentralContorno, 1, (0, 0, 0), 1)

    # Testa interseccao dos centros dos contornos com a linha de referencia e seus quadrantes
    if (CoordenadaXCentroContorno >= 0) and (CoordenadaXCentroContorno <= CoordXLeft):
        if (TestaQuad1(idOut,CoordenadaYCentroContorno, CoordYSaida)):
            if colorId:
                count_p +=1
                ContadorQuad1 += 1
                ContadorSaidas += 1
                print("Count_ST"+str(count_p)+" P1 timer: "+str(time()))
                threading.Timer(14.3, TimerP, args = ("DO1 E1 TM400",serialUSB,"P1",count_p)).start()
            else:
                ContadorSaidasGreen += 1
                
    if (CoordenadaXCentroContorno >= CoordXLeft+1) and (CoordenadaXCentroContorno <= CoordXCenter):
        if (TestaQuad2(idOut,CoordenadaYCentroContorno, CoordYSaida)):
            if colorId:
                count_p +=1
                ContadorQuad2 += 1
                ContadorSaidas += 1
                print("Count_ST"+str(count_p)+" P2 timer: "+str(time()))
                threading.Timer(14.3, TimerP, args = ("DO2 E1 TM400",serialUSB,"P2",count_p)).start()
            else:
                ContadorSaidasGreen += 1
                
    if (CoordenadaXCentroContorno >= CoordXCenter+1) and (CoordenadaXCentroContorno <= CoordXRight):
        if (TestaQuad3(idOut,CoordenadaYCentroContorno,CoordYSaida)):
            if colorId:
                count_p +=1
                ContadorQuad3 += 1
                ContadorSaidas += 1
                print("Count_ST"+str(count_p)+" P3 timer: "+str(time()))
                threading.Timer(14.3, TimerP, args = ("DO3 E1 TM400",serialUSB,"P3",count_p)).start()
            else:
                ContadorSaidasGreen += 1
                
    if (CoordenadaXCentroContorno >= CoordXRight+1) and (CoordenadaXCentroContorno <= width):
        if (TestaQuad4(idOut,CoordenadaYCentroContorno,CoordYSaida)):
            if colorId:
                count_p +=1 
                ContadorQuad4 += 1
                ContadorSaidas += 1
                print("Count_ST"+str(count_p)+" P4 timer: "+str(time()))
                threading.Timer(14.3, TimerP, args = ("DO4 E1 TM400",serialUSB,"P4",count_p)).start()
            else:
                ContadorSaidasGreen += 1
                


'''
###################################
        Funçâos Principal
###################################
'''
flag_D1 = 0
flag_D2 = 0
flag_D3 = 0
flag_D4 = 0
tracker = EuclideanDistTracker()

camera = cv2.VideoCapture(0, cv2.CAP_V4L2)

camera.set(3, 640)
camera.set(4, 360)
camera.set(5, 15)  #set frame
camera.set(cv2.CAP_PROP_BRIGHTNESS, 128)
camera.set(cv2.CAP_PROP_CONTRAST, 32)
camera.set(cv2.CAP_PROP_AUTO_WB, 1)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)

kernel = np.ones((3, 3), np.uint8)

###### VERDE ESCURO #####
#lower = np.array([70, 100, 100])
#upper = np.array([77, 200, 200])
###### VERDE CLARO #####
#lower = np.array([44, 100, 120])
#upper = np.array([55, 200, 220])
###### VERDE CLARO FUNDO BRANCO #####
lower = np.array([44, 85, 50])
upper = np.array([55, 230, 160])
##### VERMELHO #####
#lower2 = np.array([0, 85, 150])
#upper2 = np.array([15, 255, 255])
##### VERMELHO FUNDO BRANCO #####
lower2 = np.array([0, 115, 80])
upper2 = np.array([10, 230, 185])
lower1 = np.array([170, 115, 80])
upper1 = np.array([180, 230, 185])
##### ROXO FUNDO BRANCO #####
#lower3 = np.array([120, 75, 80])
#upper3 = np.array([140, 220, 185])

TextColor = ""
colorId = 0
colorHSV = []
DilateBulr3 = 0
MoveW = 0

serialUSB = serial.Serial('/dev/ttyACM0', 57600, timeout=0, dsrdtr=False)
serialUSB.flush()

# Laço para realizar a leitura de alguns frames antes de iniciar a analise para estabilização da luminosidade da câmera
for i in range(0,20):
    grabbed, Frame = camera.read()

# Configura os parametros das rodas
serialUSB.write(b"WP MT1 WD99,65")
sleep(0.1)
serialUSB.write(b"WP MT2 WD100,25")
sleep(0.1)
serialUSB.write(b"WP DW261")
sleep(0.1)

# Inicializa as variáveis de rastreamento
tracker = EuclideanDistTracker()


while True:
    # Realiza a leitura dos frames da imagem
    (grabbed, Frame) = camera.read()

    #se nao foi possivel obter frame, nada mais deve ser feito
    if not grabbed:
        break
    
    # Determina a altura e largura do frame
    height = int(np.size(Frame,0))
    width = int(np.size(Frame,1))

    # Região para realizar a identificação dos objetos
    roi = Frame[AreaMinY:AreaMaxY, 0:width]

    # Filtros para tratamento de cor do frame
    FrameBulr = cv2.GaussianBlur(roi, (19, 19), 0)
    FrameHsv = cv2.cvtColor(FrameBulr, cv2.COLOR_BGR2HSV)
    erode = cv2.erode(FrameHsv, kernel, iterations=1)
    dilate = cv2.dilate(erode, kernel, iterations=1)

    # Determina o Range de cor vermelha e verde para localizar os contornos
    Range1 = cv2.inRange(dilate, lower, upper)
    Range2 = cv2.inRange(dilate, lower2, upper2)
    Range3 = cv2.inRange(dilate, lower1, upper1)
    Range = Range1 + Range2 + Range3
    cnts,_ = cv2.findContours(Range.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Desenha linhas de referência
    CoordenadaYLinhaSaida = int((height / 2)+OffsetLinhaSaida)
    CoordenadaXLeft = int(((width/2)/2)-1)
    CoordenadaXCenter = int(width/2)
    CoordenadaXRight = int((width/2) + CoordenadaXLeft + 2)

    cv2.line(Frame, (CoordenadaXLeft,0), (CoordenadaXLeft,height), (200, 255, 100), 1)
    cv2.line(Frame, (CoordenadaXCenter,0), (CoordenadaXCenter,height), (200, 255, 100), 1)
    cv2.line(Frame, (CoordenadaXRight,0), (CoordenadaXRight,height), (200, 255, 100), 1)
    cv2.line(Frame, (0,CoordenadaYLinhaSaida), (width,CoordenadaYLinhaSaida), (0, 0, 200), 6)
    cv2.line(Frame, (0,AreaMinY), (width,AreaMinY), (200, 255, 100), 1)
    cv2.line(Frame, (0,AreaMaxY), (width,AreaMaxY), (200, 255, 100), 1)

    # Faz a varredura das áreas encontradas
    detections = []

    for c in cnts:
        #contornos de area muito pequena sao ignorados.
        #print(str(cv2.contourArea(c))+' '+str(color))
        if cv2.contourArea(c) > AreaContornoLimiteMin: 
            #obtem coordenadas do contorno (na verdade, de um retangulo que consegue abrangir todo ocontorno) e
            #realca o contorno com um retangulo.
            (x, y, w, h) = cv2.boundingRect(c)  #x e y: coordenadas do vertice superior esquerdo
                                                #w e h: respectivamente largura e altura do retangulo
            # Adiciona contorno encontrado para função de rastreamento
            detections.append([x, y, w, h])

    # Verifica os contornos rastreáveis e marca na tela e faz a contagem dos contornos encontrados
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        colorHSV = []
        x, y, w, h, id = box_id
        colorHSV = dilate[int(y+(h/2))][int(x+(w/2))]
        if (colorHSV[0] >= 0 and colorHSV[0] <= 15) or (colorHSV[0] >= 170 and colorHSV[0] <= 180):
            #TextColor = "Red"
            colorId = 1
        elif colorHSV[0] >= 44 and colorHSV[0] <= 55:
            #TextColor = "Green"
            colorId = 0
        
        CntsOutputTest(Frame,x, y+AreaMinY, w, h, id,colorId,CoordenadaYLinhaSaida,CoordenadaXLeft,CoordenadaXCenter,CoordenadaXRight,serialUSB,width)

    # Informa na imagem o número de objetos que passaram pelas zonas pré determinadas
    TotalSaidas = ContadorSaidasGreen + ContadorSaidas

    cv2.rectangle(Frame, (0,0), (width,27), (255,255,255), -1)
    cv2.rectangle(Frame, (0,height-25), (width,height), (255,255,255), -1)

    cv2.putText(Frame, "BOM: {}".format(str(ContadorSaidasGreen)), (10, 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.1, (0, 165, 0), 2)
    cv2.putText(Frame, "RUIM: {}".format(str(ContadorSaidas)), (243, 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.1, (0, 0, 200), 2)
    cv2.putText(Frame, "TOTAL: {}".format(str(TotalSaidas)), (436, 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.1, (220, 100, 0), 2)
    cv2.putText(Frame, "SE1: {}".format(str(ContadorQuad1)), (3, height - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 220), 1)
    cv2.putText(Frame, "SE2: {}".format(str(ContadorQuad2)), (CoordenadaXLeft + 3, height - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 220), 1)
    cv2.putText(Frame, "SE3: {}".format(str(ContadorQuad3)), (CoordenadaXCenter + 3, height - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 220), 1)
    cv2.putText(Frame, "SE4: {}".format(str(ContadorQuad4)), (CoordenadaXRight + 3, height - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 220), 1)

    cv2.imshow("Original", Frame)

    buttonKey = cv2.waitKey(1)

    if buttonKey == ord('q'):
        break

    if buttonKey == ord('f'):

        # Sequência de comandos para movimentação do robô
        serialUSB.write(b"LT E1 RD20 GR70 BL30")
        serialUSB.write(b"MT0 E1 D420 AT1500 DT0 V8")   # Reta inicial
        serialUSB.write(b"LT E1 RD50 GR0 BL5")
        serialUSB.write(b"MT0 E1 D1450 AT0 DT0 V8")     # Área de plantiu
        serialUSB.write(b"LT E1 RD50 GR0 BL0")
        serialUSB.write(b"MT0 D47 DF L RI200 V8")       # Manobra da cabeceira
        serialUSB.write(b"MT0 D270 DF R RI400 V8")
        serialUSB.write(b"MT0 D56 DF L RI300 V8")
        serialUSB.write(b"MT0 D21 DF R RI200 V8")
        serialUSB.write(b"LT E1 RD20 GR70 BL30")
        serialUSB.write(b"MT0 D550 AT0 DT0 V8")         # Reta para indireitar o implemento
        serialUSB.write(b"LT E1 RD50 GR0 BL5")
        serialUSB.write(b"MT0 D1450 AT0 DT0 V8")        # Área de plantiu
        serialUSB.write(b"LT E1 RD20 GR70 BL30")
        serialUSB.write(b"MT0 D50 DF L RI300 V8")       # Manobra para saída da área de teste
        serialUSB.write(b"MT0 D510 AT0 DT0 V8")
        serialUSB.write(b"MT0 D54 DF R RI290 V8")
        serialUSB.write(b"MT0 D1000 AT0 DT1500 V8")
        serialUSB.write(b"LT E0 RD0 GR0 BL0")


    if buttonKey == ord('b'):
        serialUSB.write(b"MT0 BC")
        serialUSB.write(b"MT0 E0")
        serialUSB.write(b"LT E0 RD0 GR0 BL0") 

    if buttonKey == ord('s'):
        serialUSB.write(b"MT0 E1")
        serialUSB.write(b"LT E1 RD20 GR70 BL30") 
    
    if buttonKey == ord('1'):
        if flag_D1 == 0:
            flag_D1 = 1
            serialUSB.write(b"DO1 E1")
        else:
            flag_D1 = 0
            serialUSB.write(b"DO1 E0")
    if buttonKey == ord('2'):
        if flag_D2 == 0:
            flag_D2 = 1
            serialUSB.write(b"DO2 E1")
        else:
            flag_D2 = 0
            serialUSB.write(b"DO2 E0")
    if buttonKey == ord('3'):
        if flag_D3 == 0:
            flag_D3 = 1
            serialUSB.write(b"DO3 E1")
        else:
            flag_D3 = 0
            serialUSB.write(b"DO3 E0")
    if buttonKey == ord('4'):
        if flag_D4 == 0:
            flag_D4 = 1
            serialUSB.write(b"DO4 E1")
        else:
            flag_D4 = 0
            serialUSB.write(b"DO4 E0")


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


# Let CTRL+C actually exit