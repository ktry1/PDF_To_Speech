from objects import Reader, TextToSpeech
from interface import Interface

reader = Reader()
text_to_speech = TextToSpeech()


interface = Interface(reader=reader, converter=text_to_speech)

