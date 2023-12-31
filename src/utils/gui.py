import tkinter as ttk 

class Gui:
    # This are the colors options for tk_setPalette's method: 
    # activeBackground, foreground, selectColor, activeForeground, highlightBackground, selectBackground, background, highlightColor, selectForeground, disabledForeground, insertBackground, troughColor
    def __init__(self, foreground="black", background="white", activeForeground="white", activeBackground="black") -> None:
        """
        ### Description
        *Init a gui instance to create a tkinter app.
        
        ---
        ### Parameters
        @param foreground: Foreground color.
        @param background: Background color.
        @param activeForeground: Active foreground color.
        @param activeBackground: Active background color.
        """
        self.color = {
            'foreground': foreground,
            'background': background,
            'activeForeground': activeForeground,
            'activeBackground': activeBackground
        }
        """
        Next variables to use for color:
            'text': "",
            'background': "",
            'button-background': "",
            'button-shadow': "",
            'button-hover': "",
        """


    # Methods to add tkinter module
    def Window(self) -> ttk.Tk:
        window = ttk.Tk()
        window.tk_setPalette(
            foreground= self.color['foreground'],
            background= self.color['background'],
            activeforeground= self.color['activeForeground'],
            activebackground= self.color['activeBackground']
        )
        return window
    

    def Frame(self, master, column, row) -> ttk.Frame:
        frame = ttk.Frame(
            master= master,
        )
        frame.grid(
            column=column,
            row=row
        )
        return frame


    def Label(self, master, text, column, row, *, fg=None, bg=None, aFg=None, aBg=None) -> ttk.Label:
        label = ttk.Label(
            text= text,
            master= master,
            foreground= fg if fg is not None else self.color['foreground'],
            background= bg if bg is not None else self.color['background'],
            activeforeground= aFg if aFg is not None else self.color['activeForeground'],
            activebackground= aBg if aBg is not None else self.color['activeBackground']
        )
        label.grid(
            column=column,
            row=row
        )
        return label
    

    def Entry(self, master, column, row, *, fg=None, bg=None, aFg=None, aBg=None) -> ttk.Entry:
        entry = ttk.Entry(
            master=master,
            foreground= fg if fg is not None else self.color['foreground'],
            background= bg if bg is not None else self.color['background']
        )
        entry.grid(
            column=column,
            row=row
        )
        return entry


    def Button(self, master, text, command, column, row, *, fg=None, bg=None, aFg=None, aBg=None) -> None:
        button = ttk.Button(
            text= text,
            master= master,
            command=command,
            foreground= fg if fg is not None else self.color['foreground'],
            background= bg if bg is not None else self.color['background'],
            activeforeground= aFg if aFg is not None else self.color['activeForeground'],
            activebackground= aBg if aBg is not None else self.color['activeBackground']
        )

        button.grid(
            column=column,
            row=row
        )

        return button


    def Menu(self, master) -> ttk.Menu:
        return ttk.Menu(master=master)