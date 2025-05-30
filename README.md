# 🎤 LyricBot: Your AI Songwriting Companion 🎶

Welcome to **LyricBot**, the AI-powered lyric generator that helps you turn emotions into music! Whether you’re writing a heartfelt ballad or a party anthem, our chatbot’s got your back—fine-tuned with Reinforcement Learning to *sing your feelings*.

---

## 🌟 Project Overview

This project is a **Streamlit-based lyric chatbot**, designed to generate song lyrics tailored to your selected:
- **Genre** (e.g., Pop, Hip-Hop)
- **Emotion** (28 finely tuned emotional tones 🎭)
- **Topic** (from heartbreak to street life)

Under the hood: a GPT-2 model fine-tuned via RL to enhance lyric structure, emotional depth, and stylistic accuracy.

---

This document outlines the project directory layout for the lyric chatbot system, highlighting the frontend, model assets, dependencies, and documentation. Although the generator model has been fine-tuned offline using reinforcement learning (RL), the RL training code is not included in this repository.

```
project/
│
├── models/
│   ├── generator_base/                          # GPT-2 model fine-tuned on lyrics (pre-RL baseline)
│   ├── reinforce_finetuned_generator_best/      # Best-performing RL-fine-tuned generator (with full reward set)
│   └── reinforce_finetuned_generator_best_no3/  # RL model variant (e.g., without 3rd reward or altered config)
│
├── src/
│   ├── slot_manager.py      # Validates and normalizes user inputs (genre, topic, emotion, length)
│   ├── lyric_generator.py   # Loads and runs the generator model based on input slots
│   └── __pycache__/         # Auto-generated Python cache files
│
├── app.py                   # Streamlit app: handles chatbot interface and real-time lyric generation
│
├── requirements.txt         # Python dependencies needed to run the app and models
├── README.md                # Project overview, setup instructions, and usage guide
└── Structure Description.txt# Directory and file purpose explanations (this file)
```
## DEMO Lyrics
<img width="800" alt="image" src="https://github.com/user-attachments/assets/c87b9c9c-95d3-4b53-94aa-377be702f4a1" />

## Lyrics Comparison
<img width="800" alt="image" src="https://github.com/user-attachments/assets/c30e053b-638f-4896-b95e-f8a316fea136" />

## DEMO Video

https://github.com/user-attachments/assets/e783ddcd-861a-4cc3-8792-750070d42a4f


## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd project
```

### 2. Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage Guide

Launch the chatbot locally:

```bash
cd "your/path/to/project"
streamlit run app.py
```

🎧 This opens a simple chat UI where you can interactively:
- Choose your **Genre**
- Set the **Emotion**
- Pick a **Topic**
- Define the **Length**

...and voilà! Your personalised lyrics await ✨

---

## 🧠 Model Details

- **Base model**: GPT-2
- **Enhancement**: Reinforcement Learning (RL) fine-tuning for more accurate topic, genre and emotions alignment, improved coherence and stylistic structure
- **Note**: RL training scripts are not included in this repo

## 🧠 How to Change the Model Path

The default model path is set in the code as follows:

```python
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(current_dir, "models", "reinforce_finetuned_generator_best_no3"))
```

✨ **Want to use a different model? It’s easy!**

Simply change `"reinforce_finetuned_generator_best_no3"` in `MODEL_PATH` to the name of your desired model folder:

```python
MODEL_PATH = os.path.abspath(os.path.join(current_dir, "models", "your_custom_model_name"))
```

📁 Make sure your new model is placed inside the `models/` directory and includes all necessary files like `config.json`, `pytorch_model.bin`, etc.
---

## 🎵 Options

**Genres Supported**:
- 🎹 Pop
- 🎤 Hip-Hop

**Emotions (GoEmotions, 28 classes)**:
> admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire, disappointment, disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness, optimism, pride, realization, relief, remorse, sadness, surprise, neutral

**Topics (10 lyrical themes)**:
> 💔 Heartbreak & Loss, ❤️ Love & Intimacy, 🎭 Persona & Performance, 🌈 Hope & Reflection, 🎉 Urban Party Life, 🔥 Street & Conflict, 🔄 Personal Change, 🎙 Voice & Identity, ⚰️ Life & Mortality, ✝️ Faith & Religion

---

## ⚠️ Limitations

- Generated lyrics might **lack rhyming consistency** or **deep narrative arcs**
- **Repetition** may still occur in some outputs
- **Real-time performance** varies (GPU recommended for smoothest results)
- Model quality depends on **training data diversity**

---

## 🛠 Troubleshooting

- **Missing model weights?** ➤ Ensure you’ve downloaded files to the `models/` subdirectory  
- **Streamlit errors?** ➤ Try upgrading:  
```bash
pip install --upgrade streamlit
```

---

## 📚 References

- [GPT-2 Paper (OpenAI)](https://openai.com/research/better-language-models)
- [GoEmotions Dataset](https://github.com/google-research/google-research/tree/master/goemotions)
- [Streamlit Documentation](https://docs.streamlit.io/)

---
## 👨‍💻 Author

Frank (MTech EBA, NUS 2025)

---



