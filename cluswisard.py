# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:18:02 2018

@author: jhon
"""

import retina
import discriminador_cluswisard
from PIL import Image

PIL_Version = Image.VERSION

class Cluswisard(object):
  
  def __init__(self, numero_entradas_rams, tamanho_entrada, numero_discriminadores, score_minimo, intervalo_crescimento):
      self.retina = retina.Retina(tamanho_entrada)
      self.discriminadores = []
      self.numero_discriminadores = numero_discriminadores
      self.numero_entradas_rams = numero_entradas_rams
      self.tamanho_entrada = tamanho_entrada
      self.score_minimo = score_minimo
      self.intervalo_crescimento = intervalo_crescimento
      
      for i in range(0, numero_discriminadores):
          self.discriminadores.append(discriminador_cluswisard.DiscriminadorCluswisard(numero_entradas_rams, tamanho_entrada, i))
      self.classificacao_discriminadores = [0]*numero_discriminadores
      
  def treinar(self, entrada, discriminador):
      entrada_reorganizada = self.retina.organizar(entrada)
      self.discriminadores[discriminador].treinar(entrada_reorganizada)
      self.discriminadores[discriminador].exemplos_aprendidos = self.discriminadores[discriminador].exemplos_aprendidos+1
      
  def treinar_cluster(self, entrada):
      placar_discriminadores = self.obter_classificacoes(entrada, 0)
      melhor_resultado = self.obter_melhor_resultado(placar_discriminadores)
      discriminador = placar_discriminadores.index(melhor_resultado)
      
      if(melhor_resultado >= min([1, self.score_minimo+
                              self.discriminadores[discriminador].exemplos_aprendidos/self.intervalo_crescimento])):
        self.treinar(entrada, discriminador)
      else:
          self.discriminadores.append[discriminador_cluswisard.DiscriminadorCluswisard(self.numero_entradas_rams,
                                                                                       self.tamanho_entrada, self.discriminadores[discriminador].classe)]
          self.numero_discriminadores = self.numero_discriminadores + 1
          self.treinar(entrada, self.numero_discriminadores)
          
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