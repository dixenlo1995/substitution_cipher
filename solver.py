import string
import random
import time
from math import log10
from pycipher import SimpleSubstitution as SimpleSub
quadgram={}
trigram={}
whichgram={}
t_Start=0
t_End=0

def calfreq(dicnum):
    Sum=0
    if(dicnum=='3'):
        for v in trigram.values():
            Sum += v
        for key in trigram.keys():
            trigram[key] = log10(float(trigram[key])/Sum)
    elif(dicnum=='4'):
        for v in quadgram.values():
            Sum += v
        for key in quadgram.keys():
            trigram[key] = log10(float(quadgram[key])/Sum)        
    floor=log10(0.01/Sum)
    return floor

def opendic(dicnum):
    sep=' '
    if(dicnum=='3'):
        with open('english_trigrams.txt') as f:
            for line in f.readlines():
                key,cnt =line.split(sep)
                trigram[key]=int(cnt)
    elif(dicnum=='4'):
        with open('english_quadgrams.txt') as f:
            for line in f.readlines():
                key,cnt =line.split(sep)
                quadgram[key]=int(cnt)
        
def chooseCtextflag(which):
    if which=='1':
        f=open('Ciphertext/Cipher1.txt','r')
        f.seek(1,0)
        flag=f.read(15)
        return flag
    elif which=='2':
        f=open('Ciphertext/Cipher2.txt','r')
        f.seek(1.0)
        flag=f.read(15)
        return flag
    elif which=='3':
        f=open('Ciphertext/Cipher3.txt','r')
        f.seek(1.0)
        flag=f.read(15)
        return flag
    elif which=='4':
        f=open('Ciphertext/Cipher4.txt','r')
        f.seek(1.0)
        flag=f.read(15)
        return flag
    elif which=='5':
        f=open('Ciphertext/Cipher5.txt','r')
        f.seek(1.0)
        flag=f.read(15)
        return flag
        


def chooseCtext(which):
    if which=='1':
        f=open('Ciphertext/Cipher1.txt','r')
        f.seek(17,0)
        ctext=f.read()
        return ctext
    elif which=='2':
        f=open('Ciphertext/Cipher2.txt','r')
        f.seek(17.0)
        ctext=f.read()
        return ctext
    elif which=='3':
        f=open('Ciphertext/Cipher3.txt','r')
        f.seek(17.0)
        ctext=f.read()
        return ctext
    elif which=='4':
        f=open('Ciphertext/Cipher4.txt','r')
        f.seek(17.0)
        ctext=f.read()
        return ctext
    elif which=='5':
        f=open('Ciphertext/Cipher5.txt','r')
        f.seek(17.0)
        ctext=f.read()
        return ctext

def decipher(ctext,flag,length,floor,which,dicnum):
    file=open('Plaintext/Result.txt','w')
    if(dicnum=='3'):
        ngram=trigram
    elif(dicnum=='4'):
        ngram=quadgram
    print("\nDeciphering^_^")
    t_Start=time.time()
    max_key = list(string.ascii_uppercase)
    max_score = -99e9
    while str(SimpleSub(max_key).decipher(flag))!="TOLPKTEHDCISSZQ":
        max_key = list(string.ascii_uppercase)
        max_score = -99e9
        parentscore,parentkey = max_score,max_key[:]
        random.shuffle(parentkey)
        deciphering = SimpleSub(parentkey).decipher(ctext)
        parentscore = 0
        for x in range(len(deciphering)-length+1):
            if deciphering[x:x+length] in ngram: 
                parentscore += ngram[deciphering[x:x+length] ]
            else: 
                parentscore += floor   
        cnt=0
        while cnt < 1000:
            a = random.randint(0,25)
            b = random.randint(0,25)
            child = parentkey[:]
            child[a],child[b] = child[b],child[a]
            deciphering = SimpleSub(child).decipher(ctext)
            score = 0
            for x in range(len(deciphering)-length+1):
                if deciphering[x:x+length] in ngram: 
                    score += ngram[deciphering[x:x+length] ]
                else: 
                    score += floor
            if score > parentscore:
                parentscore = score
                parentkey = child[:]
                cnt = 0
            cnt = cnt+1
        if parentscore>max_score:
            max_score,max_key = parentscore,parentkey[:]
    t_End=time.time()
    print("\nFinish Decipher ^_^\n")
    print("Total time:",int(t_End-t_Start),'s')
    print("\nSubsituition table:")
    print("==========================")
    print("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    print(''+''.join(max_key))
    print("==========================")
    print('Plain text of Cipher:'+which+".txt is in Plaintext/Result.txt")
    file.write(SimpleSub(max_key).decipher(ctext))
    print('\nFlag of 105062226 ^_^: '+SimpleSub(max_key).decipher(flag))


def main():
    dicnum='\0'
    ngram_len=0
    while True:
        way=input("There are two cipher way,choose which way you want(input tri or quad): ")
        if way in('tri','quad'):
            if(way=='tri'):
                dicnum='3'
                ngram_len=3
            elif(way=='quad'):
                dicnum='4'
                ngram_len=4
            break
        else:
            print("\nPlease enter 'tri' or 'quad' ^_^\n")
    opendic(dicnum)

    while True:
        which=input("\nThere are five Ciphertext,choose which Ciphertext you want(input 1~5): ")
        if which in('1','2','3','4','5'):
            break
        else:
            print("\nPlease enter integer 1~5 ^_^\n")    
    flag=chooseCtextflag(which)
    ciphertext=chooseCtext(which)
    floor=calfreq(dicnum)
    decipher(ciphertext,flag,ngram_len,floor,which,dicnum)

main()