# Cisco Meraki MV RTSP Annotation using CV2
This application can be used if you want to overlay information on top of the video stream of a Meraki MV camera (or any RTSP stream). This program uses OpenCV.

### Example use case:
Integration with a POS provider to add an overlay with purchase information in real-time as transactions occur. 

#### Architecture
This system will ingest data coming from a web server and plot the text data on top of the image. Here's the overall architecture:

![Architecture](images/architecture.png)

1) Establish the RTSP stream to the camera's local IP;
2) Make an HTTP GET Request to an external web server to download the information that needs to be annotated;
3) Take one frame out of the stream (from step 1), add the data (obtained on step 2) and show the output to the user.
4) Repeat indefinitely (until user closes the program or presses q on the keyboard).


To easily install or upgrade to the latest release, use [pip](http://www.pip-installer.org/).

#### Environment
You are going to need to install OpenCV and requests. I tested this on the specified versions, but anything greater than that should work fine, until proven the contrary.
  
```shell
pip install -r requirements.txt
```

#### Sample setup
For this example, I am using the following:
- Cisco Meraki MV12W;
- Sample webserver hosted at Google Cloud ([URL](https://us-central1-ise-mailer-analyzer-206320.cloudfunctions.net/cashier)) that returns the following:
    - The current time at the server
    - A random number between 0 and 1000 and 9 numbers after that.
    - The server encapsulates this as a .txt file.
    - The used web server code is provided as part of this repository for reference only on the file `webserver_sample.py`. It is a Flask web server if you are wondering. No, you do not have to necessarily run this server. 

#### Sample output 
![Sample output](images/video.gif)
Please note that on this video, the lag is expected, since I am only processing 1 out of every 16 frames. Since the camera is configured to record at 720p - 500 kbps at 8 fps, I am always skipping one second. The second that I am waiting, is the time that it takes to engage with the web server.

### Improvements
- Make this a multi-threaded program, where the interaction with the web server is independent to the processing of the video feed. An idea to accomplish this would be to have a separate thread do the HTTP GET request and save the content on a local .txt file, which would be consumed by the main user thread (image window)

If you like this project or if you have any questions, feel free to reach out:
[LinkedIn](http://linkedin.com/in/rafaelloureirodecarvalho/?locale=en_US)