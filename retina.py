import random

class Retina(object): 

  def __init__(self, tamanho):
      self.retina = {}
      
      for i in range(0, tamanho):
          self.retina[i] = i

      for i in range(0, tamanho):
          random_indice = random.randint(0, tamanho - 1)
          temp = self.retina[i]
          self.retina[i] = self.retina[random_indice]
          self.retina[random_indice] = temp
  
  def organizar(self, input_):
      input_organizado = []
    
      for i in range(0, len(self.retina)):
          temp1 = self.retina[i]
          #print("temp1")
          #print(temp1)
          #print(len(input_))
          temp2 = input_[temp1]
          input_organizado.append(temp2)

      return input_organizado
  
  def reorganizar(self, input_organizado):
      input_ = input_organizado
      
      #print(str(len(input_)) +"/" + str(len(self.retina)))
    
      '''verdadeiro = 0
      falso = 0
    
      for i in range(0, len(input_organizado)):
          if(input_organizado[i]):
              verdadeiro += 1
          if(not(input_organizado[i])):
              falso += 1'''
      for i in range(0, len(self.retina)):
          #print(str(len(input_)) +"/" + str(self.retina[i]))
          input_[self.retina[i]] = input_organizado[i]
    
      return input
  
  def sortear(self, input_):
    input_sorteado = []
    
    for i in range(0, len(self.retina)):
        input_sorteado[self.retina[i]] = input_[i]
    return input_sorteado