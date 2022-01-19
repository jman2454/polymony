# import tkinter
from instrument import Instrument, Ring
import playsound
import os
import shutil

class App:
    def __init__(self, config=None, frame_rate=60):
        self.rate = int(1000.0 / frame_rate)
        self.instruments = []
        # self.tk = tkinter.Tk()

        if config:
            pass
        else:
            self.instruments = [
                Instrument(1)
                    .withRing(Ring(8, 3, 'click'))
                    .withRing(Ring(10, 3, 'click'))
                    .withRing(Ring(12, 3, 'click'))
                    .withRing(Ring(15, 3, 'click')),
                Instrument(100)
                    .withRing(Ring(20, 3, 'click'))
                    .withRing(Ring(24, 3, 'click'))
                    .withRing(Ring(30, 3, 'click'))
                    .withRing(Ring(35, 3, 'click')),
                Instrument(1)
                    .withRing(Ring(12, 3, 'tick'))
                    .withRing(Ring(2, 3, 'snare'))
                    .withRing(Ring(6, 3, 'snare'))
                    .withRing(Ring(8, 3, 'block'))
                    .withRing(Ring(4, 3, 'kick'))
                    .withRing(Ring(15, 3, 'click')),
                Instrument(80)
                    .withRing(Ring(12, 3, 'tick'))
                    .withRing(Ring(2, 3, 'snare'))
                    .withRing(Ring(6, 3, 'snare'))
                    .withRing(Ring(8, 3, 'block'))
                    .withRing(Ring(4, 3, 'kick'))
                    .withRing(Ring(15, 3, 'click'))
            ]

    def loop(self):
        for ins in self.instruments:
            ins.update(self.rate)
        # self.tk.after(self.rate, self.loop)

    def start(self):
        # self.tk.after(self.rate, self.loop)
        if os.path.exists('out'):
            shutil.rmtree('out')
        os.mkdir('out')

        for i in range(len(self.instruments)):
            full, loops = self.instruments[i].generateLoop(10)
            instrument_path = str.format('out/instrument{}/', i)
            os.mkdir(instrument_path)
            full.export(instrument_path + 'full.wav', format='wav')
            for n in range(len(loops)):
                loops[n].export(str.format('{}ring{}.wav', instrument_path, n), format='wav')
        # self.tk.mainloop()
        # playsound.playsound('out.wav')