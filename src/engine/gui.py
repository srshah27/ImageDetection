import sys
sys.path.append('D:\\Projects\\ImageDetection\\Lib\\site-packages')

from tkinter import CENTER
import PySimpleGUI as sg
from PIL import Image
import integrated

# from Trimmed_SizeWithAruco import *
from os.path import basename

gotImage = False
"""
Checks if image is taken
"""

newpath = ""

# sg.theme_previewer()
sg.theme("DarkBlue")
# sg.theme('DarkAmber')

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Image(key="-IMAGE-", filename="C:/Users/dusng/Documents/GitHub/image-size-detection/gui/1.png", size=(600, 500))],
    # [sg.Image(data=png_data, key="-ArtistAvatarIMG-")],
]

button_column = [
    [
        # sg.In(key="-PATH-",enable_events=True),
        # sg.FileBrowse("Choose",key="-FILE-",enable_events=True),
        sg.In(size=(10, 1), enable_events=True, key="-FILE-", text_color="yellow"),
        sg.FileBrowse("Choose Image"),
        # sg.Button(button_text='Capture Image', tooltip='Captures the image'),
        sg.Button(button_text="Run", tooltip="Runs the code", size=(10, 1)),
        sg.Button(button_text="Exit", tooltip="Exits the program"),
    ]
]
text_column = [
    [
        sg.Text(
            key="-STATUS-",
            text="Press the Capture Image button",
            auto_size_text=True,
            background_color="LightBlue",
            text_color="black",
            justification="center",
        )  # , pad=((60, 0), (0, 0)))
    ]
]
# ----- Full layout -----
layout = [
    [sg.Column(button_column, element_justification="c", justification="center")],
    [sg.Column(image_viewer_column, expand_x=True, element_justification="c")],
    [
        sg.Column(
            text_column,
            element_justification="c",
            pad=((0, 0), (20, 0)),
            justification="center",
            expand_x=True,
        )
    ],
]


window = sg.Window(
    "Dimension Finder",
    layout,
    return_keyboard_events=True,
    size=(600, 630),
    location=(sg.Window.get_screen_size()[0] // 4, 0),
    finalize=True,
    use_default_focus=False,
)


# Run the Event Loop
while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-FILE-":
        print("Path: ", basename(values["-FILE-"]))
        # print("Path: ",values["-FILE-"])
        window["-FILE-"].update(basename(values["-FILE-"]))

        if (values["-FILE-"]).lower().endswith((".png", ".jpg", ".jpeg")):
            newpath = values["-FILE-"]
            print("heee", newpath)

        if newpath == "":
            window["-IMAGE-"].update(filename="gui/noimg.png", size=(600, 500))

        # elif event == 'Capture Image':
        else:
            window["-STATUS-"].update("Capturing Image", background_color="LightBlue")
            window.refresh()

            image = integrated.TakeImg(newpath)

            # image = Image.open(r'trimtest_temp.png')
            base_width = 720
            width_percent = base_width / float(image.size[0])
            hsize = int((float(image.size[1]) * float(width_percent)))
            image = image.resize((base_width, hsize), Image.ANTIALIAS)
            image.save("trimtest_temp.png")

            gotImage = True

            window["-STATUS-"].update(
                "Press the Run button to get measurements\nPress Capture Image to retake the image"
            )
            window["-IMAGE-"].update(filename="trimtest_temp.png", size=(600, 500))
            window.refresh()

    elif event == "Run":
        if gotImage == False:
            window["-STATUS-"].update("Capture image first", background_color="red")
            window.refresh()
        else:
            window["-STATUS-"].update("Calculating... please wait")
            window.refresh()
            # todo show loading symbol
            # runCode.measure()  # Run the code
            integrated.calculate()
            exit(0)
            # todo hide loading symbol

            # image = Image.open(r"trimtest.png")

            # base_width = 720
            # width_percent = base_width / float(image.size[0])
            # hsize = int((float(image.size[1]) * float(width_percent)))
            # image = image.resize((base_width, hsize), Image.ANTIALIAS)
            # image.save("trimtest_compressed.png")

            # window["-IMAGE-"].update(
            #     filename="trimtest_compressed.png", size=(500, 500)
            # )
            # window["-STATUS-"].update("Done !")
            # window.refresh()

            # gotImage = False


window.close()
