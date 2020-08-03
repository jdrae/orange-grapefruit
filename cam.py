import tkinter
from tkinter import filedialog 
import cv2
import PIL.Image, PIL.ImageTk
import time
import os

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.model_name = "please select model"
        
        # model select
        self.m_label = tkinter.Label(window, 
                                    text="model", width = 50)
        self.m_label.pack(anchor=tkinter.CENTER, expand = False)
        self.m_path = tkinter.Label(window, text=self.model_name)
        self.m_path.pack(anchor=tkinter.CENTER, expand = True)
        self.btn_select = tkinter.Button(window,text="select", width = 50, command = self.get_file)
        self.btn_select.pack(anchor=tkinter.CENTER, expand = True)

        # widht and height
        self.vid = MyVideoCapture(video_source)
        self.canvas = tkinter.Canvas(window, 
                                    width = self.vid.width,
                                    height = self.vid.height)
        self.canvas.pack()

        #snapshot btn
        self.btn_snapshot = tkinter.Button(window, 
                                        text="snapshot", width = 50, command = self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand = True)

        # video frame setting
        self.delay = 15
        self.update()

        self.window.mainloop()
    
    def update(self):
        ret, frame = self.vid.get_frame()

        if ret : 
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image = self.photo, anchor = tkinter.NW)
        
        self.window.after(self.delay, self.update)

    def snapshot(self):
        ret, frame = self.vid.get_frame()
        if ret:
            if not os.path.exists("photo\\"):
                os.makedirs("photo\\")
            cv2.imwrite("photo\\frame-"+time.strftime("%Y%m%d-%H%M%S")+".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def get_file(self):
        self.model_name = filedialog.askopenfilename(initialdir = "/", 
                                                title = "Select a File", 
                                                filetypes = (("Model files", 
                                                                "*.h5"),
                                                                ("all files",
                                                                "*.*")))
        self.m_path.configure(text= self.model_name)

class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)

        if not self.vid.isOpened():
            raise ValueError("Unable to open video", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret: #return boolean success flag
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)



App(tkinter.Tk(), "Zucchini")