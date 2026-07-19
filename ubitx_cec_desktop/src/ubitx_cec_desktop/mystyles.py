# --------------------
# This file is used for defining Ttk styles.
# Use the 'style' object to define styles.

# Pygubu Designer will need to know which style definition file
# you wish to use in your project.

# To specify a style definition file in Pygubu Designer:
# Go to: Edit -> Preferences -> Ttk Styles -> Browse (button)

# In Pygubu Designer:
# Assuming that you have specified a style definition file,
# - Use the 'style' combobox drop-down menu in Pygubu Designer
#   to select a style that you have defined.
# - Changes made to the chosen style definition file will be
#   automatically reflected in Pygubu Designer.
# --------------------

# import tkinter as tk
import tkinter.ttk as ttk

#import sv_ttk

def setup_ttk_styles(master=None):
    
    style = ttk.Style(master)
    style.theme_use('default')

    fontList = {
            'Heading0b': ('Arial', 24, 'bold'),
            'Heading1b': ('Arial', 20, 'bold'),
            'Heading2b': ('Arial',14, 'bold' ),
            'Heading3b': ('Arial',12, 'bold' ),
            'Heading4b': ('Arial',10, 'bold' ),
            'Heading5': ('Fixed', 6),
            'HeadingVFO': ("TkFixedFont",96, 'bold' )
        }


    style.configure('Heading1b.TLabel', font=fontList['Heading1b'], background='gray', foreground='white')
    style.map('Heading1b.TLabel', background=[('disabled', 'gray')], foreground=[('disabled', 'white')])
    style.configure('Heading2b.TLabel',font=fontList['Heading2b'], foreground='white', background="gray")
    style.configure('Heading3b.TLabel',font=fontList['Heading3b'], background='gray', foreground='white')
    style.configure('Heading4b.TLabel',font=fontList['Heading4b'], background='gray', foreground='white')

    style.configure('VFO.TLabel',font=fontList['HeadingVFO'], background='gray', foreground='white')
    style.configure('Heading3bRed.TLabel', font=fontList['Heading3b'], background='red', foreground='white')
    style.configure('Heading3bGreen.TLabel', font=fontList['Heading3b'], background='green', foreground='white')
    style.configure('OffLED.TLabel', font=fontList['Heading5'], background='gray', foreground='gray')
    style.configure('OnLED.TLabel', font=fontList['Heading5'], background='green', foreground='green')


    style.configure('Button0bRaised.TButton', font=fontList['Heading0b'], justify='center', relief='raised')
    style.configure('Button0bPressed.TButtoΩn', font=fontList['Heading0b'], justify='center', relief='sunken')
    style.configure('Button1bRaised.TButton', font=fontList['Heading1b'], justify='center', relief='raised')
    style.configure('Button1bPressed.TButton', font=fontList['Heading1b'], justify='center', relief='sunken')
    style.configure('RedButton1bPressed.TButton', font=fontList['Heading1b'], background='red', foreground='white',
                    anchor="center", relief='sunken')
    style.configure('GreenButton1bPressed.TButton', font=fontList['Heading1b'], background='green', foreground='white',
                    justify='center', relief='sunken')
    style.configure('Button2bRaised.TButton', font=fontList['Heading2b'], justify='center', relief='raised')
    style.configure('Button2bPressed.TButton', font=fontList['Heading2b'], justify='center', relief='sunken')


    style.configure('Custom.Toolbutton', font=fontList['Heading3b'], background='gray', foreground='black')

    style.configure('Heading1b.TMenubutton', font=fontList['Heading1b'], anchor='center')

    style.configure('Checkbox1b.TCheckbutton', font=fontList['Heading1b'], background='gray', foreground='white')

    style.configure('Entry1b.TEntry', font=fontList['Heading0b'])

    style.configure('Heading1b.TLabelframe', background='gray', bd=4)
    style.configure('Heading1b.TLabelframe.Label', background='gray', bd=4, font=fontList['Heading1b'])

    style.configure('Heading2b.TLabelframe', background='gray', bd=4)
    style.configure('Heading2b.TLabelframe.Label', background='gray', bd=4, font=fontList['Heading2b'])

    style.configure('GreenBox.TLabelframe', background='green', bd=4)
    style.configure('GreenBox.TLabelframe.Label', background='green', foreground='white', bd=4, font=fontList['Heading1b'])
    style.configure('GreenBox.TLabel', font=('Fixed', 24, 'bold'), background='green', bd=0)
    style.configure('GreenBoxi.TLabel', font=('Fixed', 24, 'italic'), background='green', bd=0)


    style.configure('Normal.TFrame', background='gray', bd=4)
    style.configure('NormalOutline.TFrame', background='gray', bd=4, bordercolor='white' ,relief='groove')


    style.configure("Striped.Horizontal.TProgressbar",
                troughcolor='lightgray',  # Color of the empty part of the bar
                background='red',  # Color of the progress indicator,
                thickness=25)  # Height/width of the bar (depending on orientation)

    style.configure("Custom.TSpinbox",
                    background="gray",
                    foreground="black",
                    arrowsize=50)

    style.map('Custom.Horizontal.TScale',
                    foreground=[('disabled', 'gray'),('!disabled', 'blue')],
                    troughcolor=[('disabled', 'gray'), ('!disabled', 'black')],
                    background=[('disabled', 'gray'), ('!disabled', 'gray')])


    #style.configure('Normal.TLabelframe', background='gray', bd=4, font=fontList['Heading1b'])
    # style.configure('Normal.TLabelframe.Label', background='gray', bd=4, font=fontList['Heading3b'])

    # style.configure('Normal.TFrame', background='gray', bd=4, font=fontList['Heading1b'])
    # style.configure('RedButton1bRaised.TButton', font=fontList['Heading1b'], background='red', foreground='white',
    #                 anchor="center", relief='raised')
    # style.configure('GreenButton1bRaised.TButton', font=fontList['Heading1b'], background='green', foreground='white',
    #                 justify='center', relief='raised')
    # style.configure('Heading1.TLabel', font=fontList['Heading0b'], background='gray', foreground='white')
    # style.configure('Heading2.TLabelframe.Label', background='gray', bd=4, font=fontList['Heading1b'])
    # style.configure('Heading2.TLabelframe', background='gray', bd=4)
    # style.configure('Heading3.TLabelframe.Label', background='gray', bd=4, font=fontList['Heading2b'])
    # style.configure('Heading3.TLabelframe', background='gray', bd=4)

    # style.configure('Entry2b.TEntry', font=fontList['Heading1b'])
    # style.configure('Checkbox2b.TCheckbutton', font=fontList['Heading2b'], background='gray', foreground='white')

    # style.configure('Heading0.TMenubutton', font=fontList['Heading0b'], anchor='center')
    # style.configure('Heading1n.TMenubutton', font=fontList['Heading1n'], anchor='center')
    # style.configure('Heading2b.TMenubutton',font=fontList['Heading2b'])

    # style.configure('Heading1bi.TLabel', font=fontList['Heading1bi'], background='gray', foreground='white')
    # style.configure('Heading3.TLabel',font=fontList['Heading3b'])
    # style.configure('Heading2.TLabel',font=fontList['Heading1b'
    # style.configure('Heading2bi.TLabel', font=fontList['Heading2bi'], background='gray', foreground='white')
    #
    # style.configure('Heading1.TLabel',font=fontList['Heading0b'
    # style.configure('Heading1Fixed.TLabel',font=fontList['Heading0b'

    # style.configure('Heading3bi.TLabel', font=fontList['Heading3i'], background='gray', foreground='white')
    # style.configure('Heading2b.TLabel', font=fontList['Heading2b'], foreground='white', background="gray",
    #                 fieldbackground=[("normal", "gray"), ("disabled", "gray")])
    # style.configure('GreenLED3.TLabel',font=fontList['Heading3b'], background='green', foreground='white')
    # style.configure('Heading4bRed.TLabel', font=fontList['Heading4'], background='red', foreground='white')
    # style.configure('Button2Sunken.TButton', font=fontList['Heading2b'], justify='center', relief='sunken')

    # style.configure('Heading3Black.TLabel',font=fontList['Heading3b'],background='gray', foreground='black')
    # style.configure('Heading4.TLabel',font=fontList['Heading4'], background='gray', foreground='white')
    # style.configure('Symbol1.TLabel',font=fontList['Symbol1'])
    # style.configure('RedLED.TLabel', font=fontList['Heading1b'], background='red', foreground='white')
    # style.configure('GreenLED.TLabel', font=fontList['Heading1b'], background='green', foreground='white')
    # style.configure('Normal.TLabel',font=fontList['Normal'])
    # style.configure('RedButton2b.TButton',font=fontList['Heading2b'], background='red', foreground='white',anchor="center", relief='raised')
    # style.configure('GreenButton2b.TButton', font=fontList['Heading2b'], background='green', foreground='white',justify='center', relief='raised')

    # style.configure('Button1.TButton',font=fontList['Heading0b'])
    #   style.configure('DarkButton3.TButton',font=fontList['Heading3b'], background='black', foreground='white', boarderwidth=5, relief='raised')
    #    style.configure('Button4.TButton',font=fontList['Heading4'])
    #    style.configure('Button3Blue.TButton',font=fontList['Heading3b'], foreground='blue')
    #    style.configure('Normal.TButton',font=fontList['Normal'])
    #    style.configure('Symbol1.TButton',font=fontList['Symbol1'])
    #    style.configure('Symbol3.TButton',font=fontList['Symbol3'])
    #    style.configure('ButtonEmphasis.TButton',font=fontList['Emphasis'])

    # style.configure('Button2.TButton',font=fontList['Heading1b'])
    # style.configure('Button2b.TButton',font=fontList['Heading2b'], justify='center',anchor="center")

    # style.configure('Button3.TButton',font=fontList['Heading3b'],)
    # style.configure('Button3Pressed.TButton', font=fontList['Heading3b'],relief='sunken', background='darkgray')
    # style.configure('Button3Raised.TButton', font=fontList['Heading3b'], relief='raised')

    # style.configure('RadioButton4.TRadiobutton',font=fontList['Heading4'])
    # style.configure('RadioButtonNormal.TRadiobutton',font=fontList['Normal'])
    # style.configure('RadioButtonEmphasis.TRadiobutton',font=fontList['Emphasis'])
    # style.configure('Button2bipressed.TButton', relief='sunken', font=fontList['Heading2bi'], justify='center')
    # style.configure('Button2bcentered.TButton', font=fontList['Heading2b'],justify='center')
    # style.configure('Button1bARaised.TButton', font=fontList['Heading1b'], relief='raised')
    # style.configure('Button1bAPressed.TButton', font=fontList['Heading1b'], relief='sunken')
    # style.configure('Button1Sunken.TButton', font=fontList['Heading0b], relief='sunken')

    # style.configure('Checkbox3.TCheckbutton',font=fontList['Heading3b'])
    # style.configure('Checkbox4.TCheckbutton',font=fontList['Heading4'])
    # style.configure('CheckboxNormal.TCheckbutton',font=fontList['Normal'])
    # style.configure('CheckboxNormalNoBorder.TCheckbutton',font=fontList['Normal'],highlightthickness=0, borderwidth=0, bd=0)
    # style.configure('CheckboxEmphasis.TCheckbutton',font=fontList['Emphasis'])
    
    # style.configure('RadioButton3.TRadiobutton',font=fontList['Heading3b'])

    # style.configure('TCombobox', font=fontList['Heading0'])

    # style.configure('OptionMenu1b.TOptionMenu', font=fontList['Heading1b'], anchor='center')

    # style.configure('ComboBox1.TCombobox', font=fontList['Heading2b'], arrowsize=50, relief='raised')
    # style.configure('ComboBox1.TCombobox.Listbox', font=fontList['Heading1b'])

    # style.configure('ComboBox2.TCombobox',font=fontList['Heading1b'])
    # style.configure('ComboBox2b.TCombobox', font=fontList['Heading2b'])
    # style.configure('ComboBox3.TCombobox', font=fontList['Heading3b'])
    # style.configure('ComboBox4.TCombobox',font=fontList['Heading4'])
    # style.configure('ComboBox4White.TCombobox',font=fontList['Heading4'],foreground='white')
    # style.configure('Normal.TEntry',font=fontList['Normal'])

    # style.configure('Entry3b.TEntry', font=fontList['Heading3b'])
    # style.configure('Entry2bCopy.TEntry', font=fontList['Heading1b'],highlightthickness=0, borderwidth=0, background='red', readonlybackground='red',bd=0)
    # style.configure('NoBorder.TEntry',font=fontList['Normal'], highlightthickness=0, borderwidth=0, bd=0)

    # style.configure('Title.TFrame', background='blue', foreground='white')

    # style.configure('Normal.TText', background='gray', foreground='white', font=fontList['Heading3b'])

    # style.configure('Highlight.TFrame', background='blue', bd=4 )
    #   style.configure('Dark.TFrame', background='black', bd=4, bordercolor='white')
    # style.configure('Submenu.TMenuitem.Command',font=fontList['Heading2b'])
    # style.configure('WarningOutline.TFrame', background='red', bd=4, bordercolor='white', relief='groove')

    # style.configure('Fixed.TNotebook')
    # style.configure('Fixed.TNotebook.Tab',padding=[5,2])
    # style.configure('Red.TSeparator', background='red', height=25)