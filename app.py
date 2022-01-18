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
            self.instruments.append(
                Instrument()
                    # .withRing(Ring(3, 3, 'tick'))
                    .withRing(Ring(2, 3, 'kick'))
                    # .withRing(Ring(3, 3, 'kick'))
                    # .withRing(Ring(8, 3, 'kick'))
                    # .withRing(Ring(8, 3, 'tick'))
                    # .withRing(Ring(6, 3, 'closed'))
                )

    def loop(self):
        for ins in self.instruments:
            ins.update(self.rate)
        self.tk.after(self.rate, self.loop)

    def start(self):
        self.tk.after(self.rate, self.loop)
        for ins in self.instruments:
            ins.generateLoop(10000)
        # self.tk.mainloop()
        # ins = Instrument()
        # if val.isnumeric():
        #     ins = ins.withRing(Ring(int(val),3,'kick'))
        # else:
        #     if val == 'p':
        #         ins.generateLoop(1000)
        playsound.playsound('out.wav')

        # os.remove('out.wav')