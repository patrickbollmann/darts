# datrs
import wave
import pyaudio
import random
import os
def play_file(fname):
    # create an audio object
    wf = wave.open(fname, 'rb')
    p = pyaudio.PyAudio()
    chunk = 1024

    # open stream based on the wave object which has been input.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    x = 1
    while x != 100:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)
        x +=1
        # cleanup stuff.
    stream.close()
    p.terminate()  
def nrSound(nr):
    if(str(nr) == "180"):
        play_file(str(nr)+"v"+str(random.randint(1, 3))+".wav")
    else:
        play_file(str(nr)+".wav")        
def graphics(pList,p):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Punktestand:")
    for x in pList:
        print(x.name + " : "+str(x.score)+"          avg: "+str(x.avg))
    print("--------------------")
    print("")
    print(p.name+" ist am Zug!")
    print("Dir fehlen noch: "+str(p.score)+" Punkte!")    
class Player():
    
    def __init__(self, name, score):
        self.name =name
        self.score = score
        self.zuege = 0
        self.avg = 0
class Spiel():
    def __init__(self, pList,laenge):
        self.pList = pList
        self.spielerZahl = len(pList)
        self.laenge = laenge
    def winner(self, l):
        for x in l:
            if x.score == 0:
                return True
        return False
    def getAvg(self,p):
        return round(((self.laenge-p.score)/p.zuege),3)
    def zug(self, player):
        graphics(self.pList, player)
        wurf1 = None
        while wurf1 == None:
            wurf1 = self.wurf (input("Wurf 1:  "))
        if((player.score - wurf1) <0):
            print("Zug ungültig!")
            nrSound(0)
            return 0
        player.score -=wurf1
        graphics(self.pList, player)
        wurf2= None
        while wurf2 == None:
            wurf2  = self.wurf (input("Wurf 2:  "))
        if((player.score - wurf2) <0):
            print("Zug ungültig!")
            nrSound(0)
            player.score += wurf1
            return 0
        player.score -=wurf2
        graphics(self.pList, player)
        wurf3 = None
        while wurf3 == None:
            wurf3 = self.wurf (input("Wurf 3:  "))
        if((player.score - wurf3) <0):
            print("Zug ungültig!")
            nrSound(0)
            player.score += wurf1+wurf2
            return 0
        player.score -=wurf3
        punkte = wurf1+wurf2+wurf3
        print(punkte)
        player.zuege +=1
        player.avg = self.getAvg(player)
        nrSound(punkte)
        return punkte
    def wurf(self, a):
        if len(a)==0:
            return None
        multi = 1
        if(a[:2] == "3x"):
            multi = 3
            a = a[2:]
        if (a[:2] == "2x"):
            multi = 2
            a = a[2:]
        
        try:
            out = multi*int(a)
        except ValueError:
            return None
        if(out <= 60):
            return out
        else:
            print("Bitte gebe eine Zahl zwischen 1 und 60 ein. Multiplikatoren in der Form 3x20")
            return self.wurf((input("Erneute Eingabe:  ")))  
    def start(self):
        while self.winner(self.pList) == False:
            for p in self.pList:
                
                self.zug(p)
                
                if (p.score == 0):
                    graphics(self.pList,p)
                    print(p.name + " hat gewonnen")
                    break
def initSpiel():
    laenge = int(input("Welcher Punktestand soll erreicht werden?:  "))      
    sAnzahl = int(input("Spieleranzahl:  "))
    pList = []
    for x in range(sAnzahl):
        name = input("Wie heißt Spieler "+str(x+1)+"? ")
        pList.append(Player(name, laenge))
    return Spiel(pList, laenge)     

s = initSpiel()
s.start()