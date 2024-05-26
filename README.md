
# Nervousness Classification

This project uses Flask, OpenCV, MediaPipe, and DeepFace to classify and analyze nervousness levels in real-time based on facial emotions. The application captures video from a webcam, detects faces, and analyzes emotions to categorize nervousness into weak, strong, and neutral levels.

## Features

- Real-time video capture and processing
- Face detection using MediaPipe
- Facial emotion analysis using DeepFace
- Nervousness classification based on detected emotions
- Probability table display for emotion analysis
- Database integration to store nervousness data

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/repository-name.git
   cd repository-name
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```sh
   python createdatabase.py
   ```

## Usage

1. **Run the Flask application:**
   ```sh
   python main.py
   ```

2. **Open your web browser and go to:**
   ```
   http://127.0.0.1:5000
   ```

3. **Enter your name and start the video feed:**
   - Enter your name in the input field and click the "Start" button.
   - The real-time video feed will start, showing emotion probabilities and nervousness classification.

4. **Terminate the video feed and store data:**
   - Click the "Terminate" button to stop the video feed and store the nervousness data into the database.

## Functionality

### Real-time Video Capture and Processing

The application captures video from your webcam and processes each frame to detect faces using MediaPipe. It then analyzes facial emotions using DeepFace to determine the dominant emotions.

### Emotion Analysis and Nervousness Classification

The detected emotions are categorized into nervousness levels:
- **Weak**: Disgusted, Sad, Surprised
- **Strong**: Angry, Fearful
- **Neutral**: Happy, Neutral

A probability table is displayed on the video feed showing the probability of each detected emotion.

### Database Integration
The application uses SQLite to store nervousness data. Each record includes the name of the user and counts of weak, strong, and neutral nervousness levels.

## Requirements
- Flask
- OpenCV
- MediaPipe
- DeepFace
- SQLite
