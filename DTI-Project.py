import cv2
import face_recognition

video_capture = cv2.VideoCapture(0)

def detect_faces(vid):
    face_locations = face_recognition.face_locations(vid)
    return face_locations

def compare_faces(face1, face2):
    encoding1 = face_recognition.face_encodings(face1)[0]
    encoding2 = face_recognition.face_encodings(face2)[0]
    results = face_recognition.compare_faces([encoding1], encoding2)
    return results[0]

while True:
    ret, video_frame = video_capture.read()

    if not ret:
        break

    faces = detect_faces(video_frame)

    if len(faces) == 2:
        face1 = video_frame[faces[0][0]:faces[0][2], faces[0][3]:faces[0][1]]
        face2 = video_frame[faces[1][0]:faces[1][2], faces[1][3]:faces[1][1]]
        matched = compare_faces(face1, face2)
        if matched:
            text = "Matched"
        else:
            text = "Different Faces"
    else:
        text = "Faces not detected" if len(faces) == 0 else "Only one face detected"

    cv2.putText(video_frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("My Face Detection Project", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
