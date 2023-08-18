import os
from tkinter import filedialog, Button, Label, Listbox, Scrollbar, Scale, Tk, Frame, PhotoImage, BOTH, LEFT, RIGHT, END, X, Y
from tkinter.ttk import Progressbar, Style
import pygame, random
from mutagen.mp3 import MP3


class BobAmp:
    def __init__(self, root):
        self.root = root
        self.root.title('BobAmp v1.0')
        self.root.geometry('350x400')
        pygame.mixer.init()
        self.playlist=[]
        self.current_index=0
        self.is_paused=False
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.superior = Frame(self.root, background='#232632')
        self.superior.pack(side='top', fill=BOTH, expand=True)
        
        self.inferior = Frame(self.root, background='#232632')
        self.inferior.pack(side='top')

        self.volumen = Frame(self.root, background='#232632', bd=0)
        self.volumen.pack(side='top', expand=True, fill=X)

        self.progreso = Frame(self.root, background='#232632')
        self.progreso.pack(side='bottom', fill=X, expand=True)

        image_path3 = os.path.join(script_dir, 'icons/bobamp.png')
        self.favicon = PhotoImage(file=image_path3)
        self.root.iconphoto(True, self.favicon)
        self.root.call('wm', 'iconphoto', self.root._w, self.favicon)

        image_path = os.path.join(script_dir, 'icons/open.png')
        self.button_open = PhotoImage(file=image_path)

        image_path2 = os.path.join(script_dir, 'icons/forward.png')
        self.button_forward = PhotoImage(file=image_path2)

        image_path3 = os.path.join(script_dir, 'icons/pause.png')
        self.button_pause = PhotoImage(file=image_path3)

        image_path4 = os.path.join(script_dir, 'icons/play.png')
        self.button_play = PhotoImage(file=image_path4)

        image_path5 = os.path.join(script_dir, 'icons/stop.png')
        self.button_stop = PhotoImage(file=image_path5)

        image_path6 = os.path.join(script_dir, 'icons/rewind.png')
        self.button_rewind = PhotoImage(file=image_path6)

        style = Style()
        style.configure('Custome.Horizontal.TProgressbar', troughcolor='green', background='purple')

        self.create_ui()


    def create_ui(self):

        self.root.configure(bg="#232632")

        self.listbox = Listbox(self.superior, bg='#222222', fg='#5ddc06', selectforeground='white')
        self.listbox.pack(fill=BOTH, expand=True, side=LEFT)
        self.listbox.bind("<Double-1>", self.play_selected_track)

        self.scrollbar=Scrollbar(self.superior, command=self.listbox.yview, bg='#232632')
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.boton_abrir = Button(self.inferior, image=self.button_open, relief='flat', bg='#232632', activebackground='#232632', bd=0, command=self.open_directory)
        self.boton_abrir.pack(side=LEFT, pady=25, padx=3)
        self.boton_abrir.config(cursor='hand2')

        self.boton_reproducir = Button(self.inferior, image=self.button_play, relief='flat', bg='#232632', activebackground='#232632', bd=0, command=self.play_pause)
        self.boton_reproducir.pack(side=LEFT, pady=25, padx=3)
        self.boton_reproducir.config(cursor='hand2')

        self.boton_atrasar = Button(self.inferior, image=self.button_rewind, relief='flat', bg='#232632', activebackground='#232632', bd=0, command=self.prev_track)
        self.boton_atrasar.pack(side=LEFT, pady=25, padx=3)
        self.boton_atrasar.config(cursor='hand2')

        self.boton_adelantar = Button(self.inferior, image=self.button_forward, relief='flat', bg='#232632', activebackground='#232632', bd=0, command=self.next_track)
        self.boton_adelantar.pack(side=LEFT, pady=25, padx=3)
        self.boton_adelantar.config(cursor='hand2')

        self.boton_detener = Button(self.inferior, image=self.button_stop, relief='flat', bg='#232632', activebackground='#232632', bd=0, command=self.stop)
        self.boton_detener.pack(side=LEFT, pady=25, padx=3)
        self.boton_detener.config(cursor='hand2')

        self.volumen_slider = Scale(self.volumen, troughcolor='#581845', activebackground='#232632', from_=0, to=100, orient='horizontal', label='Volumen', bg='#232632', fg="#fff", bd=0, highlightbackground='#232632', font=('Verdana', 11), command=self.set_volume)
        self.volumen_slider.set(50)
        self.volumen_slider.pack(expand=True, fill=X, padx=6)
        self.volumen_slider.config(cursor='hand2')

        self.time_label=Label(self.progreso, text='00:00 / 00:00', fg='white', bg="#232632")
        self.time_label.pack(side=LEFT)

        self.barra_progreso = Progressbar(self.progreso, mode='determinate', maximum=100, length=300, style='Custom.Horizontal.TProgressbar')
        self.barra_progreso.pack(fill=X, expand=True, side=RIGHT, padx=6)
        
        self.update_progress_bar()

    def open_directory(self):
        directory=filedialog.askdirectory()
        if directory:
            self.playlist=sorted([os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(('.mp3', '.wma', '.ogg', '.flac'))])  
            self.listbox.delete(0, END)      
        
            for song in self.playlist:
                self.listbox.insert(END, os.path.basename(song))
            self.current_index = 0
            self.play_current_track()

    def play_current_track(self):
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.is_paused=False

    def play_pause(self):
        if self.is_paused:
            self.boton_reproducir.configure(image=self.button_pause)
            self.boton_reproducir.img = self.button_pause
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            self.boton_reproducir.configure(image=self.button_play)
            self.boton_reproducir.img = self.button_play
            pygame.mixer.music.pause()
            self.is_paused = True

    def update_progress_bar(self):
        if pygame.mixer.music.get_busy() and not self.is_paused:
            current_time = pygame.mixer.music.get_pos() / 1000  # In seconds
            song_length = self.get_song_length()
            progress_percent = (current_time / song_length) * 100
            self.barra_progreso["value"] = progress_percent
            self.update_time_labels(current_time, song_length)
        # elif not pygame.mixer.music.get_busy() and self.playlist:
        #    self.next_track()
        self.root.after(1000, self.update_progress_bar)
    
    def stop(self):
        pygame.mixer.music.stop()
    #    self.barra_progreso["value"] = 0
    #    self.update_time_labels(0, 0)

    def get_song_length(self):
        audio = MP3(self.playlist[self.current_index])
        return audio.info.length

    def update_time_labels(self, current_time, song_length):
        current_time_str = self.format_time(current_time)
        song_length_str = self.format_time(song_length)
        self.time_label.config(text=f"{current_time_str} / {song_length_str}")

    def format_time(self, time_in_seconds):
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_current_track()
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(self.current_index)
        self.listbox.activate(self.current_index)

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_current_track()
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(self.current_index)
        self.listbox.activate(self.current_index)

    def play_selected_track(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.current_index = selected_index[0]
            self.play_current_track()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(int(volume) / 100)
        self.volumen_slider.config(label=f"Volumen: {int(volume)}")


root = Tk()
app=BobAmp(root)
root.mainloop()
