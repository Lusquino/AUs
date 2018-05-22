import random

class Ram(object):

  def __init__(self, numero_entrada_rams):
      self.ram = {} 
      for i in range(0, numero_entrada_rams):
          self.ram[i] = 0
    
  def incrementar(self, posicao):
    if not(posicao in self.ram):
        self.ram[posicao] = 0  
    self.ram[posicao] = self.ram[posicao] + 1
    
  def obter_acessos(self, bleaching):
      acessos = 0
	  
      for i in self.ram.values():
          if i > bleaching :
              acessos += i-bleaching
	  
      acessos_esperados = random.randint(0, acessos)
      
      acessos = 0
      
      for k in self.ram.keys():
          acessos += self.ram[k] - bleaching
          if acessos > acessos_esperados :
              return self.converter_int_lista_bool(acessos)
	  
      return None
  
  def obter_acessos_2(self, bleaching):
      acessos = 0
      
      for i in self.ram.values():
          acessos += i // bleaching
          
      acessosEsperados = random.randint(0, acessos)
      
      acessos = 0
      
      for k in self.ram.keys():
          acessos += self.ram[k] // bleaching
          if acessos > acessosEsperados :
              return bool(acessos)
      return None
  
  def converter_int_lista_bool(self, valor):
      entrada = []
      base2 = self.dec2bin(valor)
      for i in range(0, len(base2)):
          entrada.append(base2[i: i+1] == '1')
      
      return entrada
  
  @staticmethod
  def dec2bin(n):
        hexDict = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101',
                   '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'a':'1010', 'b':'1011',
                   'c':'1100', 'd':'1101', 'e':'1110', 'f':'1111', 'L':''}
        return ''.join([hexDict[hstr] for hstr in hex(n)[2:]])