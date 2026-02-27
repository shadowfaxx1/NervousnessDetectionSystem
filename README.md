# Nervousness Classifier

Real-time nervousness detection using your webcam. Detects facial emotions and classifies them into nervousness levels, storing results in a database.

---

## Quick Start

```sh
git clone https://github.com/your-username/repository-name.git
cd repository-name
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python createdatabase.py
python main.py
```

Then open **http://127.0.0.1:5000**, enter your name, and hit **Start**.

---

## How It Works

Each webcam frame is scanned for faces (MediaPipe), emotions are analysed (DeepFace), and mapped to a nervousness level:

| Level | Emotions |
|-------|----------|
| Weak | Disgusted, Sad, Surprised |
| Strong | Angry, Fearful |
| Neutral | Happy, Neutral |

Live emotion probabilities are overlaid on the video feed. Hit **Terminate** to stop and save your session to the SQLite database.

---

## Stack
Flask · OpenCV · MediaPipe · DeepFace · SQLite
