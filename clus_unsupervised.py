# -*- coding: utf-8 -*-
"""
Created on Wed May 16 19:41:15 2018

@author: jhon
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:18:02 2018

@author: jhon
"""

import retina
import discriminador_cluswisard
from PIL import Image

PIL_Version = Image.VERSION

class CluswisardUnsupervised(object):
  
  def __init__(self, numero_entradas_rams, tamanho_entrada, score_minimo, intervalo_crescimento):
      self.retina = retina.Retina(tamanho_entrada)
      self.discriminadores = []
      self.numero_discriminadores = 0
      self.numero_entradas_rams = numero_entradas_rams
      self.tamanho_entrada = tamanho_entrada
      self.score_minimo = score_minimo
      self.intervalo_crescimento = intervalo_crescimento
      self.classificacao_discriminadores = []
      self.clusters = []
      
  def treinar_cluster(self, entrada, item):
      entrada_reorganizada = self.retina.organizar(entrada)

      if(self.numero_discriminadores == 0):
          self.discriminadores.append(discriminador_cluswisard.DiscriminadorCluswisard(self.numero_entradas_rams,
                                                                                       self.tamanho_entrada, 0))
          self.clusters.append([])
          self.numero_discriminadores = self.numero_discriminadores + 1
          self.discriminadores[0].treinar(entrada_reorganizada)
          self.discriminadores[0].exemplos_aprendidos += 1
          self.clusters[0].append(item)
      if(self.numero_discriminadores > 0):              
          placar_discriminadores = self.obter_classificacoes(entrada, 0)      
          melhor_resultado = self.obter_melhor_resultado(placar_discriminadores)
          discriminador = placar_discriminadores.index(melhor_resultado)
                
          if(melhor_resultado >= min([1, self.score_minimo+
                                  self.discriminadores[discriminador].exemplos_aprendidos/self.intervalo_crescimento])):
              self.discriminadores[discriminador].treinar(entrada_reorganizada) 
              self.discriminadores[discriminador].exemplos_aprendidos += 1
              self.clusters[discriminador].append(item)
          else:
              self.discriminadores.append(discriminador_cluswisard.DiscriminadorCluswisard(self.numero_entradas_rams,
                                                                                           self.tamanho_entrada, self.discriminadores[discriminador].classe))
              self.clusters.append([])
              self.numero_discriminadores = self.numero_discriminadores + 1
              self.discriminadores[self.numero_discriminadores-1].treinar(entrada_reorganizada)
              self.discriminadores[self.numero_discriminadores-1].exemplos_aprendidos += 1
              self.clusters[self.numero_discriminadores-1].append(item)
          
  def classificar(self, entrada, confianca, bleaching):
      entrada_reorganizada = self.retina.organizar(entrada)
      return self.classificar2(entrada_reorganizada, confianca, bleaching)
      
  def classificar2(self, entrada, confianca, bleaching):
      self.classificacao_discriminadores = self.obter_classificacoes(entrada, bleaching)
      
      classe = 0
      
      melhor_resultado = self.obter_melhor_resultado(self.classificacao_discriminadores)
      segundo_resultado = self.obter_segundo_melhor_resultado(self.classificacao_discriminadores)
      
      if(melhor_resultado == 0):
          confianca_resultado = 0
      else:
          confianca_resultado = (melhor_resultado-segundo_resultado)/melhor_resultado
                  
      if(confianca_resultado<confianca):
          if(melhor_resultado==0):
              return 0
          else:
              classe = self.classificar2(entrada, confianca, bleaching+1)
      else:
          classe = self.obter_classe(self.classificacao_discriminadores, melhor_resultado)
    
      return classe
  
  def obter_classificacoes(self, entrada, bleaching):
      self.classificacao_discriminadores = [0]*self.numero_discriminadores
      
      for i in range(0, self.numero_discriminadores):
          if(self.discriminadores[i].exemplos_aprendidos == 0):
              self.classificacao_discriminadores[i] = 0
          else:
              self.classificacao_discriminadores[i] = (self.discriminadores[i].classificar(entrada, bleaching)/
                                                       self.discriminadores[i].exemplos_aprendidos)
	  
      return self.classificacao_discriminadores
  
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