


from flask import Flask, request, jsonify, render_template, Response
import cv2
from deepface import DeepFace
import mediapipe as mp
import sqlite3
import threading
from flask import g

nervousness_counts = {
    'weak': 0,
    'strong': 0,
    'neutral': 0
}
# Initialize Flask app
app = Flask(__name__)

# Initialize MediaPipe Face Detection and Face Mesh
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# Define emotion to nervousness mapping
emotion_mapping = {
    'angry': 'strong',
    'disgusted': 'weak',
    'fearful': 'strong',
    'happy': 'neutral',
    'sad': 'weak',
    'surprised': 'weak',
    'neutral': 'neutral'
}

def draw_probabilities_table(frame, probabilities):
    table_height = 250
    table_width = 180
    cell_height = int(table_height / len(probabilities))
    cell_width = int(table_width / 2)

    cv2.rectangle(frame, (10, 10), (10 + table_width, 10 + table_height), (255, 255, 255), -1)
    
    # Draw header
    cv2.putText(frame, 'Emotion', (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(frame, 'Probability', (15 + cell_width, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    for i, (emotion, probability) in enumerate(probabilities.items()):
        y = 50 + i * cell_height
        cv2.putText(frame, emotion, (15, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.putText(frame, f'{probability:.2f}', (15 + cell_width, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        
# Function to connect to the database
def connect_db():
    conn = sqlite3.connect('nervousness_data.db')
    return conn

# Function to store data in the database
def store_nervousness_data(name, weak, strong, neutral):
    conn = connect_db()
    c = conn.cursor()
    c.execute('''INSERT INTO Nervousness (name, weak, strong, neutral) 
                 VALUES (?, ?, ?, ?)''', (name, weak, strong, neutral))
    conn.commit()
    conn.close()

# Function to process each frame
def process_frame(frame, name):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            face_roi = frame[y:y+h, x:x+w]
            
            if face_roi.size == 0 or (face_mesh == None):
                text_size = cv2.getTextSize("NO FACE DETECTED", cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
                text_x = (frame.shape[1] - text_size[0]) // 2
                text_y = (frame.shape[0] + text_size[1]) // 2
                cv2.putText(frame, "NO FACE DETECTED", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                continue 
            
            rgb_face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
            results_mesh = face_mesh.process(rgb_face_roi)
            
            if results_mesh.multi_face_landmarks:
                for face_landmarks in results_mesh.multi_face_landmarks:
                    for landmark in face_landmarks.landmark:
                        x_m = int(landmark.x * w + x)
                        y_m = int(landmark.y * h + y)
                        cv2.circle(frame, (x_m, y_m), 1, (0, 255, 0), -1)

            result = DeepFace.analyze(rgb_face_roi, actions=['emotion'], enforce_detection=False)

            nervousness_categories = { 
                'weak': 0,
                'strong': 0,
                'neutral': 0
            }
            
            for face_result in result:
                emotion_probabilities = face_result['emotion']
                draw_probabilities_table(frame, emotion_probabilities)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, face_result['dominant_emotion'].capitalize(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                
            for face_result in result:
                emotion_probabilities = face_result['emotion']
                for emotion, probability in emotion_probabilities.items():
                    if emotion in emotion_mapping:
                        nervousness_category = emotion_mapping[emotion]
                        nervousness_categories[nervousness_category] += probability
                for category, count in nervousness_categories.items():
                    nervousness_counts[category] += count
                    
            dominant_nervousness_category = max(nervousness_categories, key=nervousness_categories.get)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, dominant_nervousness_category, (x + 120, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 0, 255), 2)
            
    return frame

# @app.before_request
# def before_request():
#     g.nervousness_counts = {
#         'weak': 0,
#         'strong': 0,
#         'neutral': 0
#     }

# @app.teardown_request
# def teardown_request(exception):
#     if exception is None:
#         store_nervousness_data(request.args.get('name', default='Anonymous'), g.nervousness_counts['weak'], 
#                                g.nervousness_counts['strong'], g.nervousness_counts['neutral'])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    name = request.args.get('name', default='Anonymous')
    return Response(generate_frames(name), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/terminate', methods=['POST'])
def terminate():
    name = request.form.get('name')
    print(name)
    store_nervousness_data(name, nervousness_counts['weak'], nervousness_counts['strong'], nervousness_counts['neutral'])
    print("faffafffa")
    return 'Data stored successfully'

def generate_frames(name):
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = process_frame(frame, name)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

if __name__ == '__main__':
    app.run(debug=True)

