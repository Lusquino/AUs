# -*- coding: utf-8 -*-
"""
Created on Wed May 16 19:59:20 2018

@author: jhon
"""

import clus_unsupervised
import os
import ckp
import math

class Clusterizacao(object):   
    def __init__(self, pasta):
      self.pasta = pasta
      self.arquivos = []
      self.arquivos = os.listdir(self.pasta)
      self.imgs, lbl = ckp.CKP.get_imgs_and_labels(None, 
                                           labels_dir='C:/Users/jhon/Desktop/Doutorado/Tese/ck+/FACS/', 
                                           imgs_dir='C:/Users/jhon/Desktop/Mestrado/Dissertacao/cohn kanade/imagens/')
      self.labels = []
      for i in range(0, len(lbl)):
          self.labels.append([])
          for j in range(0, len(lbl[i])):
              if(lbl[i][j][0][2] == '0'):
                  if(lbl[i][j][0][len(lbl[i][j][0])-1] == '1'):
                      self.labels[i].append(lbl[i][j][0][0] + '0')
                  else:
                      self.labels[i].append(lbl[i][j][0][0])
              else:
                  self.labels[i].append(lbl[i][j][0][0]+lbl[i][j][0][2])
      
    def validacao(self, numero_entradas_rams, tamanho_entrada_rams, score_minimo, intervalo_crescimento, confianca = 0.01, bleaching = 0):
       rede = clus_unsupervised.CluswisardUnsupervised(numero_entradas_rams,tamanho_entrada_rams,score_minimo,intervalo_crescimento)
        
       for i in range(0, len(self.imgs)):
           imagem = self.imgs[i]
           entrada = self.gerador_booleano(imagem)
           labels = self.labels[i]
           for j in range(0, len(labels)):
               rede.treinar_cluster(entrada, labels[j])
               
           soma_a = self.obter_soma_a(rede)
           soma_b = self.obter_soma_b(rede)
           soma_c = self.obter_soma_c(rede)
           soma_d = self.obter_soma_d(rede)
            
            
       arquivo = open(self.pasta+'cluster.txt', 'a')
       arquivo.write('n: ' + str(numero_entradas_rams))
       arquivo.write('\n\n')
       arquivo.write('rand: ')
       arquivo.write(str(self.rand(soma_a, soma_b, soma_c, soma_d)))
       arquivo.write('\n\n')
       arquivo.write('jaccard: ')
       arquivo.write(str(self.jaccard(soma_a, soma_b, soma_c)))
       arquivo.write('\n\n')
       arquivo.write('folkes-mellow: ')
       arquivo.write(str(self.folkes_mellow(soma_a, soma_b, soma_c)))
       arquivo.write('\n\n')
       arquivo.write('\n\n')
        
       arquivo.close()
       
    @staticmethod
    def gerador_booleano(imagem):
        entrada = []
        
        for i in range(0, imagem.shape[0]):
            for j in range(0, imagem.shape[1]):
                if(imagem[i, j][0] == 255) and (imagem[i, j][1] == 255) and (imagem[i, j][2] == 255):
                #print(imagem)
                #if(imagem[i, j] == 1):
                    entrada.append(True)
                else:
                    entrada.append(False)
        return entrada
    
    @staticmethod
    def obter_soma_a(rede):
        soma_a = 0
        
        for i in range(0, len(rede.clusters)):
            elementos = []
            
            for j in range(0, len(rede.clusters[i])):
                if(not(rede.clusters[i][j] in elementos)):
                    soma_a += rede.clusters[i].count(rede.clusters[i][j])
                    elementos.append(rede.clusters[i][j])
        
        return soma_a
    
    @staticmethod
    def obter_soma_b(rede):
        soma_b = 0
        
        for i in range(0, len(rede.clusters)):
            soma_b += len(set(rede.clusters[i]))
        
        return soma_b
    
    @staticmethod
    def obter_soma_c(rede):
        soma_c = 0
        
        for i in range(0, len(rede.clusters)):
            elementos = []
            
            for j in range(0, len(rede.clusters)):
                if(not(i == j)):
                    for k in range(0, len(rede.clusters[i])):
                        if(not(rede.clusters[i][k] in elementos)):
                            soma_c += rede.clusters[j].count(rede.clusters[i][k])
                            elementos.append(rede.clusters[i][k])
                            
        return soma_c
    
    @staticmethod
    def obter_soma_d(rede):
        soma_d = 0
        elementos = []
        
        for i in range(0, len(rede.clusters)):
            for j in range(0, len(rede.clusters)):
                if(not(i == j)):
                    for k in range(0, len(rede.clusters[i])):
                        if((not(rede.clusters[i][k] in elementos))and(rede.clusters[i][k] in rede.clusters[j])):
                            nova_lista = rede.clusters[j].remove(rede.clusters[i][k])
                            if(not(nova_lista==None)):   
                                soma_d += len(set(nova_lista))
                                elementos.append(rede.clusters[i][k])
                            
        return soma_d
    
    @staticmethod
    def rand(a, b, c, d):
        return (a+d)/(a+b+c+d)
    
    @staticmethod
    def jaccard(a, b, c):
        return a/(a+b+c)
    
    @staticmethod
    def folkes_mellow(a, b, c):
        return math.sqrt((a/(a+b))*(a/(a+c)))