import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from numpy import arange,pi

class SinePlotter:

    def __init__(self, phase, amp, period, color):
        self.phase = phase
        self.color = color
        self.amp = amp
        self.period = period

    def angularVelocity(self):
        return 2 * pi / self.period

    def xAxisToRad(self, xAxisPos):
        return xAxisPos * self.angularVelocity() + self.phase

    def radToComplex(self, xAxisPos):    
        radians = self.xAxisToRad(xAxisPos)
        return (self.amp * np.cos(radians), 
                self.amp * np.sin(radians))
        
    def drawPhaseIntoCircle(self, xAxisPos, startCircle):
        (real_part, imaginary_part) = self.radToComplex(xAxisPos)
        # Adjust real part because center if circle is shifted
        real_part_shifted = startCircle + real_part #(real_part - self.amp)
        plt.plot((startCircle, real_part_shifted, xAxisPos     , xAxisPos), 
                 (     0     , imaginary_part   , imaginary_part,    0     ), 
                 self.color + ':' , linewidth=1)

    def sin(self, array):
        return self.amp * np.sin( self.angularVelocity() * array + self.phase)

    def drawCircle(self, centerCircle):
        patch= plt.Circle((centerCircle, 0), 
                          fill=False, radius= self.amp, 
                          color=self.color, linestyle="--")
        plt.gca().add_patch(patch)
        plt.axis('scaled')

    def describe(self, textVertPos, textHorPos, xAxisPos):
        radians = self.xAxisToRad(xAxisPos)
        angleRad = self.xAxisToRad(xAxisPos) % (2 * pi)
        yAxisPos = self.amp * np.sin(radians)

        staticProperties = [
            f"velocity={self.angularVelocity():.2f} rad/sec",
            f"amp={self.amp:.2f}"
            f"phase={self.phase:.2f}"
        ]
        dynamicProperties = [
            f"angle={angleRad:.2f} rad",
            f"x={xAxisPos:.2f}",
            f"y={yAxisPos:.2f}"
        ]
        plt.text(textHorPos, textVertPos, 
            f"{', '.join(dynamicProperties)}, ({', '.join(staticProperties)})",
            horizontalalignment='left', 
            verticalalignment='center',
            color=self.color,
            size="8")

    def draw(self, xAxisPos, startCircle):
        arrayUntilXPos = arange(0,xAxisPos,0.01)
        plt.plot(arrayUntilXPos, self.sin(arrayUntilXPos), 
                 self.color, linewidth=0.75)
        self.drawCircle(startCircle)
        self.drawPhaseIntoCircle(xAxisPos, startCircle)

class FunctionPlotter:
    
    def __init__(self,label,f, color="b"):
        self.label = label
        self.f = f
        self.color = color
    
    def draw(self, xAxisPos, startCircle):
        arrayUntilXPos = arange(0,xAxisPos,0.01)
        plt.plot(arrayUntilXPos, self.f(arrayUntilXPos), 
                 self.color, linewidth=0.75)
    
    def describe(self, textVertPos, textHorPos, xAxisPos):
        plt.text(textHorPos, textVertPos, 
            f"{self.label}",
            horizontalalignment='left', 
            verticalalignment='center',
            color=self.color,
            size="8")
class PhasePlotter:

    def __init__(self, axis_length):
        self.amp = 0
        self.axis_length = axis_length
        self.functionPlotters = []
        self.center_circle = 0

    def updateAmp(self, amp):
        if amp > self.amp:
            self.amp = amp
            self.center_circle = -1 * self.amp

    def addFunction(self, f):
        self.functionPlotters.append(f)
        return self

    def addSine(self, amp, phase, period, color = 'r'):
        self.updateAmp(amp)
        self.functionPlotters.append(SinePlotter(phase, amp, period, color))
        return self
    
    def drawXYAxis(self):
        plt.plot([0,0], [self.amp,-self.amp], color="k")
        plt.plot([self.center_circle, self.axis_length], [0, 0], color = "k" )

    def removeXYLabels(self):
        plt.gca().set_yticklabels([])    
        plt.gca().set_xticklabels([])
    
    def draw(self, pos_pct):
        pos = self.axis_length * pos_pct
        self.drawXYAxis()
        plt.xticks(arange(self.axis_length + 1))    
        # self.removeXYLabels()
        for count, sine in enumerate(self.functionPlotters):
            sine.draw(pos, self.center_circle)
            textPos = self.amp + 1 + count / 2
            sine.describe(textPos, self.center_circle * 2, pos)

class PlotterMovieWriter:
    
    def __init__(self, frames=200, fps=15):
        self.frames = frames
        self.fps = fps
    
    def writeMovie(self, file_name, p):
        FFMpegWriter = manimation.writers['ffmpeg']
        writer = FFMpegWriter(fps=self.fps)
        fig = plt.figure()

        with writer.saving(fig, file_name, 100):
            for i in range(self.frames):
                plt.gcf().clear()
                p.draw((float(i)  / float(self.frames)))
                writer.grab_frame()