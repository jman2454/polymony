import math
import playsound
import json
import wave
import pydub
import os
import shutil
from gensound import WAV
from gensound.effects import Stretch

SOUNDS = { 
    'default': 'rimshot.wav', 
    'kick': 'kick.wav', 
    'open': 'hat_open.wav', 
    'closed': 'hat_closed.wav',
    'tick': 'hat_tick.wav',
    'snare': 'snare.wav',
    'block': 'block.wav',
    'piano': 'piano.wav',
    'wave': 'rev_kick.wav',
    'click': 'click.wav'
}

TWOPI = 2*math.pi

class Instrument:
    def __init__(self, multiplier=1):
        self.theta = 0

        # speed in rad/sec
        self.speed = math.pi
        self.rings = []
        self.mult = multiplier

    def generateLoop(self, n_loops=1):
        # channels: 2, width: 2, rate: 44100, comptype: 'NONE', compname: 'not compressed'
        if os.path.exists('temp'):
            shutil.rmtree('temp')
        os.mkdir('temp')
        num_seconds = TWOPI / (self.speed * self.mult)
        ms = num_seconds * 1000
        n_frames = int(44100 * num_seconds)

        with wave.open('temp/temp_loop.wav', 'wb') as wvf:
            wvf.setparams((2,2,44100,n_frames,'NONE','not compressed'))
            wvf.writeframes(bytes([0] * n_frames * 2 * 2))
        
        empty = pydub.AudioSegment.from_file('temp/temp_loop.wav', format='wav')
        os.remove('temp/temp_loop.wav')
        ring_loops = []
        
        for ring_no in range(len(self.rings)):
            ring = self.rings[ring_no]
            loop = empty
            for i in range(ring.freq):
                loop = loop.overlay(ring.segment, position=int(i*ms/(ring.freq)))
                        
            # loop = loop._spawn(loop.raw_data, 
            #     overrides={
            #         'frame_rate': int(loop.frame_rate * self.mult)
            #         }).set_frame_rate(loop.frame_rate)
            filename = str.format('temp/ring{}.wav', ring_no)
            (loop*n_loops).export(filename, format='wav')
            ring_loops.append(loop)

        output = empty
        for loop in ring_loops:
            output = output.overlay(loop)
        
        (output*n_loops).export('temp/full.wav', format='wav')
        # (output[:len(output)//self.mult]*n_loops).export('temp/full.wav', format='wav')
        return output * n_loops

        
    def update(self, ms):
        inc = self.speed * (ms / 1000)
        
        # for ring in self.rings:
        #     if ring.doesNeedlePass(self.theta, inc):
        #         ring.play()

        prev = self.theta
        self.theta = (self.theta + inc) % TWOPI
        if self.theta < prev:
            playsound.playsound('out.wav', block=False)

    def withRing(self, ring):
        self.rings += [ring]
        return self

class Ring:
    def __init__(self, freq, r, sound_type='default'):
        self.freq = freq
        self.type = sound_type
        self.r = r
        self.file = str.format('sounds/{}', SOUNDS[sound_type])
        self.segment = pydub.AudioSegment.from_file(self.file)
        with wave.open(self.file) as wf:
            self.sound_bytes = wf.readframes(wf.getnframes())
        # self.file = SOUNDS[sound_type]

    def setFreq(self, val):
        assert isinstance(val, int)
        assert val > 0

        self.freq = val 

    def setR(self, val):
        assert isinstance(val, float)
        assert val > 0

        self.r = val

    def doesNeedlePass(self, start, inc):
        tick_to_check = (math.floor(start / (TWOPI / self.freq)) + 1) % self.freq
        tick_pos = (tick_to_check * (TWOPI / self.freq))
        final = (start + inc) % TWOPI

        return (start <= tick_pos and final > tick_pos) or (final < start and tick_pos == 0)

    def play(self):
        pass
        # playsound.playsound(str.format('sounds/{}', SOUNDS[self.type]), block=False)

def createRing(json):
    return Ring(json['freq'], json['r'])