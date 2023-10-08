import pyaudio
import numpy
import time
import wave

class TestClass():
    def callback(self, in_data, frame_count, time_info, status):
        data = waveData.getDataByFrameCount(frame_count)
        if len(data) < frame_count * waveData.chCount * waveData.width:
            remain = frame_count * waveData.chCount * waveData.width - len(data)
            data += b'\x00' * remain
        return (data, pyaudio.paContinue)

t = TestClass()

class AudioData():
    def __init__(self, waveFilePath):
        self.wf = wave.open(waveFilePath, 'r')
        self.chCount = self.wf.getnchannels();
        self.width = self.wf.getsampwidth()

    def seekToTop(self):
        self.wf.rewind()

    def getDataByFrameCount(self, frameCount):
        return self.wf.readframes(frameCount)

    def close(self):
        self.wf.close()

waveData = AudioData("tip.wav")
stream = None

output_device_index = 12

# define callback (2)
def callback(in_data, frame_count, time_info, status):    
    data = waveData.getDataByFrameCount(frame_count)
    if len(data) < frame_count * waveData.chCount * waveData.width:
        remain = frame_count * waveData.chCount * waveData.width - len(data)
        data += b'\x00' * remain
    return (data, pyaudio.paContinue)

def playFirst():
    # open stream using callback (3)
    global stream
    stream = p.open(format=p.get_format_from_width(waveData.wf.getsampwidth()),
                        channels = waveData.wf.getnchannels(),
                        output_device_index  = output_device_index,
                        rate = waveData.wf.getframerate(),
                        output = True,
                        frames_per_buffer = 128,
                        stream_callback=t.callback)
    # start the stream (4)
    stream.start_stream()

def play():
    # rewind the file
    waveData.seekToTop()

# open a wave file
# instantiate PyAudio (1)
p = pyaudio.PyAudio()
playFirst()

while(True):
    inp = input()
    if inp == "": # play
        play()
        continue
    elif inp == "q": # quit
        break

waveData.close()

# close PyAudio (7)
p.terminate()
