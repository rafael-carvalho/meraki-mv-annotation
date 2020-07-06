# RTSP Annotation using CV2
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

#### Environment
For this example, I am using the following:
- Meraki MV12W;
- Sample webserver hosted at Google Cloud ([URL](https://us-central1-ise-mailer-analyzer-206320.cloudfunctions.net/cashier)) that returns the following:
    - The current time at the server
    - A random number between 0 and 1000 and 9 numbers after that.
    - The server encapsulates this as a .txt file.
    - The used web server code is provided as part of this repository for reference only on the file `webserver_sample.py`. It is a Flask web server if you are wondering. No, you do not have to necessarily run this server. 

#### Sample output 
![Sample output](images/video.gif)

[LinkedIn](http://linkedin.com/in/rafaelloureirodecarvalho/?locale=en_US)