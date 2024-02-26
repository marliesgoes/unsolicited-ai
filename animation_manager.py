from PIL import Image, ImageTk
import tkinter as tk
import glob

class AnimationManager:
    def __init__(self, persona):
        self.root = tk.Tk()
        self.root.title("Character Animation")
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        self.frames_talking = [Image.open(image) for image in sorted(glob.glob(f'images/{persona}/speaking*.png'))]
        self.frames_idle = [Image.open(image) for image in sorted(glob.glob(f'images/{persona}/idle*.png'))]
        self.current_frame_index = 0
        self.frames = self.frames_idle  # Start with idle frames
        self.speaking = False  # Track speaking state

    def set_speaking(self, speaking):
        """Method to switch animation state; safe to call from any thread."""
        self.speaking = speaking
        self.frames = self.frames_talking if speaking else self.frames_idle
        self.current_frame_index = 0  # Reset frame index on state change

    def update_animation(self):
        """Schedule the next frame update in the main thread."""
        frame = self.frames[self.current_frame_index]
        tk_img = ImageTk.PhotoImage(image=frame)
        self.canvas.create_image(400, 300, image=tk_img)
        self.canvas.image = tk_img  # Keep reference
        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
        self.root.after(50, self.update_animation)

    def run(self):
        self.update_animation()  # Start the animation
        self.root.mainloop()
