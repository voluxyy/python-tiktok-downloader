import tkinter as ttk 

class gui:
    # This are the colors options for tk_setPalette's method: 
    # activeBackground, foreground, selectColor, activeForeground, highlightBackground, selectBackground, background, highlightColor, selectForeground, disabledForeground, insertBackground, troughColor
    def __init__(self, foreground, background, activeForeground, activeBackground) -> None:
        self.foreground = foreground
        self.background = background
        self.activeForeground = activeForeground
        self.activeBackground = activeBackground

    