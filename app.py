from flask import Flask, render_template
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import webbrowser
import time

# Initialize Flask app
app = Flask(__name__)

# Define global variables
result_data = None
results_template = None
total_frames = None
depressed_count = None
depressed_percentage = None
not_depressed_count = None
not_depressed_percentage = None

# Route to render index.html
@app.route("/")
def landing():
    return render_template("landing-new.html")

# Route to render index.html
@app.route("/index")
def index():
    return render_template("index.html")

# Route to handle button click and execute the functionality
@app.route("/start_detection")
def start_detection():
    face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
    classifier = load_model(r'model.h5')

    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    cap = cv2.VideoCapture(0)

    depression_count = 0
    frame_count = 0
    quit_flag = False  # Flag to control the loop

    while not quit_flag:
        start_time = time.time()
        while time.time() - start_time < 30:  # Capture frames for 30 seconds
            _, frame = cap.read()
            frame_count += 1
            labels = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    prediction = classifier.predict(roi)[0]
                    if prediction.argmax() in [3, 4, 6]:  # Happy, Neutral, Surprise
                        label = "Not Depressed"
                    else:
                        label = "Depressed"
                        depression_count += 1

                    label_position = (x, y)
                    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Emotion Detector', frame)

            # Check for 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                quit_flag = True
                break

        depressed_percentage = (depression_count / frame_count) * 100
        not_depressed_percentage = 100 - depressed_percentage

        if depression_count > 10:  # Arbitrary threshold for depression count
            result = "You are depressed."
            result_color = "red"
        else:
            result = "You are not depressed."
            result_color = "green"

        # HTML content
        result_html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Embrace Well</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='result.css') }}">
    <link href="https://fonts.googleapis.com/css2?family=Audiowide:wght@400&amp;display=swap" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

        body {{
            font-family: 'Poppins', sans-serif;
            background-color: rgba(20, 22, 46, 1);
            margin: 0;
            padding: 0;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            background-color: rgba(243, 243, 252, 1);
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            position: relative;
        }}

        h1 {{
    color: rgba(22, 120, 242, 1);
    font-weight: 600;
    font-size: 4rem;
    margin-bottom: 30px;
    text-align: left;
    position: relative;
    padding-left: 120px; /* Adjust the value as needed */
}}


    .embrace-image1{{
        position: absolute;
    top: 280px; /* Adjust top positioning as needed */
    right: 40px;
    ali
    transform: translate(-50%, -50%);
    width: 50%; /* Adjust size relative to h1 */
    height: auto;
        
    }}
        .embrace-image {{
    position: absolute;
    top: 45px; /* Adjust top positioning as needed */
    left: 40px;
    transform: translate(-50%, -50%);
    width: 5%; /* Adjust size relative to h1 */
    height: auto;

        }}

        .result {{
            margin-top: 30px;
            color: {result_color};
            font-weight: 500;
            font-size: 1.6rem;
            text-align: center;
        }}

        .progress-container {{
            width: 70%;
            margin: 30px auto;
            background-color: #ddd;
            border-radius: 20px;
            overflow: hidden;
        }}

       .progress-bar {{
    width: {depressed_percentage}%;
    height: 30px;
    background-color: red; /* Set the progress bar fill color to red */
    text-align: center;
    color: white;
    line-height: 30px;
    transition: width 0.5s;
    border-radius: 20px;
    font-weight: 500;
}}


        .result-details {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 40px;
        }}

        .result-details p {{
            margin: 0 20px;
            align-items: center;
            font-size: 1.2rem;
            color: #666;
        }}

        .embrace-well {{
            font-family: 'Audiowide', cursive;
            font-size: 2rem;
            position: absolute;
            top: 30px;
            left: 68px;
        }}
    </style>
</head>
<body>
    <div class="container">
     
        <img src="image.png" class="embrace-image">
        <span class="embrace-well">EMBRACE WELL</span>
        <br>
        <br>
        <br> <img src="ll.jpg" class="embrace-image2"  style="float: center;">
        <br>
        <br>
           
        
        
        <img src="kisspngphysiciandiabetesmellituscomputerdiseasepre1864-asht-1300w.png" class="embrace-image1"  style="float: right;">
           <br>
           <br>
           <br>
           <h1>RESULT
           </h1>
           <br>
           <br>
           <br>
           <br>
           <br>
           <br>
        <div>
            <div class="progress-container">
                <div class="progress-bar">{depressed_percentage}% Depressed</div>
            </div>
            <p class="result">{result}</p>
            <div class="result-details">
                <p>Total Frames: {frame_count}</p>
                <p>Depressed Frames: {depression_count}</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

        # Write HTML content to result.html
        with open("result.html", "w") as f:
            f.write(result_html_content)

        # Open result.html in default web browser
        webbrowser.open("result.html")

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
