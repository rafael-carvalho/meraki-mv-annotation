import cv2
import time
from datetime import datetime
import traceback
import requests

# CV2 uses BGR (Blue Green Red)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def add_text_annotation_to_video(frame, frame_counter, contextual_annotations):
    '''
    For each item on the list, I will show the text line by line.
    '''

    # Line height used to prevent a line to go on top of another.
    vertical_padding = 15
    # Do you want to have some space from the left of the image?
    horizontal_padding = 0


    # color of the printed text
    text_color = RED

    # color of the (optional) rectangle behind the text
    rectangle_color = WHITE
    # How many pixels wide do you want the rectangle to be?
    rectangle_width = 200

    prepended_annotations = list()

    # Uncomment the line below if you want to add the timestamp of the streaming device to the top of the screen
    #prepended_annotations.append(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    # prepends the current frame to the image. Comment the line below if you don't want this
    prepended_annotations.append(f'Current frame: {frame_counter}')

    annotations = prepended_annotations
    # Combine any fixed annotation to the contextual annotations
    for context in contextual_annotations:
        if context:
            annotations.append(context)

    # If you want to add a bounding rectangle to the text, uncomment this. You might need to play with the width of the
    # lines, otherwise you will have text going outside of the black box.
    #cv2.rectangle(frame, (0, 0), (rectangle_width, (len(annotations) + 1) * vertical_padding), rectangle_color, -1)

    counter = 1
    for annotation in annotations:
        if annotation:
            x = horizontal_padding
            y = counter * vertical_padding
            text_coordinates = (x, y)
            cv2.putText(frame, annotation, text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
            counter += 1

    return frame


def process_rtsp_stream_with_file_annotation(link, txt_url, fps_throttle=16, width=640, height=320):
    frame_counter = 0
    error_counter = 0
    error_threshold = 10
    annotations = None
    print(f'Initiating Stream to {link}')
    try:
        cap = cv2.VideoCapture(link)
        print('Stream established')
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if frame is None:
                error_counter += 1
                print(f'Subsequent frames lost {error_counter}')
                time.sleep(1)
                # If something wrong happens on the stream, wait for 1 second and try again. If 10 errors occur, quit.
                if error_counter == error_threshold:
                    raise Exception(f'Stream not available. Please check {link}')

            else:

                # In order to make this smoother on computers with low CPU power, I'm only processing some frames.
                if frame_counter % fps_throttle == 0:
                    if not annotations:
                        annotations = []

                    # If both width and height are given, then I will resize the image to it.
                    # This is good for computers with low CPU powers. If you pass width=None and height=None, then the program will show the image as it received from the RTSP stream
                    if width and height:
                        width = int(width)
                        height = int(height)
                        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

                    add_text_annotation_to_video(frame, frame_counter, annotations)
                    print(f'Annotating over frame {frame_counter}')
                    cv2.imshow(link, frame)
                    error_counter = 0

                # If I am not processing the frame, i.e., annotating on it, I will download the information from the server
                elif frame_counter % fps_throttle == 1:
                    annotations = fetch_annotations(txt_url)

            #If the user presses q, the program will exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_counter += 1

    except:
        traceback.print_exc()
        print('Error')

    finally:
        # When everything is done, release the RTSP stream and destroy the window
        print('Releasing resources')
        cap.release()
        cv2.destroyAllWindows()



def fetch_annotations(server_url):
    annotations = list()

    # Adding something to the URL to avoid caching issues
    right_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Makes the HTTP GET request to the webserver hosting the data
    response = requests.get(server_url + '?time='+right_now)
    if response.status_code == 200:
        filename = 'output.txt'
        with open(filename, 'wb') as input_file:
            input_file.write(response.content)
            input_file.close()
            with open(filename, 'r') as items:
                annotations = list(items)
               # print(annotations)
                items.close()
    else:
        annotations.append('Error when trying to get information from the server')
        annotations.append(f'Status code: {response.status_code}')
    return annotations


if __name__ == '__main__':
    # URL to the RTSP stream
    link = 'rtsp://192.168.100.5:9000/live'

    # URL to the server that hosts the information you want to add to the video
    pos_server_url = "https://us-central1-ise-mailer-analyzer-206320.cloudfunctions.net/cashier"

    # Let the magic begin
    process_rtsp_stream_with_file_annotation(link, pos_server_url)

