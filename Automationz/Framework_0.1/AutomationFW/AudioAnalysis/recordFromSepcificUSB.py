'''
Created on Jul 19, 2015

@author: Riz
'''
import sys, wave, pyaudio
import pyaudio

## index the devices in the system

p = pyaudio.PyAudio()
count = p.get_device_count()
devices = []
for i in range(count):
    devices.append(p.get_device_info_by_index(i))

for i, dev in enumerate(devices):
    device_index_mic = "%d - %s" % (i, dev['name'])
    if "Microphone (C-Media USB" in dev['name']:
        device_index = i
        break
print device_index_mic,device_index

device = p.get_device_info_by_index(int(device_index))

chunk = 1024
format = pyaudio.paInt16
channels = 1 
record_cap = 10

rate = int(device['defaultSampleRate'])
stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
all = []
outname="thisiscool"
def write_wav_file(outname, channels, samp_width, rate, data):
    wf = wave.open(outname, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(samp_width)
    wf.setframerate(rate)
    wf.writeframes(data)
    wf.close()


for i in range(0, rate/chunk*record_cap):
    data = stream.read(chunk)
    all.append(data)

print "x\t done recording"
stream.stop_stream()
stream.close()
p.terminate()
write_wav_file(outname, channels, p.get_sample_size(format), rate, ''.join(all))
