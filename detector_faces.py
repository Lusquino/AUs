import os
import cv2
import rede_neural_com_discriminadores
import binarizador

class DetectorFaces(object):
  
  def __init__(self, numero_entradas_rams, largura_face, altura_face):
      self.numero_entradas_rams = numero_entradas_rams
      self.largura_face = largura_face
      self.altura_face = altura_face
      self.binarizador = binarizador.Binarizador()
      self.rede_face = rede_neural_com_discriminadores.RedeNeuralComDiscriminadores(self.numero_entradas_rams, int(self.largura_face * self.altura_face / self.numero_entradas_rams), 1)
  
  def treinar_face(self, pasta, largura, altura):
    arquivos = os.listdir(pasta)
    
    for arquivo in arquivos:
       imagem = cv2.imread(pasta+arquivo)
       imagem = cv2.resize(imagem, (self.largura_face, self.altura_face))
       entrada = self.binarizador.binarizar(imagem)
       self.rede_face.treinar(entrada, 0)
  
  def detectar_face(self, imagem):
    rams = [[0 for y in range(round(imagem.shape[1]/10)+1)] for x in range(round(imagem.shape[0]/10)+1)]
   
    i=0
    j=0
    
    for x in range(0, imagem.shape[0]-10, 10):
        j=0
        for y in range(0, imagem.shape[1]-10, 10):
            if((x+self.largura_face) < imagem.shape[0]):
                x_inicial = x
            else:
                x_inicial = imagem.shape[0] - self.largura_face
                
            if((y+self.altura_face) < imagem.shape[1]):
                y_inicial = y
            else:
                y_inicial = imagem.shape[1] - self.altura_face
            
            janela = imagem[y_inicial: y_inicial+self.altura_face, x_inicial: x_inicial+self.largura_face]
            print('TEST:'+ str(janela.shape[0]) + " " + str(janela.shape[1]))
            print(str(x)+"/"+ str(y))
            #print(str(largura_janela)+"/"+ str(altura_janela))
            janela = cv2.cvtColor(janela, cv2.COLOR_BGR2GRAY)
            suave = cv2.GaussianBlur(janela, (7, 7), 0)
            canny = cv2.Canny(suave, 20, 120)
            cv2.imwrite('C:/Users/jhon/Desktop/Mestrado/Dissertacao/temp.png', canny)
            test = cv2.imread('C:/Users/jhon/Desktop/Mestrado/Dissertacao/temp.png')
            entrada = self.binarizador.binarizar(test)
            print(str(len(rams))+"/"+str(len(rams[0]))+":"+str(i)+"/"+str(j))
            rams[i][j] = self.rede_face.classificar(entrada, 0.01, 0)
            j += 1
        i += 1
    
    cluster = self.detectar_melhores_clusters(rams)
    
    return imagem[self.altura_face : ((cluster[1]*10) if (((cluster[1]*10)+self.altura_face) <= imagem.shape[1]) else (imagem.shape[1] - self.altura_face)),
                  self.largura_face : ((cluster[0]*10) if (((cluster[0]*10)+self.largura_face) <= imagem.shape[0]) else (imagem.shape[0] - self.largura_face))]
  
  
  
  def detectar_melhores_clusters(rams):
    melhor_resultado = 0
    x = 0
    y = 0
    
    for i in range(0, len(rams)):
      for j in range(0, len(rams[i])):
        if rams[i][j] >= melhor_resultado :
            melhor_resultado = rams[i][j]
            x = i
            y = j
    
    cluster = [x, y]
    
    return cluster
  
  