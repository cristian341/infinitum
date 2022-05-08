
import math
import itertools

class Encrypt:
    def __init__(self, phrase):
        self.phrase = phrase

    def build(self):
        evens = self.phrase[::2]
        odds = self.phrase[1::2]
        self.rails = evens + odds
        return self.rails
    
    def encrypt(self):
        self.cipher = "".join([self.rails[i:i+5] for i in range(0, len(self.rails), 5)])
        return self.cipher

    
class Decrypt:
    def __init__(self,phrase):
        self.phrase = phrase

    def split_rails(self):
        row_1_len = math.ceil(len(self.phrase)/2)
        self.row1 = (self.phrase[:row_1_len])
        self.row2 = (self.phrase[row_1_len:])
        return self.row1, self.row2

    def decrypt(self):
        message = []
        for r1,r2 in itertools.zip_longest(self.row1,self.row2):
            message.append(r1)
            message.append(r2)
        if None in message:
            message.pop()
        message = "".join(message)
        return message




def main():
    phrase = "Hello_world"
    security = Encrypt(phrase)
    security.build()
    text = security.encrypt()
    print(text)
    non = Decrypt(text)
    non.split_rails()
    mem = non.decrypt()
    print(mem)

if __name__ == "__main__":
    main()


