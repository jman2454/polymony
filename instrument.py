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
from pygame.mixer import Sound

SOUNDS = { 
    'default': 'hey.wav', 
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
                        
            if self.mult > 40:
                loop += 10
            
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

        outfile = str.format('full{}.wav', seconds)
        result[0].export(outfile, format='wav')
        self.sound_cache[seconds] = Sound(outfile)
        return result

    def update(self, ms):
        # inc = self.speed * (ms / 1000)
        self.time = (self.time + ms) % 1000
        self.pct = self.time / 1000
        # for ring in self.rings:
        #     if ring.doesNeedlePass(self.theta, inc):
        #         ring.play()

        # prev = self.theta
        # self.theta = (self.theta + inc) % TWOPI
        # if self.theta < prev:
        #     playsound.playsound('out.wav', block=False)

    def draw(self, canvas):
        for ring in self.rings:
            ring.draw(self.pct, canvas)

        length = 100*(len(self.rings))
        x, y = 400 + length*math.cos(TWOPI * self.pct + 2*math.pi/4), 400 + length*math.sin(TWOPI * self.pct + 2*math.pi/4)
        pygame.draw.line(canvas, (255,255,255), (400,400), (x,y))

    def withRing(self, freq, sound='default'):
        ring = Ring(freq, 100*(len(self.rings)+1), sound)
        self.rings += [ring]
        return self

    def playMusic(self, seconds):
        self.getLoop(seconds)
        self.sound_cache[seconds].play()

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

    def draw(self, beat_pct, canvas):
        pygame.draw.circle(canvas, (255,255,255), (400,400), self.r, 1)

        circ_ball_pct = 20 / math.pi * self.r * 2

        for i in range(self.freq):
            pct = i / self.freq
            x, y = 400 + self.r*math.cos(TWOPI * pct), 400 + self.r*math.sin(TWOPI * pct)
            fill_color = (255,255,255)

            if ((pct + 3) * 100 - 5) % 100 < beat_pct * 100 and ((pct + 3) * 100 + 5) % 100 > beat_pct * 100:
                print("YEE")
                fill_color = (0,0,0)

            pygame.draw.circle(canvas, fill_color, (x, y), 10)

def createRing(json):
    return Ring(json['freq'], json['r'])