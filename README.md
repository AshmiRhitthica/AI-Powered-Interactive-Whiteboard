# 🎓 AI-Powered Interactive Whiteboard

An AI-powered interactive whiteboard prototype designed to support visual learning and student engagement. The application allows users to enter a topic through handwriting, image upload, or keyboard input, then provides an explanation, text-to-speech audio, and an educational video.

## ✨ Features

✏️ Interactive Whiteboard — Draw or write topics using a digital canvas.

🖼️ Handwriting Upload — Upload a handwritten JPG/PNG image.

⌨️ Text Input — Type a topic directly using the keyboard.

🔍 OCR Recognition — Extract handwritten text using Tesseract OCR.

📖 Topic Explanation — Retrieve topic information using the Wikipedia API.

🔊 Text-to-Speech — Convert explanations into spoken audio.

🎥 Educational Video Search — Find relevant educational videos from YouTube.

💬 Doubt Clearing — Ask questions and receive explanations.

👀 Student Attentiveness Monitoring — Use webcam-based face/eye tracking to provide an attentiveness status.

🖥️ Streamlit Interface — Simple interactive web interface for the complete learning workflow.

## 🧠 How It Works

                 ┌──────────────────────┐
                 │      User Input      │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
        ✏️ Canvas      🖼️ Upload       ⌨️ Type
             │              │              │
             └──────────────┼──────────────┘
                            ↓
                     🔍 OCR Processing
                            │
                            ↓
                    ✅ Confirm Topic
                            │
                            ↓
                 ┌──────────┴──────────┐
                 ↓          ↓          ↓
             📖 Explain    🔊 Audio   🎥 Video
                 │
                 ↓
             💬 Ask Questions
                 
                 + 
                 
             👀 Attentiveness
                Monitoring

## 🛠️ Technologies Used

### Frontend / Application

- Python
- Streamlit
- Streamlit Drawable Canvas
  
### OCR & Image Processing

- Tesseract OCR
- Pytesseract 
- Pillow
- OpenCV
  
### AI / Educational Features

- Wikipedia API
- Google Text-to-Speech (gTTS)
- YouTube Search
- MediaPipe
  
### Other

- NumPy
- Requests

## 🔄 Application Workflow

### 1. Enter a Topic

The user can provide a topic using:

- ⌨️ Keyboard
- 🖼️ Handwritten image
- ✏️ Interactive canvas

### 2. OCR Processing

For handwritten input, **Tesseract OCR** extracts the text from the image.

### 3. Topic Confirmation

The detected topic can be corrected before generating learning content.

### 4. Explanation

The application retrieves an introductory explanation for the selected topic using the **Wikipedia API**.

### 5. Audio

The explanation is converted into speech using **gTTS (Google Text-to-Speech)**.

### 6. Educational Video

The application searches **YouTube** for an educational video related to the topic.

### 7. Doubt Clearing

Users can enter additional questions and retrieve relevant explanations.

### 8. Attentiveness Monitoring

The application uses the webcam and **MediaPipe face landmarks** to monitor basic visual attentiveness indicators such as face presence and eye closure.

> **Note:** The attentiveness feature is a prototype indicator and should not be interpreted as a definitive measurement of a student's actual attention.

---

## 🎯 Project Objective

The objective of this project is to combine **AI, OCR, computer vision, natural language processing, and multimedia learning** into a single interactive platform that can make digital learning more engaging and accessible.

---

## 👩‍💻 Author

**Ashmi L. Rhitthica**

B.E. Computer Science and Engineering

---

### ⭐ If you find this project interesting

Feel free to explore the repository, experiment with the application, and suggest improvements.
