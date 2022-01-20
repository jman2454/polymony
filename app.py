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
                Instrument(60).withRing(2, 'kick').withRing(3, 'snare').withRing(6,'click').withRing(4,'closed')
                # Instrument(1).withRing(8,'click').withRing(10,'click').withRing(12,'click').withRing(15,'click'),
                # Instrument(10).withRing(8,'click').withRing(10,'click').withRing(12,'click').withRing(15,'click'),
                # Instrument(50).withRing(8,'click').withRing(10,'click').withRing(12,'click').withRing(15,'click')

                # Instrument(100).withRing(4, 'click').withRing(5, 'click').withRing(6, 'click'),
                # Instrument(50).withRing(3, 'click'),
                # Instrument(100).withRing(3, 'click').withRing(5, 'click'),
                # Instrument(50).withRing(5, 'click').withRing(8, 'click'),
                # Instrument(76).withRing(3, 'click').withRing(5, 'click'),
                # Instrument(67).withRing(3, 'click').withRing(5, 'click'),
                # Instrument(67).withRing(5, 'click').withRing(8, 'click'),
                # Instrument(100).withRing(3, 'click').withRing(5, 'click')
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

        for i in range(len(self.instruments)):
            instrument_path = str.format('out/instrument{}/', i)
            playsound.playsound(instrument_path + 'full.wav')

        # self.tk.mainloop()
        # playsound.playsound('out.wav')