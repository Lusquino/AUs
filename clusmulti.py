# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:18:02 2018

@author: jhon
"""

import retina
import discriminador_cluswisard
from PIL import Image

PIL_Version = Image.VERSION

class CluswisardMultiLabel(object):
  
  def __init__(self, numero_entradas_rams, tamanho_entrada, score_minimo, intervalo_crescimento, limitante = 2):
      self.retina = retina.Retina(tamanho_entrada)
      self.discriminadores = []
      self.numero_discriminadores = 0
      self.numero_entradas_rams = numero_entradas_rams
      self.tamanho_entrada = tamanho_entrada
      self.score_minimo = score_minimo
      self.intervalo_crescimento = intervalo_crescimento
      self.classificacao_discriminadores = []
      self.limitante = limitante
      
  def treinar(self, entrada, classe):
      entrada_reorganizada = self.retina.organizar(entrada)
      exemplo_aprendido = False
      
      if(not(self.possui_classe(classe))):
          #print("passei aqui, onde tem label, mas não tem classe. fala tu")
          self.discriminadores.append(discriminador_cluswisard.DiscriminadorCluswisard(self.numero_entradas_rams,
                                                                                       self.tamanho_entrada, classe))
          self.numero_discriminadores = self.numero_discriminadores + 1
          self.discriminadores[self.numero_discriminadores-1].treinar(entrada_reorganizada)
          self.discriminadores[self.numero_discriminadores-1].exemplos_aprendidos += 1
      else:
          for i in range(0, self.numero_discriminadores):
              if((self.discriminadores[i].classe == classe) and (self.obter_score(self.discriminadores[i].classificar_score(entrada)) >= min([1, self.score_minimo+
                                              self.discriminadores[i].exemplos_aprendidos/self.intervalo_crescimento]))):
                  self.discriminadores[i].treinar(entrada_reorganizada)
                  self.discriminadores[i].exemplos_aprendidos += 1
                  exemplo_aprendido = True
          
          if(not(exemplo_aprendido) and self.quantidade_classe_repetida(classe) <= self.limitante):
              self.discriminadores.append(discriminador_cluswisard.DiscriminadorCluswisard(self.numero_entradas_rams,
                                                                                           self.tamanho_entrada, classe))
              self.numero_discriminadores = self.numero_discriminadores + 1
              self.discriminadores[self.numero_discriminadores-1].treinar(entrada_reorganizada)
              self.discriminadores[self.numero_discriminadores-1].exemplos_aprendidos += 1
      
  def treinar_cluster(self, entrada):
      entrada_reorganizada = self.retina.organizar(entrada)
      exemplo_aprendido = False

      if(self.numero_discriminadores > 0):              
          placar_discriminadores = self.obter_classificacoes(entrada, 0)      
          melhor_resultado = self.obter_melhor_resultado(placar_discriminadores)
          discriminador = placar_discriminadores.index(melhor_resultado)
          classe = self.discriminadores[discriminador].classe
    
          for i in range(0, self.numero_discriminadores):
             if((self.discriminadores[i].classe == classe) and (self.obter_score(self.discriminadores[i].classificar_score(entrada)) >= min([1, self.score_minimo+
                                  self.discriminadores[discriminador].exemplos_aprendidos/self.intervalo_crescimento]))):
              self.discriminadores[i].treinar(entrada_reorganizada)
              self.discriminadores[i].exemplos_aprendidos = self.discriminadores[i].exemplos_aprendidos+1
              exemplo_aprendido = True
          
          if(not(exemplo_aprendido) and self.quantidade_classe_repetida(classe) <= self.limitante):
              self.discriminadores.append(discriminador_cluswisard.DiscriminadorCluswisard(self.numero_entradas_rams,
                                                                                           self.tamanho_entrada, self.discriminadores[discriminador].classe))
              self.numero_discriminadores = self.numero_discriminadores + 1
              self.discriminadores[self.numero_discriminadores-1].treinar(entrada_reorganizada)
              self.discriminadores[self.numero_discriminadores-1].exemplos_aprendidos += 1
          
  def classificar(self, entrada, confianca, bleaching):
      entrada_reorganizada = self.retina.organizar(entrada)
      return self.classificar2(entrada_reorganizada, confianca, bleaching)
      
  def classificar2(self, entrada, confianca, bleaching):
      self.classificacao_discriminadores = self.obter_classificacoes(entrada, bleaching)
      
      #print('classificacao discriminadores') 
      #print(self.classificacao_discriminadores)
      
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
      
      #print('VOU CLASSIFICAR')
      
      for i in range(0, self.numero_discriminadores):
          #print(i)
          if(self.discriminadores[i].exemplos_aprendidos == 0):
              #print('APRENDEU NADA')
              self.classificacao_discriminadores[i] = 0
          else:
              #print('APRENDEU')
              #print(self.discriminadores[i].classificar(entrada, bleaching))
              #print(self.discriminadores[i].exemplos_aprendidos)
              self.classificacao_discriminadores[i] = (self.discriminadores[i].classificar(entrada, bleaching)/
                                                       self.discriminadores[i].exemplos_aprendidos)
	  
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
  
  def possui_classe(self, classe):
      if(any(self.discriminadores[i].classe for i in range(0, self.numero_discriminadores)) == classe):
      #for i in range(0, self.numero_discriminadores):
       #   if(self.discriminadores[i].classe == classe):
       return True
      return False
  
  @staticmethod
  def obter_score(classificacao):
      return sum(classificacao)/(max(classificacao)*len(classificacao))
  
  def quantidade_classe_repetida(self, classe):
      return self.discriminadores.count(classe)