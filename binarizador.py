from math import sqrt

class Binarizador(object):
  def binarizar(self, imagem):
    binarizacao = []
    
    luminancia_media = 0
       
    for x in range(0, imagem.shape[0]):
        for y in range(0, imagem.shape[1]):
            cor = imagem[x, y]
            luminancia_media += self.obter_luminancia(cor)
            
    luminancia_media /= imagem.shape[0] * imagem.shape[1]
    
    for x in range(0, imagem.shape[0]):
        for y in range(0, imagem.shape[1]):
            cor = imagem[x, y]
            luminancia = self.obter_luminancia(cor)
            if (luminancia >= 1.5 * luminancia_media):
                condicao = True
            else:
                condicao = False
            binarizacao.append(condicao)
    return binarizacao 
 
  def binarizar_luminancia(self, imagem):
      luminancia_media = 0
      
      for x in range(0, imagem.shape[0]):
          for y in range(0, imagem.shape[1]):
              cor = imagem[x, y]
              luminancia_media += self.obter_luminancia(cor)
    
      luminancia_media /= imagem.shape[0] * imagem.shape[1]
    
      for x in range(0, imagem.shape[0]):
          for y in range(0, imagem.shape[1]):
              cor = imagem[x, y]
        
              luminancia = self.obter_luminancia(cor)
        
              if (luminancia >= 0.7 * luminancia_media):
                  imagem[x, y] = [0, 0, 0]
              else:
                  imagem[x, y] = [255, 255, 255]
      
      return imagem
  
  def calcular_histograma(self, imagem):
      histograma = [0]*257
	  
      for x in range(0, imagem.shape[0]):
          for y in range(0, imagem.shape[1]):
              cor = imagem[x, y]
              histograma[int (self.obter_luminancia(cor))] += 1
	  
      return histograma
  
  @staticmethod
  def calcular_media(imagem):
      media = 0
	  
      for x in range(0, imagem.shape[0]):
          for y in range(0, imagem.shape[1]):
              media += sum(imagem[x, y])/3
	  
      media /= imagem.shape[0] * imagem.shape[1]
	  
      return media
  
  @staticmethod
  def calcular_desvio_padrao(histograma, media):
	  variancia = 0
	  
	  for i in range(0, 256):
		  variancia += (histograma[i]-media)**2
	  
	  variancia /= 256
	  
	  desvio_padrao = sqrt(variancia)
	  
	  return desvio_padrao
  
  def binarizar_savoula(self, imagem, peso):
      histograma = self.calcular_histograma(imagem)
      media = self.calcular_media(imagem)
      desvio_padrao = self.calcular_desvio_padrao(histograma, media)
      
      limiar = media + peso * (desvio_padrao/128 - 1) + 1
      
      for x in range(0, imagem.shape[0]):
          for y in range(0, imagem.shape[1]):
              if(sum(imagem[x, y])/3 > limiar):
                  imagem[x, y] = [255, 255, 255]
              else:
                  imagem[x, y] = [0, 0, 0]
      
      return imagem

  @staticmethod
  def obter_luminancia(cor):
      return 0.2126 * cor[0] + 0.7152 * cor[1] + 0.0722 * cor[2]