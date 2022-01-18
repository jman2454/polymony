import tkinter
from instrument import Instrument, Ring
import playsound

class App:
    def __init__(self, config=None, frame_rate=60):
        self.rate = int(1000.0 / frame_rate)
        self.instruments = []
        self.tk = tkinter.Tk()

        if config:
            pass
        else:
            self.instruments = [
                Instrument(1)
                    .withRing(Ring(12, 3, 'tick'))
                    .withRing(Ring(2, 3, 'snare'))
                    .withRing(Ring(6, 3, 'snare'))
                    .withRing(Ring(8, 3, 'block'))
                    .withRing(Ring(4, 3, 'kick'))
                # ,
                # Instrument(1)
                #     .withRing(Ring(12, 3, 'tick'))
                #     .withRing(Ring(2, 3, 'snare'))
                #     .withRing(Ring(6, 3, 'snare'))
                #     .withRing(Ring(8, 3, 'block'))
                #     .withRing(Ring(4, 3, 'kick'))
                # Instrument(200)
                #     .withRing(Ring(1, 3, 'kick'))
                    # .withRing(Ring(3, 3, 'kick'))
            ]

    def loop(self):
        for ins in self.instruments:
            ins.update(self.rate)
        self.tk.after(self.rate, self.loop)

    def start(self):
        self.tk.after(self.rate, self.loop)
        for ins in self.instruments:
            ins.generateLoop(1)
        # self.tk.mainloop()
        # playsound.playsound('out.wav')