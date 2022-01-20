from instrument import Instrument, Ring
from pygame.time import Clock
import playsound
import os
import shutil
import pygame

class App:

    FRAME_RATE = 60

    def __init__(self, config=None, frame_rate=60):
        self.rate = int(1000.0 / frame_rate)
        self.instruments = []
        
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        self.screen.fill((50,50,50))
        pygame.display.flip()
        self.clock = Clock()
        # self.tk = tkinter.Tk()

        if config:
            pass
        else:
            self.instruments = [
                # Instrument(1).withRing(1, 'kick').withRing(2, 'snare'),
                # Instrument(1).withRing(1, 'kick').withRing(3).withRing(6, 'closed').withRing(2, 'snare'),
                # Instrument(1).withRing(1, 'kick').withRing(3).withRing(6, 'closed').withRing(2, 'snare').withRing(12, 'click').withRing(15,'tick'),
                # Instrument(.4).withRing(4, 'snare').withRing(5,'snare').withRing(6,'snare'),
                # Instrument(1).withRing(4, 'snare').withRing(5,'snare').withRing(6,'snare'),
                # Instrument(50).withRing(4, 'snare').withRing(5,'snare').withRing(6,'snare'),
                # Instrument(100).withRing(4, 'snare').withRing(5,'snare').withRing(6,'snare')
                # Instrument(1).withRing(2,'kick'),
                Instrument(1).withRing(2, 'kick').withRing(3, 'snare').withRing(6, 'tick'),
                Instrument(.5).withRing(8, 'closed').withRing(12, 'tick').withRing(15, 'click'),
                Instrument(25).withRing(8, 'closed').withRing(12, 'tick').withRing(15, 'click'),
                Instrument(50).withRing(8, 'closed').withRing(12, 'tick').withRing(15, 'click')
                # ,
                # Instrument(70).withRing(2).withRing(3),
                # Instrument(.25).withRing(4).withRing(6).withRing(12).withRing(8).withRing(15).withRing(18),
                # Instrument( 40).withRing(4).withRing(6).withRing(12).withRing(8).withRing(15).withRing(18),
                # Instrument(1).withRing(8).withRing(10).withRing(12).withRing(15),
                # Instrument(25).withRing(8).withRing(10).withRing(12).withRing(15),
                # Instrument(50).withRing(8).withRing(10).withRing(12).withRing(15),
                # Instrument(100).withRing(4).withRing(5).withRing(6),
                # Instrument(50).withRing(3),
                # Instrument(100).withRing(3).withRing(5),
                # Instrument(50).withRing(5).withRing(8),
                # Instrument(75).withRing(3).withRing(5),
                # Instrument(66).withRing(3).withRing(5),
                # Instrument(66).withRing(5).withRing(8),
                # Instrument(100).withRing(3).withRing(5),
                # Instrument(44).withRing(10).withRing(12).withRing(15),
                # Instrument(100).withRing(4).withRing(5).withRing(6),
                ]
            # self.instruments = [Instrument(100).withRing(4).withRing(5).withRing(6)]

    def loop(self):
        for ins in self.instruments:
            ins.update(self.rate)
        # self.tk.after(self.rate, self.loop)

    def animate(self, instrument):
        # time = 0
        pygame.draw.rect(self.screen, (255,0,0), (400, 400, 20, 20),0)

        delta = 0
        running = True
        # playsound.playsound('out/instrument0/full.wav', block=False)

        instrument.playMusic(10)
        while running:
            # prev_time = time
            # time = (time + delta) % 1000
            instrument.update(delta)
            self.screen.fill((50,50,50))
            instrument.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
            delta = self.clock.tick(App.FRAME_RATE)

        pygame.quit()
            

    def start(self):
        # self.tk.after(self.rate, self.loop)
        if os.path.exists('out'):
            shutil.rmtree('out')
        os.mkdir('out')

        f = None
        for i in range(len(self.instruments)):
            full, loops = self.instruments[i].getLoop(10)
            if f is None:
                f = full
            for ring in loops:
                instrument_path = str.format('out/instrument{}/', i)
                if (os.path.exists(instrument_path)):
                    shutil.rmtree(instrument_path)
                os.mkdir(instrument_path)
                # full.export(instrument_path + 'full.wav', format='wav')
                for n in range(len(loops)):
                    loops[n].export(str.format('{}ring{}.wav', instrument_path, n), format='wav')

        # for i in range(len(self.instruments)):
        #     instrument_path = str.format('out/instrument{}/', i)
        #     playsound.playsound(instrument_path + 'full.wav')

        self.animate(self.instruments[0])

        # self.tk.mainloop()
        # playsound.playsound('out.wav')