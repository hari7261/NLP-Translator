import customtkinter as ctk
from googletrans import Translator
import speech_recognition as sr
import datetime
import threading

translator = Translator()

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Japanese": "ja",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-cn",
    "Russian": "ru",
    "Arabic": "ar",
    "Portuguese": "pt"
}

recognizer = sr.Recognizer()

class TranslationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Language Translation Tool")
        self.geometry("700x550")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.source_lang = "en"
        self.target_lang = "hi"
        self.is_listening = False
        self.auto_translate_mode = True
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Language Translator", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)
        self.auto_translate_switch = ctk.CTkSwitch(self, text="Auto-Translate", command=self.toggle_auto_translate, font=("Arial", 14))
        self.auto_translate_switch.pack(pady=5)
        self.auto_translate_switch.select()
        self.input_text = ctk.CTkTextbox(self, width=600, height=100, font=("Arial", 14))
        self.input_text.pack(pady=10)
        self.voice_button = ctk.CTkButton(self, text="🎤 Start Listening", command=self.toggle_listening, font=("Arial", 14))
        self.voice_button.pack(pady=5)
        self.language_frame = ctk.CTkFrame(self)
        self.language_frame.pack(pady=10)
        self.source_lang_var = ctk.StringVar(value="English")
        self.source_lang_menu = ctk.CTkOptionMenu(self.language_frame, values=list(LANGUAGES.keys()), variable=self.source_lang_var, font=("Arial", 14))
        self.source_lang_menu.pack(side="left", padx=10)
        self.swap_button = ctk.CTkButton(self.language_frame, text="⇄", command=self.swap_languages, font=("Arial", 14), width=30)
        self.swap_button.pack(side="left", padx=10)
        self.target_lang_var = ctk.StringVar(value="Hindi")
        self.target_lang_menu = ctk.CTkOptionMenu(self.language_frame, values=list(LANGUAGES.keys()), variable=self.target_lang_var, font=("Arial", 14))
        self.target_lang_menu.pack(side="left", padx=10)
        self.translate_button = ctk.CTkButton(self, text="Translate", command=self.manual_translate, font=("Arial", 14))
        self.translate_button.pack(pady=10)
        self.translate_button.pack_forget()
        self.output_text = ctk.CTkTextbox(self, width=600, height=100, font=("Arial", 14))
        self.output_text.pack(pady=10)
        self.save_button = ctk.CTkButton(self, text="Save Translation History", command=self.save_history, font=("Arial", 14))
        self.save_button.pack(pady=10)

    def toggle_auto_translate(self):
        self.auto_translate_mode = self.auto_translate_switch.get()
        if self.auto_translate_mode:
            self.translate_button.pack_forget()
            self.input_text.configure(state="normal")
        else:
            self.translate_button.pack(pady=10)
            self.input_text.configure(state="normal")

    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.voice_button.configure(text="⏹️ Stop Listening")
            threading.Thread(target=self.speech_to_text, daemon=True).start()
        else:
            self.is_listening = False
            self.voice_button.configure(text="🎤 Start Listening")

    def speech_to_text(self):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            while self.is_listening:
                try:
                    audio = recognizer.listen(source, phrase_time_limit=3)
                    text = recognizer.recognize_google(audio)
                    self.input_text.configure(state="normal")
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("end", text + " ")
                    self.input_text.configure(state="disabled")
                    if self.auto_translate_mode:
                        self.auto_translate()
                except sr.WaitTimeoutError:
                    self.is_listening = False
                    self.voice_button.configure(text="🎤 Start Listening")
                    break
                except sr.UnknownValueError:
                    self.input_text.configure(state="normal")
                    self.input_text.insert("end", "(Could not understand audio) ")
                    self.input_text.configure(state="disabled")
                except sr.RequestError as e:
                    self.input_text.configure(state="normal")
                    self.input_text.insert("end", f"(Error: {e}) ")
                    self.input_text.configure(state="disabled")

    def auto_translate(self):
        self.input_text.configure(state="normal")
        text = self.input_text.get("1.0", "end-1c")
        self.input_text.configure(state="disabled")
        self.source_lang = LANGUAGES.get(self.source_lang_var.get())
        self.target_lang = LANGUAGES.get(self.target_lang_var.get())
        if not text:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", "No text to translate.")
            return
        try:
            translated = translator.translate(text, src=self.source_lang, dest=self.target_lang)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", translated.text)
        except Exception as e:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", f"Error: {e}")

    def manual_translate(self):
        self.auto_translate()

    def swap_languages(self):
        source_lang = self.source_lang_var.get()
        target_lang = self.target_lang_var.get()
        self.source_lang_var.set(target_lang)
        self.target_lang_var.set(source_lang)
        if self.auto_translate_mode:
            self.auto_translate()

    def save_history(self):
        self.input_text.configure(state="normal")
        input_text = self.input_text.get("1.0", "end-1c")
        self.input_text.configure(state="disabled")
        output_text = self.output_text.get("1.0", "end-1c")
        if not input_text or not output_text:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", "No translation to save.")
            return
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("translation_history.txt", "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}]\n")
            file.write(f"Source: {input_text}\n")
            file.write(f"Translated: {output_text}\n")
            file.write("-" * 50 + "\n")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", "Translation saved to history.")

if __name__ == "__main__":
    app = TranslationApp()
    app.mainloop()
