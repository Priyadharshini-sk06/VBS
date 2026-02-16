# from flask import Flask, Response, jsonify, request, render_template, redirect, url_for, send_from_directory
# from flask_socketio import SocketIO
# import cv2, mediapipe as mp, joblib, time, atexit, threading, webbrowser, random
# import pyttsx3
# import os
# import comtypes.client

# # ===============================
# # APP
# # ===============================
# app = Flask(__name__, template_folder="../templates", static_folder="../static")
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# CURRENT_MODE = "SPELL"

# UPLOAD_FOLDER = "uploads"
# SLIDE_FOLDER = os.path.join(UPLOAD_FOLDER, "slides")
# os.makedirs(SLIDE_FOLDER, exist_ok=True)

# # ===============================
# # MODEL
# # ===============================
# model = joblib.load("../ml/models/sign_model.pkl")

# # ===============================
# # TTS (NON-BLOCKING)
# # ===============================
# def speak(text):
#     if not text.strip():
#         return

#     def run():
#         engine = pyttsx3.init()
#         engine.setProperty("rate", 150)
#         engine.say(text)
#         engine.runAndWait()

#     threading.Thread(target=run, daemon=True).start()

# # ===============================
# # MEDIAPIPE
# # ===============================
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# mp_draw = mp.solutions.drawing_utils

# # ===============================
# # CAMERA
# # ===============================
# cap = cv2.VideoCapture(0)

# # ===============================
# # STATE
# # ===============================
# current_letter = None
# current_word = ""
# letter_start_time = 0
# HOLD_TIME = 1.0

# # ===============================
# # VIDEO STREAM
# # ===============================
# def generate_frames():
#     global current_letter, current_word, letter_start_time

#     while True:
#         success, frame = cap.read()
#         if not success:
#             continue

#         frame = cv2.flip(frame, 1)
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         result = hands.process(rgb)

#         if result.multi_hand_landmarks:
#             lm = result.multi_hand_landmarks[0].landmark
#             mp_draw.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

#             data = []
#             for p in lm:
#                 data.extend([p.x, p.y, p.z])

#             detected = model.predict([data])[0]
#             now = time.time()

#             if detected != current_letter:
#                 current_letter = detected
#                 letter_start_time = now

#             elif now - letter_start_time >= HOLD_TIME:

#                 if CURRENT_MODE == "SPELL":
#                     socketio.emit("transcript", detected)
#                     speak(detected)

#                 elif CURRENT_MODE == "WORD":
#                     socketio.emit("transcript", detected + " ")
#                     speak(detected)

#                 elif CURRENT_MODE == "QA":
#                     socketio.emit("qa_complete", detected)
#                     speak(detected)

#                 current_letter = None
#                 letter_start_time = 0

#             cv2.putText(frame, f"{CURRENT_MODE}: {detected}", (20, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

#         cv2.putText(frame, f"MODE: {CURRENT_MODE}", (20, 90),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

#         _, buffer = cv2.imencode(".jpg", frame)
#         yield (b"--frame\r\n"
#                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

# # ===============================
# # ROUTES
# # ===============================
# @app.route("/")
# def home(): return render_template("home.html")

# @app.route("/presentation")
# def presentation(): return render_template("presentation.html")

# @app.route("/video_feed")
# def video_feed():
#     return Response(generate_frames(),
#                     mimetype="multipart/x-mixed-replace; boundary=frame")

# @app.route("/mode", methods=["POST"])
# def set_mode():
#     global CURRENT_MODE
#     CURRENT_MODE = request.json.get("mode", "SPELL")
#     return jsonify({"mode": CURRENT_MODE})

# # ===============================
# # PPT UPLOAD → SLIDES
# # ===============================
# @app.route("/upload-ppt", methods=["POST"])
# def upload_ppt():
#     ppt = request.files["ppt"]
#     ppt_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, ppt.filename))
#     ppt.save(ppt_path)

#     powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
#     presentation = powerpoint.Presentations.Open(ppt_path)
#     presentation.SaveAs(os.path.abspath(SLIDE_FOLDER), 17)  # JPG
#     presentation.Close()
#     powerpoint.Quit()

#     slides = sorted(os.listdir(SLIDE_FOLDER))
#     return jsonify({"slides": slides})

# @app.route("/uploads/<path:filename>")
# def uploads(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

# # ===============================
# # CLEANUP
# # ===============================
# @atexit.register
# def cleanup():
#     cap.release()
#     cv2.destroyAllWindows()

# # ===============================
# # RUN
# # ===============================
# if __name__ == "__main__":
#     threading.Thread(
#         target=lambda: (time.sleep(1), webbrowser.open("http://127.0.0.1:5000/presentation")),
#         daemon=True
#     ).start()

#     socketio.run(app, host="127.0.0.1", port=5000, debug=False)


from flask import Flask, Response, jsonify, request, render_template, redirect, url_for
from flask_socketio import SocketIO
import cv2, mediapipe as mp, joblib, time, atexit, threading, webbrowser, random
import pyttsx3
from pptx import Presentation
import os
from flask import send_from_directory
# ===============================
# APP
# ===============================
app = Flask(__name__, template_folder="../templates", static_folder="../static")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

CURRENT_MODE = "SPELL"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ===============================
# MODEL
# ===============================
model = joblib.load("../ml/models/sign_model.pkl")

# ===============================
# TTS
# ===============================
def speak(text):
    if not text.strip():
        return

    def run():
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run, daemon=True).start()



# ===============================
# MEDIAPIPE
# ===============================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# ===============================
# CAMERA
# ===============================
cap = cv2.VideoCapture(0)

# ===============================
# STATE
# ===============================
current_letter = None
current_word = ""
letter_start_time = 0
HOLD_TIME = 1.0
last_hand_time = time.time()
HAND_GAP_TIME = 2.0
hand_present_last = False
# ===============================
# VIDEO STREAM
# ===============================
def generate_frames():
    global current_letter, current_word, letter_start_time, last_hand_time
    # if request.path == "/practice" and CURRENT_MODE == "QA":
    #     CURRENT_MODE = "SPELL"

    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        hand_present = False

        if result.multi_hand_landmarks:
            hand_present = True
            last_hand_time = time.time()

            lm = result.multi_hand_landmarks[0].landmark
            mp_draw.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
            
            if CURRENT_MODE == "SPELL":
                data = []
                for p in lm:
                    data.extend([p.x, p.y, p.z])

                detected = model.predict([data])[0]
                now = time.time()

                if detected != current_letter:
                    current_letter = detected
                    letter_start_time = now
                elif now - letter_start_time >= HOLD_TIME:
                    current_word += detected
                    speak(current_word)   
                    socketio.emit("transcript", detected)
                    current_letter = None
                    letter_start_time = 0

                cv2.putText(frame, f"Detected: {detected}", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            elif CURRENT_MODE == "WORD":
                data = []
                for p in lm:
                    data.extend([p.x, p.y, p.z])

                detected = model.predict([data])[0]
                now = time.time()

                if detected != current_letter:
                    current_letter = detected
                    letter_start_time = now

                elif now - letter_start_time >= HOLD_TIME:
                    current_word = detected
                    speak(current_word)   # 🔊 ADD THIS LINE
                    socketio.emit("transcript", detected + " ")
                    current_letter = None
                    letter_start_time = 0


                cv2.putText(frame, f"Word: {current_word}", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 255), 2)

         # qa mode
            elif CURRENT_MODE == "QA":
                data = []
                for p in lm:
                    data.extend([p.x, p.y, p.z])

                detected = model.predict([data])[0]
                now = time.time()

                if detected != current_letter:
                    current_letter = detected
                    letter_start_time = now

                elif now - letter_start_time >= HOLD_TIME:
                    current_word += detected
                    socketio.emit("qa_answer", detected)
                    socketio.emit("qa_complete", current_word)
                    current_letter = None
                    letter_start_time = 0

                cv2.putText(frame, f"Answering: {current_word}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            if CURRENT_MODE != "WORD" and not hand_present and current_word and time.time() - last_hand_time >= HAND_GAP_TIME:
                if CURRENT_MODE == "WORD":
                    speak(current_word)     # 🔊 SPEAK FULL WORD
                    socketio.emit("transcript", " " + current_word + " ")

                if CURRENT_MODE == "SPELL":
                    speak(current_word)     # optional
                    socketio.emit("transcript", " " + current_word + " ")

                if CURRENT_MODE == "QA":
                    speak(current_word)
                    socketio.emit("qa_complete", current_word)

                current_word = ""
                current_letter = None


            hand_present_last = hand_present

            cv2.putText(frame, f"MODE: {CURRENT_MODE}", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

# ===============================
# ROUTES – FLOW
# ===============================
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("sign2speech"))
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        return redirect(url_for("sign2speech"))
    return render_template("register.html")

@app.route("/userguide")
def userguide():
    return render_template("userguide.html")

@app.route("/connectwithus", methods=["GET", "POST"])
def connectwithus():
    if request.method == "POST":
        # you can store data later
        return redirect(url_for("home"))
    return render_template("connectwithus.html")

@app.route("/sign2speech", methods=["GET","POST"])
def sign2speech():
    if request.method == "POST":
        return redirect(url_for("mode_select"))
    return render_template("sign2speech.html")

@app.route("/mode-select")
def mode_select():
    return render_template("mode-select.html")

@app.route("/practice")
def practice():
    return render_template("practice.html")

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")

@app.route("/meeting-setup")
def meeting_setup():
    return render_template("meeting-setup.html")

@app.route("/qa")
def qa():
    return render_template("qa.html")

# ===============================
# VIDEO FEED
# ===============================
@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame")

# ===============================
# MODE SWITCH
# ===============================
@app.route("/mode", methods=["POST"])
def set_mode():
    global CURRENT_MODE
    CURRENT_MODE = request.json.get("mode", "SPELL")
    return jsonify({"mode": CURRENT_MODE})

# ===============================
# PPT UPLOAD (DEMO)
# ===============================
@app.route("/upload-ppt", methods=["POST"])
def upload_ppt():
    ppt = request.files["ppt"]
    ppt_path = os.path.join(UPLOAD_FOLDER, ppt.filename)
    ppt.save(ppt_path)

    output_dir = os.path.join(UPLOAD_FOLDER, "slides")
    os.makedirs(output_dir, exist_ok=True)

    # Convert PPT → images (Windows needs PowerPoint installed)
    import comtypes.client
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    presentation = powerpoint.Presentations.Open(os.path.abspath(ppt_path))
    presentation.SaveAs(os.path.abspath(output_dir), 17)  # 17 = JPG
    presentation.Close()
    powerpoint.Quit()

    images = sorted(os.listdir(output_dir))
    return jsonify({"slides": images})


@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ===============================
# ONLINE MEETING
# ===============================
@app.route("/meeting/create", methods=["POST"])
def create_meeting():
    meeting_id = str(random.randint(100000,999999))
    return jsonify({"meeting_id": meeting_id})

# ===============================
# QA LISTENER (DEMO)
# ===============================
@app.route("/qa/listen", methods=["POST"])
def qa_listen():
    questions = [
        "What is your project about?",
        "How does sign detection work?",
        "What model are you using?"
    ]
    return jsonify({"question": random.choice(questions)})

# ===============================
# CLEANUP
# ===============================
@atexit.register
def cleanup():
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()

# ===============================
# AUTO OPEN
# ===============================
def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    print("✅ Voice Beyond Sound running")
    threading.Thread(target=open_browser).start()
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)


# from flask import Flask, Response, jsonify, request, render_template
# from flask_socketio import SocketIO
# import cv2, mediapipe as mp, joblib, time, math, atexit
# import pyttsx3
# import webbrowser

# # ===============================
# # APP
# # ===============================
# app = Flask(__name__, template_folder="../templates", static_folder="../static")
# socketio = SocketIO(app, cors_allowed_origins="*")

# CURRENT_MODE = "SPELL"

# # ===============================
# # MODEL
# # ===============================
# model = joblib.load("../ml/models/sign_model.pkl")

# # ===============================
# # TTS
# # ===============================
# engine = pyttsx3.init()
# engine.setProperty("rate", 150)

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # ===============================
# # MEDIAPIPE
# # ===============================
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(max_num_hands=1)
# mp_draw = mp.solutions.drawing_utils

# # ===============================
# # CAMERA
# # ===============================
# cap = cv2.VideoCapture(0)

# # ===============================
# # STATE
# # ===============================
# current_letter = None
# current_word = ""
# letter_start_time = 0
# HOLD_TIME = 1.0
# hand_present_last = False

# # ===============================
# # STREAM
# # ===============================
# def generate_frames():
#     global current_letter, current_word, letter_start_time, hand_present_last

#     while True:
#         success, frame = cap.read()
#         if not success:
#             continue

#         frame = cv2.flip(frame, 1)
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         result = hands.process(rgb)

#         hand_present = False

#         if result.multi_hand_landmarks:
#             hand_present = True
#             lm = result.multi_hand_landmarks[0].landmark

#             mp_draw.draw_landmarks(
#                 frame,
#                 result.multi_hand_landmarks[0],
#                 mp_hands.HAND_CONNECTIONS
#             )

#             if CURRENT_MODE == "SPELL":
#                 data = []
#                 for p in lm:
#                     data.extend([p.x, p.y, p.z])

#                 detected = model.predict([data])[0]
#                 now = time.time()

#                 if detected != current_letter:
#                     current_letter = detected
#                     letter_start_time = now

#                 elif now - letter_start_time >= HOLD_TIME:
#                     current_word += detected
#                     socketio.emit("transcript", detected)
#                     letter_start_time = now
#                     current_letter = None

#                 cv2.putText(frame, f"Letter: {detected}", (20, 50),
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

#         # 🔥 HAND REMOVED = WORD COMPLETE
#         if not hand_present and hand_present_last and current_word:
#             speak(current_word)
#             socketio.emit("transcript", " " + current_word + " ")
#             current_word = ""
#             current_letter = None

#         hand_present_last = hand_present

#         cv2.putText(frame, f"MODE: {CURRENT_MODE}", (20, 90),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

#         _, buffer = cv2.imencode(".jpg", frame)
#         frame = buffer.tobytes()

#         yield (b"--frame\r\n"
#                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

# # ===============================
# # ROUTES
# # ===============================
# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/presentation")
# def presentation():
#     return render_template("presentation.html")

# @app.route("/video_feed")
# def video_feed():
#     return Response(generate_frames(),
#                     mimetype="multipart/x-mixed-replace; boundary=frame")

# @app.route("/mode", methods=["POST"])
# def set_mode():
#     global CURRENT_MODE
#     CURRENT_MODE = request.json.get("mode", "SPELL")
#     return jsonify({"mode": CURRENT_MODE})

# # ===============================
# # CLEANUP
# # ===============================
# @atexit.register
# def cleanup():
#     cap.release()
#     cv2.destroyAllWindows()

# # ===============================
# # RUN
# # ===============================

# if __name__ == "__main__":
#     webbrowser.open("http://127.0.0.1:5000/presentation")
#     socketio.run(app, port=5000, debug=False)




