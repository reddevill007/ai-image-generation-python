import tkinter as tk
import customtkinter
import replicate
from PIL import ImageTk
from urllib.request import urlopen

class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Image Generator App")
        
        # Ui elements
        self.heading = customtkinter.CTkLabel(root, text="Write Your prompt here")
        self.heading.pack(padx=10, pady=10)

        # prompt input
        self.promptVariable = tk.StringVar()
        self.prompt = customtkinter.CTkEntry(root, width=400, height=50, textvariable=self.promptVariable)
        self.prompt.pack(padx=10, pady=10)

        # Run Btn
        self.run = customtkinter.CTkButton(root, text="Run", command=self.generate_image)
        self.run.pack(padx=10, pady=10)

        # Image
        self.image_label = customtkinter.CTkLabel(root, text="")
        self.image_label.pack()

    def generate_image(self):
        # Disable the entry and button during processing
        self.prompt.configure(state='disabled')
        self.run.configure(state='disabled')

        # Show loading label
        self.run.configure(text="Running...")

        # Get the prompt from the entry
        prompt = self.promptVariable.get()

        # Call your image generation function
        image_url = self.generate_image_from_prompt(prompt)

        # Display the generated image
        self.display_image(image_url)

        # Enable the entry and button after processing
        self.prompt.configure(state='normal')
        self.run.configure(state='normal')

    def generate_image_from_prompt(self, prompt):
        output = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={
                "width": 768,
                "height": 768,
                "prompt": prompt,
                "scheduler": "DPMSolverMultistep",
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "num_inference_steps": 50
            }
        )

        return output[0]

    def display_image(self, image_url):
        # Fetch the image
        u = urlopen(image_url)
        raw_data = u.read()
        u.close()

        # Display the image
        photo = ImageTk.PhotoImage(data=raw_data)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

        # Hide loading label
        self.run.configure(text="Run")



if __name__ == "__main__":
    # System Setting
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    #Our app frame
    root = customtkinter.CTk()
    root.geometry('1400x800')
    app = ImageGeneratorApp(root)
    root.mainloop()