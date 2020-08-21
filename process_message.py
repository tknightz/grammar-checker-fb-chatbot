import re
import random
from grammerchecker import CheckerProcess

class Process:
    def __init__(self,string):
        self.string = string
        self.response = ''
        self.classifyMessage()

    # Classify message : checking grammar or any functionality
    def classifyMessage(self):
        if self.isGrammarChecking() is not None:
            self.response = self.checkGrammar()
        elif self.isGreeting() is not None:
            self.response = self.sendGreeting()

    # if message for checking grammar
    def isGrammarChecking(self):
        # find pattern check '{english}' using regrex 
        patternCheckGrammar = re.compile(r'^(check)\s\"(.+?)\"',re.IGNORECASE)
        matchGrammar = patternCheckGrammar.match(self.string)
        if matchGrammar is not None:
            return True
        return None

    def isGreeting(self):
        # if message just to say Hello
        patternGreeting = re.compile(r'^(Hi|Hello|Xin Chao).*',re.IGNORECASE)
        matchGreeting = patternGreeting.finditer(self.string)
        if matchGreeting is not None:
            return True
        return False

    def sendGreeting(self):
        myGreeting = ['Hello. How can I help you?', 'Hi. Nice to meet you.','Hi. Thanks for using my services.']
        return myGreeting[random.randint(0,2)]


    def checkGrammar(self):
        # find grammar mistakes in CheckerProcess
        sentence = re.findall(r'\"(.+?)\"',self.string)
        print(sentence[0])
        CP = CheckerProcess(sentence[0])
        return CP.error


    def sendResponse(self):
        return self.response


if __name__ == '__main__':
    cp = Process('check "this is sentence."')
    print(cp.sendResponse())
