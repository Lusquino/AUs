from PIL import Image
import random
import image_setup
import ram

PIL_Version = Image.VERSION

class Discriminador(object):

  def __init__(self, numero_entradas_rams, tamanho_entrada):
    self.numero_entradas_rams = numero_entradas_rams
    self.tamanho_entrada = tamanho_entrada
    self.rams = []
    self.inicializar_rams()
  
  def treinar(self, entrada_reorganizada):
    posicao_atual = 0
    valor_entrada = 0
    
    for i in range(0, len(self.rams)):
       bloco = []
      
       for j in range(posicao_atual, min(posicao_atual + self.numero_entradas_rams, len(entrada_reorganizada))):
           bloco.append(entrada_reorganizada[j])
      
       posicao_atual += self.numero_entradas_rams
       valor_entrada = self.converter_para_int(bloco)
       
       #print(bloco)
       #print(valor_entrada)
       
       self.rams[i].incrementar(valor_entrada)
     
  def classificar(self, entrada_reorganizada, bleaching):
    saida = 0
    posicao_atual = 0
    valor_entrada =0
    saida_ram = 0
    
    for i in range(0, len(self.rams)):      
      bloco = []
    	
      for j in range(posicao_atual, min(posicao_atual + self.numero_entradas_rams, len(entrada_reorganizada))):
        bloco.append(entrada_reorganizada[j])
      
      posicao_atual += self.numero_entradas_rams
            
      valor_entrada = self.converter_para_int(bloco)
      
      if valor_entrada in self.rams[i].ram:
        saida_ram = self.rams[i].ram[valor_entrada]
        
        if saida_ram >= bleaching :
            saida += 1
     
    return saida
  
  def inicializar_rams(self):
    numero_rams = int(round(self.tamanho_entrada/self.numero_entradas_rams))
    for i in range(0, numero_rams):
        self.rams.append(ram.Ram(self.numero_entradas_rams))
   
  def precriar_imagens_mentais_0(self, bleaching):
      entrada = []
	  
      for i in range(0, len(self.rams)):
          for j in range(0, self.numero_entradas_rams):
              entrada.append(self.rams[i][j]>bleaching)
	    
      return entrada
  
  def precriar_imagens_mentais(self, bleaching):
      entrada = []
	  
      for i in range(0, len(self.rams)):
          entrada.append(self.rams[i].obter_acessos(bleaching))
	  
      return entrada
  
  def criar_imagens_mentais(self, entrada):
      imagem_mental = Image.Image()
      imagem_mental.width = image_setup.WIDTH_EMOTION
      imagem_mental.height = image_setup.HEIGHT_EMOTION
      
      for x in range(0, imagem_mental.width):
          for y in range(0, imagem_mental.height):
        
              if((y*imagem_mental.width + x)>=len(entrada)):
                  break
        
              if (entrada[y*imagem_mental.width + x]):
                  cor = (255, 255, 255)
              else:
                  cor = (0, 0, 0)
        
              imagem_mental.putpixel((x, y), cor)
              y += 1
          x += 1
    
      return imagem_mental
  
  def gerar_input(self):
      entrada = []
      posicao_atual = 0

      for i in range(0, len(self.rams)):
          ram = self.rams[i].ram
          numero_acessos = 0
      
          for valor in ram.values():
            numero_acessos += valor
            
          random_num_ac = random.randint(0, numero_acessos)
          
          chave_escolhida = -1
          
          for chave in ram.keys():
            random_num_ac -= ram[chave]
            
            if random_num_ac < 0 :
              chave_escolhida = chave
              break
          
          lista_bool = bin(chave_escolhida)
          
          while (len(lista_bool) < min([self.numero_entradas_rams, len(entrada)-posicao_atual])):
            lista_bool = '0' + lista_bool
          
          for j in range(len(lista_bool) - 1, -1, -1):
            if lista_bool[j]=='1' :
              entrada[posicao_atual + len(lista_bool) - j - 1] = True
            else:
              entrada[posicao_atual + len(lista_bool) - j - 1] = False
          posicao_atual += len(lista_bool)
      
      return entrada
  
  def gerar_input_modo(self, bleaching, modo):
      entrada = []
    
      posicao_atual = 0

      for i in range(0, len(self.rams)):
          ram = self.rams[i].ram
          numero_acessos = 0
          
          for valor in ram.values():
              if modo :
                  numero_acessos += valor//bleaching
              else:
                  if valor-bleaching >= 0:
                      numero_acessos += valor-bleaching
 		      
          random_num_ac = random.randint(0, numero_acessos)
          
          chave_escolhida = -1
          
          for chave in ram.keys():
              random_num_ac -= ram[chave]
              
              if random_num_ac<0 :
                  chave_escolhida = chave 
                  break			
        			
          lista_bool = bin(chave_escolhida)
      
          while (len(lista_bool) < min([self.numero_entradas_rams, len(entrada) - posicao_atual])):
              lista_bool = '0' + lista_bool
   
          for j in (len(lista_bool) - 1, -1, -1):
              if lista_bool[j]=='1':
                  entrada[posicao_atual + len(lista_bool) - j - 1] = True
              else:
                  entrada[posicao_atual + len(lista_bool) - j - 1] = False        
          posicao_atual += len(lista_bool)
      return entrada
  
  @staticmethod
  def converter_para_int(bloco):
      valor = 0
      #print('bloco')
      #print(bloco)
      for i in range(0, len(bloco)):
          #print(bloco[i])
          if bloco[i]:
              valor += int(pow(2, i))
      
      #print(valor)
      return valor