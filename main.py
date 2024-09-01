import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
import time

# Set a second for disappearing the texts
COUNT_DOWN_SEC = 5
# The default color hex code
FG_COLOR_RESET = "#000000"

# Initialize the variables last_texts and cnt
# last_texts stores the texts at the previous second
last_texts = ""

# Set a variable timer for after() function
timer = None
# cnt to count the times the text does not change
cnt = 0

# variable to update the text brightness in hex representation, set to FG_COLOR_RESET by default
color_update = FG_COLOR_RESET


def save_texts():
    '''Save texts function for the button'''
    # Make the countdown stop
    window.after_cancel(timer)
    # print("Time stops")
    # Get the current texts
    texts = texting_textbox.get("1.0", tk.END)

    # Ask user to save as a new txt file, and store the path to file_path
    file_path = asksaveasfilename(title="Save a new txt file",
                                  initialfile='Untitled.txt',
                                  defaultextension=".txt",
                                  filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    # Write the current texts into the saved file.
    try:
        with open(file_path, mode="w") as file:
            file.write(texts)
    # The FileNotFoundError exception to prevent user didn't save a file, resulting in no value stored in file_path
    except FileNotFoundError:
        pass

    # Make the countdown re-run and set the color to the default value
    global cnt, color_update
    cnt = 0
    color_update = FG_COLOR_RESET
    window.after(1000, check_for_changes())


def text_fade_out(color_hex:str):
    '''To make the text fade out second by second, and return a faded-out color hex code'''
    global color_update
    # For every second the texts remain the same
    if cnt > 0:
        # The format of color_hex is: #rrggbb in hex representation respectively
        # Extract the r, g, b values and covert them into decimal representations
        r = int(color_hex[1:3], base=16)
        g = int(color_hex[3:5], base=16)
        b = int(color_hex[5:], base=16)
        # Change the r, g, b values
        r += 50
        g += 50
        b += 50
        # Combine r, g, b values into a variable color_update, which is a string datatype of hex color code
        color_update = f"#{str(hex(r))[2:]}{str(hex(g))[2:]}{str(hex(b))[2:]}"
    return color_update


def check_for_changes():
    '''Check whether the texts in the textbox currently are same as the ones of previous second.'''
    global last_texts, cnt, color_update, timer
    # Get the current texts in the textbox
    current_texts = texting_textbox.get("1.0", tk.END)
    # print(cnt)
    # print(f"Current text: {current_texts}.")

    # The condition that the current texts are not the same,
    # make the count-down re-run, text color back to the default value and store the new texts
    if current_texts != last_texts:
        # print("Text content has changed.")
        cnt = 0
        texting_textbox.config(foreground=FG_COLOR_RESET)
        color_update = FG_COLOR_RESET
        last_texts = current_texts

    # The condition that the current texts remain the same,
    else:
        # print("No changes detected.")
        # Detects whether there is no text inside the Text widget, no text means only "\n" inside the widget
        # if there are any texts inside, time counts down, and fade out the text color second by second
        if current_texts != "\n":
            texting_textbox.config(foreground=text_fade_out(color_update))
            cnt += 1
        # Detect the countdown reach the limit second, re-run the countdown, clear the text widget, and set the color to default
        if cnt > COUNT_DOWN_SEC:
            cnt = 0
            texting_textbox.delete("0.0", tk.END)
            color_update = FG_COLOR_RESET
    # print(color_update, "\n")

    # Count down every second
    timer = window.after(1000, check_for_changes)


# Initialize the UI
window = tk.Tk()
window.title('Disappearing Text Writing')  # Add window title
window.minsize(width=1000, height=600)  # Scale the window
window.geometry('+200+100')  # Let the window pop up at a certain position on the screen

intro_label = tk.Label(text=f"Full of your imaginary to write down anything without any pause.\n"
                            f"Or all the typed texts will be eliminated in {COUNT_DOWN_SEC} seconds!\n"
                            f"Moreover, Saving the texts at any time is allowed.",
                       font=("New Times Roman", 30, "bold"))
intro_label.grid(column=0, row=0, padx=20, pady=10)
texting_textbox = tk.Text(background="white", foreground=FG_COLOR_RESET, width=80, height=16, font=("Ariel", 20), wrap="word")
texting_textbox.grid(column=0, row=1, padx=20, pady=10)

save_button = tk.Button(text="Save texts", width=12, height=2, foreground="red", font=("Ariel", 16, "bold"), command=save_texts)
save_button.grid(column=0, row=2, padx=20)

# Start the checking function to check whether the texting stops over a period of time.
check_for_changes()

window.mainloop()


