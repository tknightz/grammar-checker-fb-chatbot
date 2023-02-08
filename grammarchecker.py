import json
import requests

# mapMessage to translate response from LanguageTool to Vietnamese
mapMessage = {
    'Probably a noun is missing in this part of the sentence.': 'Có thể thiếu danh từ trong câu này!',
    'Use third-person verb with': 'Động từ đi với ngôi số 3',
    'The verb': 'Động từ',
    'is singular': 'là số ít',
    'Did you mean':'Ý bạn là',
    'The pronoun':'Danh từ',
    'is usually used with a third-person or a past tense verb':'thường đi với ngôi số ba hoặc động từ thì quá khứ',
    'must be used with a non-third-person form of a verb':'ko thể đi với động từ ngôi số 3',
    'This adjective uses the short comparatives form':'So sánh hơn của tính từ ngắn',
    'Use only': 'Chỉ sử dụng',
    '(without':'(ko cần',
    'when you use the comparative.':'khi bạn đặt câu so sánh.',
    'This sentence does not start with an uppercase letter':'Viết hoa ký tự đầu tiên của câu.',
    'It seems that a verb is missing.':'Có vẻ như thiếu động từ ở đây!',
    'Possible spelling mistake found.':'Có thể có lỗi chính tả ở đây!',
    'Consider using a past participle here':'Cân nhắc sử dụng dạng quá khứ ở đây',
    'instead of':'thay vì',
    'requires the base form of the verb': 'đi cùng với động từ nguyên thể',
    'is an adjective': 'là một tính từ',
    'You should probably use': 'Bạn nên sử dụng',
    'Possible agreement error': 'Có lỗi sử dụng từ'
}

class CheckerProcess:
    def __init__(self,text):
        self.endpoint = 'https://languagetool.org/api/v2/check'
        self.data = {
            'language': 'en-US',
            'text': text
        }
        self.response = json.loads(requests.post(self.endpoint,self.data).text)
        self.error = ''
        self.printError()

    def translateMessage(self,message):
        temp = message
        for tran in mapMessage:
            temp=temp.replace(tran,mapMessage[tran])
           
        self.error += f'*[?] Gợi ý* : {temp}\n'

    def printError(self):
        if self.response['language']['detectedLanguage']['code'] != 'en-US':
            self.error = 'Câu bạn nhập ko phải Tiếng Anh.'
            return

        if len(self.response['matches'])==0:
            self.error += 'Ko tìm thấy lỗi!'
        else:
            self.error += f"Tìm thấy *{len(self.response['matches'])}* lỗi.\n"
            self.error += '-------------------------------\n'
        
            for res in self.response['matches']:
                self.filterErr(res)

    def printReplacements(self,replacements,word):
        # Suggest correcting mistakes
        if len(replacements):
            self.error += f'Thay từ *"{word}"* thành từ '
            for i in range(len(replacements)):
                self.error += f"*\"{replacements[i]['value']}\"*"
                if i==len(replacements)-1:
                    self.error += '.\n'
                else:
                    self.error += ' | '

    def filterErr(self,matches):
        # Find type of mistakes in request
        self.error += f"*Trong câu* : _{matches['sentence']}_\n"
        
        if matches['rule']['issueType']=='grammar':
            self.error += '*[x] Lỗi ngữ pháp!*\n'
            
        elif matches['rule']['issueType']=='typographical':
            self.error += '*[x] Lỗi đánh máy!*\n'
        
        elif matches['rule']['issueType']=='misspelling':
            self.error += '*[x] Lỗi chính tả!*\n'
            
        else:
            self.error += f"*[x] {matches['rule']['issueType']}!*\n"
        
        
        self.translateMessage(matches['message']) 

        if len(matches['replacements']):
            self.error += '*[+] Sửa lỗi* : '
            self.printReplacements(matches['replacements'],self.data['text'][matches['offset']:matches['offset']+matches['length']])
        
        self.error += '-----------------------------\n'


if __name__ == "__main__":
    # For running project in command line.
    cp = CheckerProcess(input('Nhập câu cần kiểm tra : '))
    print(cp.error)
