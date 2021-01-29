import tkinter as tk
import pygame
from tkinter import messagebox

STOPPED = "stopped"
PAUSED = "paused"
RUNNING = "running"

my_font = ("Consolas", 14)

WAIT = 1000 # wait time in ms

class PostureApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# self.grid_columnconfigure(0, weight=1)

		self.init_mixer()
		

		self.clock = None
		self.e_time = None
		self.btn_start = None

		self.time = 0
		self.draw_window()

		self.mode = STOPPED

	def init_mixer(self):
		pygame.mixer.init()
		pygame.mixer.music.load("c.mp3")


	def draw_window(self):
		self.clock = tk.Label(self, text="0:00", font=my_font)
		self.e_min = tk.Entry(self, font=my_font)
		self.e_sec = tk.Entry(self, font=my_font)
		self.btn_start = tk.Button(self, text="Start", font=my_font, command=self.start_clicked)

		self.clock.grid(row=0, column=0)
		self.e_min.grid(row=1, column=0)
		self.e_sec.grid(row=2, column=0)
		self.btn_start.grid(row=3, column=0)
		


	def start_clicked(self):
		if self.is_time_valid():
			self.time = self.get_time_entered_as_seconds()
			self.mode = RUNNING
			self.loop(self.time)
			



	def is_time_valid(self):
		raw_m = self.e_min.get() or 0
		raw_s = self.e_sec.get() or 0
		try:
			int(raw_m)
			int(raw_s)
		except ValueError:
			messagebox.showerror("Error", "Invalid time format")
			return False
		if int(raw_m) >= 0 and int(raw_s) >= 0:
			return True
		else:
			messagebox.showerror("Error", "Invalid time format")
			return False


	def get_time_entered(self):
		"""
		Assumes validation of entries has already been done
		"""
		return (int(self.e_min.get() or 0), int(self.e_sec.get() or 0))


	def get_time_entered_as_seconds(self):
		time_tup = self.get_time_entered()
		return time_tup[0] * 60 + time_tup[1]


	def loop(self, s):
		minutes, seconds = divmod(s, 60)
		if s != 0:
			if self.mode == RUNNING:
				self._redraw_clock_label(minutes, seconds)
			elif self.mode == STOPPED:
				return
			self.after(WAIT, self.loop, s - 1)
		else:
			self.play_sound()
			self.start_clicked()

	def _redraw_clock_label(self, m, s):
		new_time = "{}:{:02}".format(m, s)
		self.clock.config(text=new_time)

	def play_sound(self):
		pygame.mixer.music.play()



def main():
	pa = PostureApp()
	pa.mainloop()

if __name__ == "__main__":
	main()