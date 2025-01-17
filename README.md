 **Overview**
This is a **Language Translation Tool** built using Python and CustomTkinter. It supports both **auto-translate** and **manual translate** modes, allowing users to translate text between multiple languages. The app also includes a **voice input feature** for hands-free translation.

---

#### **Features**
1. **Auto-Translate Mode**:
   - Automatically translates text as the user speaks or writes.
2. **Manual Translate Mode**:
   - Allows users to write text and click a "Translate" button to translate it.
3. **Voice Input**:
   - Users can speak into their microphone, and the app will recognize and translate the text.
4. **Multiple Languages**:
   - Supports translation between **English, Hindi, French, Japanese, German, Spanish, Chinese, Russian, Arabic, and Portuguese**.
5. **Swap Languages**:
   - Users can swap the source and target languages with a single click.
6. **Save Translation History**:
   - Translations can be saved to a file for future reference.

---

#### **Requirements**
- Python 3.x
- Libraries:
  - `customtkinter`
  - `googletrans==4.0.0-rc1`
  - `speechrecognition`
  - `datetime`
  - `threading`

Install the required libraries using:
```bash
pip install customtkinter googletrans==4.0.0-rc1 speechrecognition
```

---

#### **How to Use**
1. **Auto-Translate Mode**:
   - Toggle the "Auto-Translate" switch to enable auto-translate.
   - Speak into your microphone, and the recognized text will appear in the input box.
   - The text will be automatically translated and displayed in the output box.
2. **Manual Translate Mode**:
   - Toggle the "Auto-Translate" switch to disable auto-translate.
   - Write text in the input box and click the "Translate" button to translate it.
3. **Swap Languages**:
   - Use the "⇄" button to swap the source and target languages.
4. **Save History**:
   - Click "Save Translation History" to save the current translation to a file.

---

#### **License**
This project is open-source and available under the MIT License.

---
