'''
Created on Jul 19, 2015

@author: Riz
'''
from pydub import AudioSegment
sound = AudioSegment.from_wav("1.wav")
sound = sound.set_channels(1)
sound.export("2.wav", format="wav")