import cv2
import easyocr
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

root = Tk()
root.title('License Plate Reader')
root.minsize(height=600, width=1200)
root['bg'] = 'dark cyan'

def browse():
    file = filedialog.askopenfilename(initialdir='/', filetypes=(('image', '*.jpg;*.png'), ('All', '*.*')))
    image = cv2.imread(file)
    image = cv2.resize(image, (600, 400))
    plate_text, plate_image, character_images = extract_text(image)
    show_result(plate_text, image, plate_image, character_images)

def extract_text(image):
    reader = easyocr.Reader(['ar'])
    results = reader.readtext(image)
    plate_text = ""
    plate_image = image.copy()
    character_images = []
    for result in results:
        text = result[1]
        box = result[0]
        x, y, w, h = box[0][0], box[0][1], box[2][0] - box[0][0], box[2][1] - box[0][1]
        if len(text) >= 6:  # Adjust this condition based on license plate length
            plate_text += text + " "
            cv2.rectangle(plate_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            character_image = image[y:y+h, x:x+w]
            character_images.append(character_image)
    return plate_text.strip(), plate_image, character_images

def show_result(text, original_image, plate_image, character_images):
    original_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    original_img = Image.fromarray(original_img)
    original_img = original_img.resize((400, 400), Image.ANTIALIAS)
    original_img = ImageTk.PhotoImage(original_img)
    original_panel = Label(root, image=original_img)
    original_panel.image = original_img
    original_panel.place(x=50, y=50)

    plate_img = cv2.cvtColor(plate_image, cv2.COLOR_BGR2RGB)
    plate_img = Image.fromarray(plate_img)
    plate_img = plate_img.resize((400, 400), Image.ANTIALIAS)
    plate_img = ImageTk.PhotoImage(plate_img)
    plate_panel = Label(root, image=plate_img)
    plate_panel.image = plate_img
    plate_panel.place(x=500, y=50)

    result_label = Label(root, text="License Plate: " + text, font=('Times_New_Roman', 20), anchor='e')
    result_label.place(x=900, y=250)  # Adjust x-coordinate to align the text

    char_width = 100  # Adjust the width of the character images
    char_x = 950  # Updated x-coordinate for placing character images
    char_y = 50   # Updated y-coordinate for placing character images

    for char_img in character_images:
        char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2RGB)
        char_img = Image.fromarray(char_img)
        char_img = char_img.resize((char_width, 50), Image.ANTIALIAS)  # Adjust the dimensions here
        char_img = ImageTk.PhotoImage(char_img)
        char_label = Label(root, image=char_img)
        char_label.image = char_img
        char_label.place(x=char_x, y=char_y)
        char_y += 60
browse_button = Button(root, text='Browse', font=('Times_New_Roman', 30), command=browse)
browse_button.place(x=400, y=450)

root.mainloop()
