from pytube import YouTube
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
from tkinter import font as tkFont
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi


FOLDER_PATH = "C:/Users/manda/portfolio/YoutubeDownload/downloaded"
TXT_PATH = "C:/Users/manda/portfolio/YoutubeDownload/TXT_FILES"


class YoutubeDownload(Tk):
    def __init__(self):
        super().__init__()
        self.title("Youtube Download")
        self.geometry("410x400")  # Define the geometry of the window
        self.configure(bg='pink')
        self.widget()

    def widget(self):
        helv26 = tkFont.Font(family='Helvetica', size=26, weight=tkFont.BOLD)
        title = Label(width=25, text="Youtube Download App", font=helv26, anchor=CENTER, background='black', foreground='pink',)
        title.pack(side=TOP, pady=50)
        link_label = Label(text="URL Link:", font=tkFont.Font(family='Helvetica', size=11, weight=tkFont.BOLD), background='pink', foreground='black',)
        link_label.pack(side=TOP)
        input_text = StringVar()
        self.link = Entry(width=50, font=tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD), textvariable=input_text, justify=CENTER)
        self.link.pack(pady=5)
        choices = ['Low Resolution', 'High Resolution']
        variable = StringVar(self)
        variable.set('Low Resolution')
        self.w = Combobox(self, values=choices, font=tkFont.Font(family='Helvetica', size=8, weight=tkFont.BOLD))
        self.w.pack()
        space_label = Label(text="", font=tkFont.Font(family='Helvetica', size=25, weight=tkFont.BOLD),
                           background='pink', foreground='black', )
        space_label.pack(side=BOTTOM)
        caption_button = Button(text="Download English Caption", width=25, command=self.download_caption)
        style = Style()
        style.configure('TButton', background='pink')
        style.configure('TButton', foreground="black")
        style.configure("TButton", font=('Helvetica', 10, "bold"))
        caption_button.pack(side=BOTTOM, pady=5)
        download_button = Button(text="Download Video", width=25, command=self.download)
        download_button.pack(side=BOTTOM)

    def download(self):
        link = self.link.get()

        if link == "":
            tkinter.messagebox.showerror("URL LINK", "You need to write the video URL, try again")
        else:
            yt = YouTube(link)
            if self.w.get() == "Low Resolution":
                lowest = yt.streams.get_lowest_resolution()
                lowest.download(FOLDER_PATH)
                tkinter.messagebox.showinfo("Success", f"Downloaded to: {FOLDER_PATH}")
            elif self.w.get() == "High Resolution":
                highest = yt.streams.get_highest_resolution()
                highest.download(FOLDER_PATH)
                tkinter.messagebox.showinfo("Success", f"Downloaded to: {FOLDER_PATH}")
            else:
                tkinter.messagebox.showinfo("Not Complete", "Choose resolution first!")


    def download_caption(self):
        youtube_link = self.link.get()
        link = youtube_link.split("v=")
        from_separated_list = link[1]
        today = datetime.now().date()
        try:
            srt = YouTubeTranscriptApi.get_transcript(from_separated_list)
            length = len(srt)
            with open(f"TXT_FILES/Output_{today}.txt", "w") as text_file:
                for i in range(0, length):
                    start = f"start : {srt[i]['start']}"
                    duration = f"duration : {srt[i]['duration']}"
                    text = srt[i]["text"]
                    text_file.writelines([start,"\n", duration, "\n", text, "\n"])
                tkinter.messagebox.showinfo("SUCCESS", f"txt file is saved in {TXT_PATH}")
        except:
            tkinter.messagebox.showerror("ERROR", "No subtitle available.")


App = YoutubeDownload()
App.mainloop()
