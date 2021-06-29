import PySimpleGUI as sg
from acti_scoring import find_valid_days

sg.theme("DarkGrey13")
layout = [
    [sg.T("Valid Days Calculator - Actigraphy")], 
    [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-"), sg.Button("Submit")], 
    [sg.MLine(size=(80,10), key='result')]
]
window = sg.Window(title="Actigraphy Valid Days Calculator", layout=layout, margins=(100, 50))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit":
        valid_days, log_str = find_valid_days(values["-IN-"])

        result_str = f"{log_str}\nValid Dates: "
        for date in valid_days:
            result_str += f"{date}, "
        result_str = result_str[:-2]

        result_str += f"\nNumber of Valid Days: {len(valid_days)}"
        window['result'].update(result_str)

