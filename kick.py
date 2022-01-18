# import pyaudio
# import time

# pa = pyaudio.PyAudio()

# def callback(inp, frames, time, status):
#     return (bytes([255] * frames), pyaudio.paContinue)

# CHANNELS = 1
# FORMAT = pyaudio.paInt32

# stream = pa.open(
#     format=FORMAT, 
#     channels=CHANNELS,
#     rate=14400,
#     output=True,
#     stream_callback=callback)

# stream.start_stream()

# while stream.is_active():
#     time.sleep(0.1)

# stream.stop_stream()
# stream.close()
# pa.terminate()

import pyaudio
import numpy as np

p = pyaudio.PyAudio()
print(p.get_default_output_device_info())
volume = 1     # range [0.0, 1.0]
fs = 48000       # sampling rate, Hz, must be integer
duration = 100   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=fs,
                output=True)
# play. May repeat with different volume values (if done interactively) 
stream.write(volume*samples)

stream.stop_stream()
stream.close()

p.terminate()