'''
Created on Jul 15, 2015

@author: Riz
'''
#from docutils.nodes import figure


import matplotlib.pyplot as plt
from scipy.io import wavfile # get the api
from scipy.fftpack import fft
from pylab import *

def f(filename):
    fs, data = wavfile.read(filename) # load the data
    a = data # this is a two channel soundtrack, I get the first track
    b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    c = fft(b) # create a list of complex number
    d = len(c)/2  # you only need half of the fft list
    #plt.plot(abs(c[:(d-1)]),'r')
    plt.plot(a,'r')
    savefig(filename+'.png')





file_path = 'C:\\Users\\Riz\\Music\\wave.wav'

f(file_path)

'''
import matplotlib.pyplot as plt
fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
ax.plot([0,1,2], [10,20,3])
fig.savefig("C:\\Users\\Riz\\Music\\wave.png" ) # save the figure to file
plt.close(fig)    # close the figure
'''