from sineplotter import PlotterMovieWriter, PhasePlotter, FunctionPlotter
import numpy as np

period = 4
axis_length = period * 2

PlotterMovieWriter(frames = 300, fps=5) \
    .writeMovie("sine.mp4",
        PhasePlotter(axis_length = axis_length) \
            .addSine(amp = 1.5, phase = -np.pi/4, period = period, color = 'r')
            .addSine(amp = 2.5, phase =     0   , period = period, color = 'g')
            .addSine(amp = 2.25,phase =  np.pi/2, period = period, color = 'b')
            .addFunction(FunctionPlotter(label = "x / 4", f = lambda x: x / 4, color="c" ))
            )