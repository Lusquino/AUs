import retina
import discriminador
from PIL import Image

PIL_Version = Image.VERSION

class RedeNeuralComDiscriminadores(object):
  
  def __init__(self, numero_entradas_rams, tamanho_entrada, numero_discriminadores):
      self.retina = retina.Retina(tamanho_entrada)
      self.discriminadores = []
      self.numero_discriminadores = numero_discriminadores
      for i in range(0, numero_discriminadores):
          self.discriminadores.append(discriminador.Discriminador(numero_entradas_rams, tamanho_entrada))
      self.classificacao_discriminadores = [0]*numero_discriminadores
  
  def treinar(self, entrada, discriminador):
      entrada_reorganizada = self.retina.organizar(entrada)
      self.discriminadores[discriminador].treinar(entrada_reorganizada)
  
  def classificar(self, entrada, confianca, bleaching):
      self.classificacao_discriminadores = self.obter_classificacoes(entrada, bleaching)
      
      classe = 0
      
      melhor_resultado = self.obter_melhor_resultado(self.classificacao_discriminadores)
                  
      if(melhor_resultado == self.obter_segundo_melhor_resultado(self.classificacao_discriminadores)):
          if(melhor_resultado==0):
              return 0
          else:
              classe = self.classificar(entrada, confianca, bleaching+1)
      else:
          classe = self.obter_classe(self.classificacao_discriminadores, melhor_resultado)
    
      return classe
  
  def obter_classificacoes(self, entrada, bleaching):
      entrada_reorganizada = self.retina.organizar(entrada)

      for i in range(0, self.numero_discriminadores):
          self.classificacao_discriminadores[i] = self.discriminadores[i].classificar(entrada_reorganizada, bleaching)
	  
      return self.classificacao_discriminadores
  
  def criar_imagens_mentais(self, bleaching):
    imagens_mentais = []
    
    for i in range(0, self.numero_discriminadores):
      entrada = self.discriminadores[i].precriar_imagens_mentais(bleaching)
      entrada_nova = []
      
      for lb in entrada:
         if not(lb == None):
             for b in lb:
                 entrada_nova.append(b)
          
      entrada_nova = self.retina.reorganizar(entrada_nova)
      imagens_mentais[i] = self.discriminadores[i].criar_imagens_mentais(entrada_nova)
    
    return imagens_mentais
  
  def criar_imagem_mental(self, bleaching, modo):
    imagens_mentais = []
    
    for i in range(0, self.numero_discriminadores):
      entrada = self.retina.sortear(self.discriminadores[i].gerar_input())
      imagens_mentais[i] = self.discriminadores[i].criar_imagens_mentais(entrada)
    
    return imagens_mentais
  
  def calcular_confianca(self):
      melhor_resultado = self.obter_melhor_resultado(self.classificacao_discriminadores)
      segundo_melhor_resultado = self.obter_segundo_melhor_resultado(self.classificacao_discriminadores)
    
      if(melhor_resultado == 0):
          return 0
      return (melhor_resultado - segundo_melhor_resultado)/melhor_resultado
  
  def obter_classe(self, classificacao_discriminadores, valor):
      for i in range(0, self.numero_discriminadores):
          if(classificacao_discriminadores[i] == valor):
              return i
      return len(classificacao_discriminadores)-1
  
  @staticmethod
  def obter_melhor_resultado(valores):
      melhor_resultado = 0
    
      for i in range(0, len(valores)):
          if(valores[i] > melhor_resultado):
              melhor_resultado = valores[i]
      return melhor_resultado
  
  def obter_segundo_melhor_resultado(self, valores):
      novos_valores = [0] * (self.numero_discriminadores-1)
      melhor_resultado = self.obter_melhor_resultado(valores)   
      j = 0
      empate = False

      for i in range(0, len(valores)-1):
          if((valores[i] == melhor_resultado)and(empate == False)):
              i += 1
              empate = True
      
          if(i < len(valores)):
              novos_valores[j] = valores[i]
              j += 1
    
      return self.obter_melhor_resultado(novos_valores)