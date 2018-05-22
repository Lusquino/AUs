# -*- coding: utf-8 -*-
"""
Created on Mon May 21 22:16:04 2018

@author: jhon
"""

import clusterizacao
import sys
import ckp

sys.setrecursionlimit(40000)

tamanho_entradas_rams = 84*80
pasta = 'C:/Users/jhon/Desktop/Doutorado/Tese/'

imgs, lbl = ckp.CKP.get_imgs_and_labels(None, 
                                 labels_dir='C:/Users/jhon/Desktop/Doutorado/Tese/ck+/FACS/', 
                                 imgs_dir='C:/Users/jhon/Desktop/Doutorado/Tese/ck+/savoula/')

labels = []
      
for i in range(0, len(imgs)):
    labels.append([])
    for j in range(0, len(lbl[i])):
        if(lbl[i][j][0][2] == '0'):
            if(lbl[i][j][0][len(lbl[i][j][0])-1] == '1'):
                labels[i].append(lbl[i][j][0][0] + '0')
            else:
                labels[i].append(lbl[i][j][0][0])
        else:
            labels[i].append(lbl[i][j][0][0]+lbl[i][j][0][2])

teste = clusterizacao.Clusterizacao(pasta)
for i in range(5, 155, 10):
    teste.validacao(i, tamanho_entradas_rams, 0.1, 10) 