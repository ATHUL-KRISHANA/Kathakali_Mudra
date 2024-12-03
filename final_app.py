
import cv2
import mediapipe as mp
import math
import streamlit as st

# Initialize MediaPipe Hands and drawing utils
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://as1.ftcdn.net/v2/jpg/07/62/94/34/1000_F_762943499_p6HYGomjBS1j9e2S1nJatUpfk77wbAsA.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    height: 100vh; /* Ensures it covers the full viewport height */
}

[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.5);
}

/* Change the color of titles and paragraphs */
h1 {
    color: white;
}

p, div {
    color: black;
}

/* Watermark styling */
.watermark {
    position: fixed; /* Fixed position to stay in place */
    bottom: 10px;    /* Position it at the bottom */
    right: 10px;     /* Position it at the right */
    opacity: 0.5;    /* Make it semi-transparent */
    font-size: 20px; /* Font size */
    color: white;    /* Text color */
    z-index: 9999;   /* Ensure it is on top */
    pointer-events: none; /* Prevent interaction with the watermark */
}
</style>
'''

# Inject the CSS into the Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)


# Streamlit app configuration
st.title("Mudra recognizer")

# Set up session state for recording control
if 'recording' not in st.session_state:
    st.session_state.recording = False
    st.session_state.video_capture = None

# Start and Stop buttons
start_button = st.button("Start")
stop_button = st.button("Stop")

# Capture video stream using OpenCV
if start_button and not st.session_state.recording:
    st.session_state.video_capture = cv2.VideoCapture(0)
    st.session_state.recording = True
    st.text("Camera started...")

# Stop video recording when Stop button is pressed
if stop_button and st.session_state.recording:
    st.session_state.video_capture.release()
    st.session_state.recording = False
    st.text("Camera stopped.")

# Streamlit image placeholder for webcam feed
frame_window = st.image([])

# List for finger tip landmarks
tipids = [4, 8, 12, 16, 20]

# Calculate Euclidean Distance
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Webcam feed loop and finger counting logic
while st.session_state.recording:
    suc, frame = st.session_state.video_capture.read()

    if not suc:
        st.warning("Unable to access the webcam. Please check your camera.")
        break

 
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((cx, cy))

            if len(landmarks) == 21:
                thumb_tip = landmarks[4]
                index_tip = landmarks[8]
                middle_tip = landmarks[12]
                ring_tip = landmarks[16]
                pinky_tip = landmarks[20]

                distance_thumb_index = euclidean_distance(thumb_tip, index_tip)

                if distance_thumb_index < 30:  
                    
                    middle_tip = landmarks[12]
                    ring_tip = landmarks[16]
                    pinky_tip = landmarks[20]

                    middle_knuckle = landmarks[10]
                    ring_knuckle = landmarks[14]
                    pinky_knuckle = landmarks[18]

                    if (middle_tip[1] < middle_knuckle[1] and
                        ring_tip[1] < ring_knuckle[1] and
                        pinky_tip[1] < pinky_knuckle[1] and
                        landmarks[8][1] >landmarks[10][1] and
                        landmarks[8][1]> landmarks[14][1]):
                        if landmarks[6][1]>landmarks[10][1] and middle_tip[1]<ring_tip[1]:
                            print("Mudraakhyam")
                            cv2.putText(frame,'Mudraakhyam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                    elif (landmarks[20][1]< landmarks[18][1] and
                          landmarks[16][1] < landmarks[14][1] and
                          landmarks[12][1]>landmarks[10][1]
                          and landmarks[15][1]<landmarks[20][1]
                          and landmarks[4][1]<landmarks[12][1]):
                          distance_thumb_pinky=euclidean_distance(thumb_tip,pinky_tip)
                          if distance_thumb_pinky>60:
                            print('kattakam')
                            cv2.putText(frame,'kattakam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                            
   
                    elif (ring_tip[1]< ring_knuckle[1] and
                          pinky_tip[1] < pinky_knuckle[1] and
                          landmarks[12][1]<landmarks[4][1] and
                          landmarks[15][1]<landmarks[20][1]): 
                        distance_thumb_pinky=euclidean_distance(thumb_tip,pinky_tip)
                        if distance_thumb_pinky>75:
                            print('hamsasyam')   
                            cv2.putText(frame,'hamsasyam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                   
                    else:


                        
                        print('NOt identifie')
                        cv2.putText(frame,'NOt identifie ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)

                        
                elif(landmarks[4][1]<landmarks[2][1] and
                     landmarks[8][1]<landmarks[6][1] and
                     landmarks[12][1]<landmarks[10][1] and
                     landmarks[16][1]>landmarks[14][1] and
                     landmarks[20][1]<landmarks[18][1] ):
                    distance_thumb_index = euclidean_distance(thumb_tip, index_tip)
                    if distance_thumb_index>170:
                        print('pathakka')
                        cv2.putText(frame,'pathakka ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                elif(landmarks[4][0]<landmarks[3][0] and
                     landmarks[8][1]>landmarks[5][1] and
                     landmarks[12][1]> landmarks[9][1] and
                     landmarks[16][1]> landmarks[13][1] and
                     landmarks[20][1]> landmarks[17][1]):
                    print('mushti')
                    cv2.putText(frame,'mushti ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                elif (landmarks[4][1]<= landmarks[17][1] and
                     landmarks[8][1]<=landmarks[17][1] and
                     landmarks[12][1]<= landmarks[17][1] and
                     landmarks[16][1]<= landmarks[17][1] and
                     landmarks[20][1]< landmarks[17][1] and
                     landmarks[18][1]<landmarks[14][1] and 
                     landmarks[18][1]<landmarks[10][1] and 
                     landmarks[6][1]>landmarks[18][1]):
                    distance_thumb_index_pin=euclidean_distance(landmarks[4],landmarks[6])
                    distance_thumb_index = euclidean_distance(thumb_tip, index_tip)
                    if distance_thumb_index_pin<40 and distance_thumb_index>50:

                        print('Kartharee Mukham')
                        cv2.putText(frame,'Kartharee Mukham ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                elif(landmarks[4][0]<landmarks[3][0] and
                     landmarks[8][1]>landmarks[6][1] and
                     landmarks[12][1]> landmarks[9][1] and
                     landmarks[16][1]> landmarks[14][1] and
                     landmarks[20][1]> landmarks[17][1]):
                    print('sukathundam')
                    cv2.putText(frame,'sukathundam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                elif(landmarks[4][0]<landmarks[3][0] and
                     landmarks[8][1]<landmarks[6][1] and
                     landmarks[12][1]< landmarks[10][1] and
                     landmarks[16][1]> landmarks[14][1] and
                     landmarks[20][1]> landmarks[17][1]):
                    distance_index_middel=euclidean_distance(index_tip,middle_tip)

                    if distance_index_middel<50:
                        print('Kapithakam')
                        cv2.putText(frame,'Kapithakam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                    else:
                        print('sikharam')
                        cv2.putText(frame,'sikharam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                elif(landmarks[4][1]<landmarks[2][1] and
                     landmarks[8][1]<landmarks[6][1] and
                     landmarks[12][1]< landmarks[10][1] and
                     landmarks[16][1]< landmarks[14][1] and
                     landmarks[20][1]< landmarks[18][1]):
                    if  landmarks[4][0]>landmarks[3][0]:
                        if distance_thumb_index>175 :
                            print('Hamsapaksham')
                            cv2.putText(frame,'Hamsapaksham ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                        else:
                            distance__thumb_index_pip=euclidean_distance(thumb_tip,landmarks[5])
                            if landmarks[12][1]<landmarks[11][1]:
                                print('thripathaka')
                                cv2.putText(frame,'thripathaka ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                    else:
                            print('palavam')
                            cv2.putText(frame,'palavam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
        

                elif(
                     landmarks[8][1]>landmarks[6][1] and
                     landmarks[12][1]> landmarks[10][1] and
                     landmarks[16][1]< landmarks[14][1] and
                     landmarks[20][1]< landmarks[18][1]and 
                     landmarks[6][1] <landmarks[14][1] and
                     landmarks[10][1]< landmarks[14][1]):
                    distance_thumb_middel=euclidean_distance(thumb_tip,middle_tip)
                    if distance_thumb_index<30 and distance_thumb_middel<30:
                        print('hamsaasyam')
                        cv2.putText(frame,'hamsaasyam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=4,fontScale=1)
                elif (landmarks[4][1]>landmarks[3][1] and
                      landmarks[8][1]<landmarks[7][1] and
                      landmarks[12][1]>landmarks[9][1] and
                      landmarks[16][1]>landmarks[13][1] and
                      landmarks[20][1]> landmarks[17][1]):
                    print('ardhachandhanam')
                    cv2.putText(frame,'ardhachandhanam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=4,fontScale=1)
                elif (landmarks[4][1]<landmarks[3][1] and
                      landmarks[8][1]>landmarks[6][1] and
                      landmarks[12][1] <landmarks[11][1] and
                      landmarks[16][1] <landmarks[15][1] and
                      landmarks[20][1] <landmarks[19][1]):
                    distance_thumb_middel = euclidean_distance(thumb_tip, middle_tip)
                    if distance_thumb_middel>110:
                        print('bramaram')
                        cv2.putText(frame,'bramaram ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                elif(landmarks[4][0]<landmarks[3][0] and
                     landmarks[8][1]<landmarks[7][1] and
                     landmarks[12][1]>landmarks[9][1] and
                     landmarks[16][1]>landmarks[13][1] and
                     landmarks[20][1]>landmarks[17][1]):
                    distance_thumb_ring=euclidean_distance(thumb_tip,landmarks[14])
                    if distance_thumb_ring<50:
                        print('soochimukham')
                        cv2.putText(frame,'soochimukham ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                elif(landmarks[20][1]<landmarks[19][1] and
                     landmarks[8][1]<landmarks[7][1] and
                     landmarks[10][1]>landmarks[6][1] and
                     landmarks[14][1]>landmarks[18][1] 
                     ):
                    distance_thumb=euclidean_distance(thumb_tip,index_tip)
                    distance_thumb_middel=euclidean_distance(thumb_tip,middle_tip)
                    if distance_thumb_index<130 and distance_thumb_middel<30:
                    
                        print('mrigashershanam')
                        cv2.putText(frame,'mrigashershanam ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)
                    else:
                        print('mukuram')
                        
                        cv2.putText(frame,'mukuram ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)

                else:
                    print('NO mudra identified')
                    cv2.putText(frame,'NO mudra identified ',(300,300),cv2.FONT_HERSHEY_COMPLEX,color=(255,0,255),thickness=2,fontScale=1)

                
            

            # Draw hand landmarks
            # mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    frame_window.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
# Clean up resources
if not st.session_state.recording and st.session_state.video_capture:
    st.session_state.video_capture.release()
    cv2.destroyAllWindows()

st.markdown('<div class="watermark">athul</div>', unsafe_allow_html=True)

