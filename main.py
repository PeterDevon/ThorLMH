import customtkinter as ctk
import easygui
from ollama import chat
from generate.speech import speech
from generate.text import text
from vision.vision import capture_image, choose_image

attached_image = None

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
window = ctk.CTk()
window.title("ThorLMH Multimodal")
window.geometry("350x200")

def handle_image_attachment(output_box):
    global attached_image
    choice = easygui.buttonbox("How do you want to attach the image?", choices=["Webcam", "File"])
    if choice == "Webcam":
        attached_image = capture_image()
    elif choice == "File":
        attached_image = choose_image()

    if attached_image:
        output_box.configure(state="normal")
        output_box.insert("end", f"Image attached: {attached_image}\n")
        output_box.configure(state="disabled")

def send_message_to_ollama(user_input, output_box):
    global attached_image
    if attached_image:
        messages = [{'role': 'user', 'content': f'Keep your answers short. {user_input}', 'images': [attached_image]}]
    else:
        messages = [{'role': 'user', 'content': user_input}]

    stream = chat(model="gemma3:4b", messages=messages, stream=True)
    full_response = ""
    for chunk in stream:
        token = chunk['message']['content']
        output_box.insert("end", token)
        output_box.update_idletasks()
        full_response += token

    output_box.insert("end", "\n")
    output_box.configure(state="disabled")
    attached_image = None

def start_speech(output_box):
    speech.listen_once_and_return(output_box, attached_image)

def stt():
    speech_window = ctk.CTkToplevel(window)
    speech_window.title("Speak to the LLM")
    speech_window.geometry("400x350")

    label = ctk.CTkLabel(speech_window, text="Speech Input (non-editable)")
    label.pack(pady=10)

    output_box = ctk.CTkTextbox(speech_window, width=300, height=150)
    output_box.pack(pady=10)
    output_box.insert("end", "Waiting for speech input...\n")
    output_box.configure(state="disabled")

    ask_button = ctk.CTkButton(speech_window, text="Ask Thor", command=lambda: start_speech(output_box))
    ask_button.pack(pady=5)

    attach_button = ctk.CTkButton(speech_window, text="Attach Image", command=lambda: handle_image_attachment(output_box))
    attach_button.pack(pady=5)

def clo():
    text_window = ctk.CTkToplevel(window)
    text_window.title("Text the LLM")
    text_window.geometry("400x400")

    label = ctk.CTkLabel(text_window, text="Enter your message:")
    label.pack(pady=10)

    input_box = ctk.CTkEntry(text_window, width=300)
    input_box.pack(pady=10)

    output_box = ctk.CTkTextbox(text_window, width=300, height=150)
    output_box.pack(pady=10)
    output_box.insert("end", "Thor's replies will appear here...\n")
    output_box.configure(state="disabled")

    def handle_ask():
        global attached_image
        user_input = input_box.get()
        if not user_input.strip() and attached_image:
            user_input = "What is in this image?"

        if user_input.strip():
            output_box.configure(state="normal")
            output_box.insert("end", f"You: {user_input}\nThor: ")
            output_box.update_idletasks()

            # 🔥 Using your generate.text module now!
            stream = text.handle_text_input(user_input, attached_image)
            full_response = ""
            for chunk in stream:
                token = chunk['message']['content']
                output_box.insert("end", token)
                output_box.update_idletasks()
                full_response += token

            output_box.insert("end", "\n")
            output_box.configure(state="disabled")
            attached_image = None


    ask_button = ctk.CTkButton(text_window, text="Ask Thor", command=handle_ask)
    ask_button.pack(pady=5)

    attach_button = ctk.CTkButton(text_window, text="Attach Image", command=lambda: handle_image_attachment(output_box))
    attach_button.pack(pady=5)

def cwt():
    option_label = ctk.CTkLabel(window, text="Choose an option")
    option_label.place(x=120, y=80)

    speak_button = ctk.CTkButton(window, text="Speak to the LLM", command=stt)
    speak_button.place(x=100, y=110)

    text_button = ctk.CTkButton(window, text="Text the LLM", command=clo)
    text_button.place(x=100, y=150)

def main():
    label = ctk.CTkLabel(window, text="ThorLMH: Ask anything!")
    label.place(x=100, y=10)

    chat_with_thor = ctk.CTkButton(window, text="Chat with Thor", command=cwt)
    chat_with_thor.place(x=100, y=40)

    window.mainloop()

if __name__ == "__main__":
    main()
