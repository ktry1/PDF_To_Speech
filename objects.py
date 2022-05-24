from PyPDF2 import PdfFileReader
from gtts import gTTS


class Reader:
    def __init__(self):
        self.pages_text = []
        self.number_of_pages = 0
        self.reader = None

    def measure_pages(self,filename):
        self.reader = PdfFileReader(filename)
        self.number_of_pages = self.reader.numPages

    def extract_page(self,page,file_num):
        self.pages_text[file_num]+=self.reader.pages[page].extractText()
        return


class TextToSpeech:
    def __init__(self):
        pass
    def create_mp3(self,text,name,safedir):
        myobj = gTTS(text=text, lang="en", slow=False)
        if safedir == "":
            myobj.save(f"{name}.mp3")
            return
        myobj.save(f"{safedir}\{name}.mp3")

