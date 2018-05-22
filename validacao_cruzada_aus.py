import random
import clusmulti
import os

class ValidacaoCruzadaAUs(object):   
    def __init__(self, pasta, images, labels, quantidade_blocos, quantidade_fotos_bloco, numero_labels):
      self.pasta = pasta
      self.arquivos = []
      self.quantidade_blocos =  quantidade_blocos
      self.quantidade_fotos_bloco = quantidade_fotos_bloco
      self.blocos = [[0]*quantidade_fotos_bloco for i in range(0, quantidade_blocos)]
      self.classificados_corretos = [0]*7
      self.classificados_errados = [[0]*7 for i in range(0, 7)]
      self.excluidos = []
      self.arquivos = os.listdir(self.pasta)
      self.fotos_classificadas_erradas = []
      self.numero_labels = numero_labels
      self.falso_positivos = [0]*numero_labels
      self.falso_negativos = [0]*numero_labels
      self.verdadeiro_positivos = [0]*numero_labels
      self.verdadeiro_negativos = [0]*numero_labels
      self.fp_bloco = 0
      self.fn_bloco = 0
      self.vp_bloco = 0
      self.vn_bloco = 0
      self.labels_bloco = 0
      self.precisao = 0
      self.revocacao = 0
      self.todas = [0]*numero_labels
      self.images, self.labels = images, labels
      
      for i in range(0, numero_labels-1):
          self.todas[i] = i+1
      
    def validacao(self, numero_entradas_rams, tamanho_entrada_rams, score_minimo, intervalo_crescimento, confianca = 0.01, bleaching = 0):
        entrada = []
	  
        numeros = []
        
        self.precisao = 0
        self.revocacao = 0
        
        classificados_bloco = [0]*self.quantidade_blocos
	  
        for i in range(0, self.quantidade_blocos*self.quantidade_fotos_bloco):
            numeros.append(i)
       
        random.shuffle(numeros)
       
        num = 0
       
        for i in range(0, self.quantidade_blocos):
           for j in range(0, self.quantidade_fotos_bloco):
               self.blocos[i][j] = numeros[num]
               num += 1
	    
        erros_total = 0
        desvio_padrao = 0
        
        erros_bloco = [0] * self.quantidade_blocos
        blocos_invalidos = 0
	  
        for i in range(0, self.quantidade_blocos):
            self.fp_bloco = 0
            self.fn_bloco = 0
            self.vp_bloco = 0
            self.vn_bloco = 0
     
            rede = clusmulti.CluswisardMultiLabel(numero_entradas_rams,tamanho_entrada_rams,score_minimo,intervalo_crescimento)
            
            for j in range(0, self.quantidade_blocos):
                  if not(i == j):
                      for k in range(0, self.quantidade_fotos_bloco):
                          imagem = self.obter_imagem(j, k)
                          entrada = self.gerador_booleano(imagem)
                          labels = self.obter_label(j, k)
                          label = self.codificar(labels)
                          if label == 0:
                              rede.treinar_cluster(entrada)
                          else:
                              rede.treinar(entrada, label)
           
            for j in range(0, self.quantidade_fotos_bloco):
                imagem = self.obter_imagem(i, j)
                labels = self.obter_label(i, j)
                
                if(not(labels[0] == '0')):
                    entrada = self.gerador_booleano(imagem)
    			  
                    classificacao = rede.classificar(entrada, confianca, bleaching)
                    
                    labels_obtidas = self.decodificar(classificacao)
                        
                    labels_int = [int(label) for label in labels]
                
                    self.obter_falso_positivo(labels_int, labels_obtidas)
                    self.obter_falso_negativo(labels_int, labels_obtidas)
                    self.obter_verdadeiro_positivo(labels_int, labels_obtidas)
                    self.obter_verdadeiro_negativo(labels_int, labels_obtidas)
                    
                    classificados_bloco[i] += 1
                
            if(classificados_bloco[i] == 0): 
                erros_bloco[i] = 0
                blocos_invalidos += 1
            else:   
                erros_bloco[i] = 1 - ((self.vn_bloco+self.vp_bloco)/((self.fp_bloco+self.fn_bloco+self.vp_bloco+self.vn_bloco)))
                self.precisao += ((self.vp_bloco/(self.vp_bloco+self.fp_bloco)) if (not((self.vp_bloco+self.fp_bloco)==0)) else 0)
                self.revocacao += ((self.vp_bloco/(self.vp_bloco+self.fn_bloco)) if (not((self.vp_bloco+self.fn_bloco)==0)) else 0)
	  
        for i in range(0, self.quantidade_blocos-1):
            erros_total += erros_bloco[i]
            
        for i in range(0, self.quantidade_blocos-1):
            desvio_padrao += abs(erros_total-erros_bloco[i])
            
        self.precisao = self.precisao/self.quantidade_blocos
        self.revocacao = self.revocacao/self.quantidade_blocos
        
        arquivo = open(self.pasta+'new validacao cruzada-'+str(score_minimo)+'-'+str(intervalo_crescimento)+'.txt', 'a')
        arquivo.write('n: ' + str(numero_entradas_rams))
        arquivo.write('Porcentagem total de erros: ')
        arquivo.write('\n\n')
        arquivo.write(str(erros_total/(self.quantidade_blocos-blocos_invalidos)))
        arquivo.write('\n\n')
        arquivo.write('Desvio-padrão: ')
        arquivo.write(str(desvio_padrao/(self.quantidade_blocos-blocos_invalidos)))
        arquivo.write('\n\n')
        arquivo.write('Falso positivos: ')
        arquivo.write(str(self.falso_positivos))
        arquivo.write('\n\n')
        arquivo.write('Falso negativos: ')
        arquivo.write(str(self.falso_negativos))
        arquivo.write('\n\n')
        arquivo.write('Verdadeiro positivos: ')
        arquivo.write(str(self.verdadeiro_positivos))
        arquivo.write('\n\n')
        arquivo.write('Verdadeiro negativos: ')
        arquivo.write(str(self.verdadeiro_negativos))
        arquivo.write('\n\n')
        arquivo.write('Precisão: ')
        arquivo.write(str(self.precisao))
        arquivo.write('\n\n')
        arquivo.write('Revocação: ')
        arquivo.write(str(self.revocacao))
        arquivo.write('\n\n')
        arquivo.write('F1 Score: ')
        if(self.precisao+self.revocacao == 0):
            arquivo.write(str('0'))
        else:
            arquivo.write(str((2*self.precisao*self.revocacao)/(self.precisao+self.revocacao)))
        arquivo.write('\n\n')
        arquivo.write('Discriminadores:')
        for i in range(0, len(rede.discriminadores)):
            arquivo.write('Classe: ')
            classe_decodificada = self.decodificar(rede.discriminadores[i].classe)
            for i in range(0, len(classe_decodificada)):
                if(classe_decodificada[i] == 1):
                    arquivo.write(str(i+1) + ', ')
            arquivo.write('\n\n')
            arquivo.write('Número de exemplos aprendidos: ')
            arquivo.write(str(rede.discriminadores[i].exemplos_aprendidos))
            arquivo.write('\n\n')
        arquivo.write('\n\n')
        arquivo.write('\n\n')
    
        
    def sortear_imagem(self, i, j):
        foto = random.uniform(0, self.quantidade_blocos*self.quantidade_fotos_bloco)
	  
        if not(self.excluidos.contains(foto)):
            self.blocos[i][j] = foto
            self.excluidos.append(foto)
        else:
            self.sortear_imagem(i, j)
  
    def obter_imagem(self, i, j):
        return self.images[self.blocos[i][j]]
    
    def obter_label(self, i, j):
        return self.labels[self.blocos[i][j]]
    
    def codificar(self, aus):
        classe = 0
        labels = [int(i) for i in aus]
        #print(labels)
        for i in range(0, self.numero_labels-1):
            if i in labels:
                classe = classe + pow(2, i)
        return classe
    
    @staticmethod
    def decodificar(classificacao):
        #print(classificacao)
        dec = [int(i) for i in str(bin(classificacao))[2:]]
        #print('DEC')
        #print(dec)
        dec = dec[::-1]
        #print(dec)
        while(len(dec)<45):
            dec = dec + [0]
        return dec
            
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
    def subtrair_listas(lista1, lista2):
        print(lista2)
        print(lista2[len(lista2)-1])
        print(len(lista2))
        for i in range(0, len(lista2)):
            print(i)
            if lista2[i] in lista1:
                lista1.remove(lista2[i])
        return lista1
    
    @staticmethod
    def interseccao_listas(lista1, lista2):
        lista_nova = []
        for i in range(0, len(lista2)):
            if lista2[i] in lista1:
                lista_nova.append(lista2[i])
        return lista_nova
    
    def obter_falso_positivo(self, labels, labels_obtidas):
        for i in range(0, len(labels_obtidas)):
            if labels_obtidas[i] == 1:
                if(not(i in labels)):
                    self.falso_positivos[i] += 1
                    self.fp_bloco += 1
                    
    def obter_falso_negativo(self, labels, labels_obtidas):
        for i in range(0, len(labels_obtidas)):
            if labels_obtidas[i] == 0:
                if(i in labels):
                    self.falso_negativos[i] += 1
                    self.fn_bloco += 1
                    
    def obter_verdadeiro_positivo(self, labels, labels_obtidas):
        for i in range(0, len(labels_obtidas)):
            if labels_obtidas[i] == 1:
                if(i in labels):
                    self.verdadeiro_positivos[i] += 1
                    self.vp_bloco += 1
                    
    def obter_verdadeiro_negativo(self, labels, labels_obtidas):
        for i in range(0, len(labels_obtidas)):
            if labels_obtidas[i] == 0:
                if(not(i in labels)):
                    self.verdadeiro_negativos[i] += 1
                    self.vn_bloco += 1