import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk   #pillow module is used for image processing
import boto3
import boto3.session

my_w = tk.Tk()
my_w.geometry("450x400")
my_w.title("AWS Textract")

def upload_file():
    aws_console = boto3.session.Session(profile_name='Mahima')  #write your aws IAM User name here
    client = aws_console.client(service_name='textract', region_name='us-east-1')

    global Img 
    f_types = [("Image Files", "*.jpg .*png"), ("PDF  File", ".pdf")]
    filename = askopenfilename(filetypes=f_types)
    if filename:
        Img = Image.open(filename)

        # Image Resizing
        img_resize = Img.resize((400, 200))
        Img = ImageTk.PhotoImage(img_resize)
        # Update the image displayed in the label
        img_label.configure(image=Img)
        img_label.image = Img

        imgbytes = get_image_byte(filename)  #converting Images to Bytes
        response = client.detect_document_text( Document={'Bytes': imgbytes})
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                print(item["Text"])

l1 = tk.Label(my_w, text="Extract your Text", width="30", font=('Helvetica', 20, 'bold'))
l1.pack(pady=6)

b1 = tk.Button(my_w, text="Upload Image", width=30, command=upload_file)
b1.pack()

# Create a label widget to display the image
img_label = tk.Label(my_w)
img_label.pack()


def get_image_byte(filename):
    with open(filename, 'rb') as Imgfile:
        return Imgfile.read()

my_w.mainloop()
