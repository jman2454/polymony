import math
import playsound
import json
import wave
import pydub
import os
import shutil
import librosa
import soundfile as sf
import pygame
import math
import pyaudio
import random
from constants import Config
from pygame.mixer import Sound

SOUNDS = { 
    'default': 'hey.wav', 
    'hey': 'hey.wav',
    # 'default': 'click.wav',
    'wow' : 'whip.wav',
    'whip': 'whip.wav',
    'kick': 'kick.wav', 
    'open': 'hat_open.wav', 
    'closed': 'hat_closed.wav',
    'shot': 'rimshot.wav',
    'tick' : 'hattick.wav',
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
        self.speed = 2*math.pi
        self.rings = []
        self.mult = multiplier
        self.loop_cache = {}
        self.sound_cache = {}
        self.pct = 0
        self.time = 0
        self.wv = None
        self.stream = None
        self.running = False
        self.spinSpoke = True

    def setMultiplier(self, val):
        self.mult = val
        self.loop_cache = {}
        self.sound_cache = {}

    def getLoop(self, seconds=1):
        if seconds in self.loop_cache:
            return self.loop_cache[seconds]

        # channels: 2, width: 2, rate: 44100, comptype: 'NONE', compname: 'not compressed'
        if os.path.exists('temp'):
            shutil.rmtree('temp')
        os.mkdir('temp')

        num_seconds = TWOPI / self.speed

        if (self.mult < 1):
            num_seconds = num_seconds / self.mult

        ms = num_seconds * 1000
        n_frames = int(44100 * num_seconds)

        # create blank wave file to work with
        with wave.open('temp/temp_loop.wav', 'wb') as wvf:
            wvf.setparams((2,2,44100,n_frames,'NONE','not compressed'))
            wvf.writeframes(bytes([0] * n_frames * 2 * 2))
        
        # load it up in pydub
        empty = pydub.AudioSegment.from_file('temp/temp_loop.wav', format='wav')
        os.remove('temp/temp_loop.wav')
        ring_loops = []
        
        for ring_no in range(len(self.rings)):
            ring = self.rings[ring_no]
            loop = empty

            # 'tick' with each ring's frequency across the entire 'num_seconds' span
            for i in range(ring.freq):
                loop = loop.overlay(ring.segment, position=int(i*ms/ring.freq))
                        
            # if self.mult > 20:
            #     loop += 10
            
            filename = lambda prefix: str.format('temp/{}ring{}.wav', prefix, ring_no)

            if (self.mult > 1):
                # write a temp loop file
                loop.export(filename('temp'), format='wav')
                orig = wave.open(filename('temp'))
                new = wave.open(filename('temp2'), 'wb')

                # multiply the frame rate (this pitches up and increases speed)
                # but the pitch of the actual sample sounds on their own don't matter
                # we care about the increased frequency of amplitude peaks!
                new.setparams(orig.getparams())
                new.setframerate(orig.getframerate()*self.mult)
                new.writeframes(orig.readframes(orig.getnframes()))
                orig.close()
                new.close()
                os.remove(filename('temp'))
            
                # load up our faster file and downsample back to 44.1kHz
                # write to output
                y, s = librosa.load(filename('temp2'), sr=44100)
                os.remove(filename('temp2'))
                sf.write(filename(''), y, s)

                loop = pydub.AudioSegment.from_file(filename(''))

            ring_loops.append(loop)

            if (os.path.exists(filename(''))):
                # remove our last temp file for the next loop
                os.remove(filename(''))
    
        # remove temp folder
        shutil.rmtree('temp')

        # we need to divide the amount of silence - we could have 
        # set num_seconds to be shorter earlier in the code, but this
        # compromises quality of the sped up audio - better to increase framerate
        # and then resample
        output = empty[:len(empty)/self.mult]
        for loop in ring_loops:
            output = output.overlay(loop)
        
        ratio = seconds * int(len(empty)/len(output))
        ratio = 1 if ratio < 1 else int(ratio)

        result = (output * ratio, list(map(lambda x: x * ratio, ring_loops)))
        self.loop_cache[seconds] = result

        outfile = str.format('out/full{}.wav', seconds)
        result[0].export(outfile, format='wav')
        self.sound_cache[seconds] = Sound(outfile)
        return result

    def stop(self, seconds=1):
        self.pct = .125/2
        self.time = 0
        self.stopMusic(seconds)
        self.running = False
    
    def start(self, seconds=1):
        self.pct = 0
        self.running = True
        self.playMusic(seconds)

    def toggleMode(self):
        self.spinSpoke = not self.spinSpoke

    def update(self, ms):
        if self.running:
            # scale (1s unscaled loop) by multiplier
            self.time = (self.time + ms) % (1000 / self.mult)
            self.pct = self.time / (1000 / self.mult)

    def draw(self, canvas):

        # pct = ((self.pct * 100 - 33) % 100)/100
        # pct = ((self.pct * 100 - 25) % 100)/100
        pct = ((self.pct * 100 - 50) % 100)/100
        for ring in self.rings:
            ring.draw(pct, self.spinSpoke, canvas)

        length = (min(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)/20)*(len(self.rings))
        if self.spinSpoke:
            x, y = (Config.SCREEN_WIDTH/2 + length * math.cos(TWOPI * pct + 3*math.pi/8), 
                Config.SCREEN_HEIGHT/2 + length * math.sin(TWOPI * pct + 3*math.pi/8))
        else:
            x,y = (Config.SCREEN_WIDTH/2 + length * math.cos(0), 
               Config.SCREEN_HEIGHT/2 + length * math.sin(0))
        pygame.draw.line(canvas, Config.WHITE, Config.SCREEN_CENTER, (x,y))

    def withRing(self, freq, sound='default'):
        ring = Ring(freq, (min(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)/20)*(len(self.rings)+1), sound)
        self.rings += [ring]
        return self

    def stopMusic(self, seconds):
        self.getLoop(seconds)
        self.sound_cache[seconds].stop()

    def playMusic(self, seconds):
        self.getLoop(seconds)
        self.sound_cache[seconds].play(-1)
        # pya = pyaudio.PyAudio()

        # self.wv = wave.open('out/full10.wav', 'rb')
        # self.stream = pya.open(format=pya.get_format_from_width(self.wv.getsampwidth()), 
        #                 channels=self.wv.getnchannels(),
        #                 rate=self.wv.getframerate(),
        #                 output=True)

        

class Ring:
    def __init__(self, freq, r, sound_type='default'):
        self.freq = freq
        self.type = sound_type
        self.r = r
        self.file = str.format('sounds/{}', SOUNDS[sound_type])
        self.color = [Config.RED, Config.GREEN, Config.BLUE][random.randint(0,2)]
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

    def draw(self, beat_pct, spinSpoke, canvas):
        pygame.draw.circle(canvas, Config.WHITE, (400,400), self.r, 1)

        circ_ball_pct = 20 / math.pi * self.r * 2

        for i in range(self.freq):
            pct = i / self.freq
            pct = (pct - .25) % 1
            if spinSpoke:
                x, y = Config.SCREEN_CENTER[0] + self.r*math.cos(TWOPI * pct), Config.SCREEN_CENTER[1] + self.r*math.sin(TWOPI * pct)
            else:
                x, y = Config.SCREEN_CENTER[0] + self.r*math.cos(TWOPI * pct - ((beat_pct + .18)%1) * TWOPI), Config.SCREEN_CENTER[1] + self.r*math.sin(TWOPI * pct - ((beat_pct + .18)%1) * TWOPI)
            fill_color = self.color

            if ((pct - .15) * 100 - 5) % 100 < beat_pct * 100 and (((pct - .15) * 100 + 2) % 100 > beat_pct * 100 or ((pct - .15) * 100 + 5) % 100 < ((pct - .15) * 100 - 5) % 100):
                fill_color = (0,0,0)

            pygame.draw.circle(canvas, fill_color, (x, y), 10)

def createRing(json):
    return Ring(json['freq'], json['r'])