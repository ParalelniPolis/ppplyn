# Gas measurement in Paralelni Polis

## Why

 Paralelni Polis has 3 hungry gas boilers and we want to keep an eye on amount of gas they eat.
 Doing gas reading in 2016 with pen and paper is more than cumbersome.

## Getting things ready
    sudo apt-get install ipython python-opencv python-scipy python-numpy python-pygame python-setuptools python-pip python-sklearn python-cssselect python-lxml
    sudo pip install https://github.com/sightmachine/SimpleCV/zipball/develop
    sudo pip install svgwrite
    git clone git@github.com:ParalelniPolis/ppplyn.git
    cd ppplyn

## Test image recognition on images included in repository
    ./test.py
    ./images/input/camera_1449323843.png	1474.652
    ./images/input/camera_1449323833.png	1474.648
    ./images/input/camera_1449323854.png	1474.657
    ./images/input/camera_1449323901.png	1474.678
    ./images/input/camera_1449323870.png	1474.664
    ./images/input/camera_1449323822.png	1474.643
    ./images/input/camera_1449323906.png	1474.680
    ./images/input/camera_1450650840.png	1947.815
    ./images/input/camera_1449323880.png	1474.669
    ./images/input/camera_1449323838.png	1474.650
    ./images/input/camera_1449323864.png	1474.662
    ./images/input/camera_1449323917.png	1474.685
    ./images/input/camera_1449323912.png	1474.683
    ./images/input/camera_1449323896.png	1474.675
    ./images/input/camera_1449323875.png	1474.665
    ./images/input/camera_1449323828.png	1474.645
    ./images/input/camera_1449323848.png	1474.655
    ./images/input/camera_1449323859.png	1474.635
    ./images/input/camera_1449323891.png	1474.673
    ./images/input/camera_1449323885.png	1474.671

## Tools for camera settings
    v4l2-ctl --set-ctrl brightness=100
    # This needs to be done after reboot
    v4l2-ctl --list-ctrls
    # List options for current webcam
    v4l2-ctl --info

## Detecting digits

### Source image
This is raw image taken by the camera. Camera is positioned slightly above the meter to prevent any reflections.

![Gas meter](docs/board7.png)

### Marker detection
We have 4 oragne markers in each corner of the meter. This color can be easily detected on the image.

![Gas meter with markers](docs/image_with_markers.png)

### Gas meter with fixed perspective
Knowing position of each corner, we can transform image to rectangle. This helps us estimate position of the digits we are looking for.

![Fixed perspective](docs/fixed_perspective.png)

### Digits detection
Now we can assume in which area of the image is each digit. These coordinates are hardcoded in the detector.

![Fixed perspective](docs/fixed_perspective_boxes.png)

### Single digits
Now we are ready find blobs (digits) in each rectangle. With some black magic we can ignore blobs which are not digits, reflections and crap we are not interested in.

![Digits 5](docs/5.png) ![Digit 7](docs/7.png) ![Digit 3](docs/3.png) ![Digit 9](docs/9.png)

## Machine learning
Currently we have two classificators used for digit recognition.

* [SVCDigitDetector](SVCDigitDetector.py) - Detector based on LinearSVC from Scikit
* [TemplateDigitDetector](TemplateDigitDetector.py) - Dumb detector substracting two images and measuring the difference

Feel free to implement any other detector, it just needs to have method ```detect_digit()```

At some point I want to implement ideas mentioned in [this article](http://joshmontague.com/posts/2016/mnist-scikit-learn/)

## Training dataset
This [dataset](images/dataset) is used for training of image recognition algoritm.

    for i in {0..9}; do echo -n "Digit $i "; echo "`ls $i/*.png | wc -l` samples"; done
    Digit 0      481 samples
    Digit 1      452 samples
    Digit 2       99 samples
    Digit 3       79 samples
    Digit 4      409 samples
    Digit 5      142 samples
    Digit 6      102 samples
    Digit 7      294 samples
    Digit 8      153 samples
    Digit 9      420 samples

## Testing dataset
Testing [dataset](images/dataset-test) contains images which are not prsent in the Training dataset

    for i in {0..9}; do echo -n "Digit $i "; echo "`ls $i/*.png | wc -l` samples"; done
    Digit 0       68 samples
    Digit 1       77 samples
    Digit 2       31 samples
    Digit 3       65 samples
    Digit 4      100 samples
    Digit 5       94 samples
    Digit 6       56 samples
    Digit 7       91 samples
    Digit 8       70 samples
    Digit 9       99 samples

## Testing digit detectors
Currently we have two ways how to detect digits. *SVCDigitDetector* (LinearSVC - best) and *TemplateDigitDetector* (template substraction - poor).

There is a simple tool which tests detectors with the testing dataset.

    ./test_detectors.py
    svc_digit:0 template_digit:0
    svc_digit:0 template_digit:0
    svc_digit:0 template_digit:0
    svc_digit:0 template_digit:0
    svc_digit:0 template_digit:0
    svc_digit:0 template_digit:0
    svc_digit:0 template_digit:0
    ...
    ...
    svc_digit:9 template_digit:0
    svc_digit:9 template_digit:0
    svc_digit:9 template_digit:8
    svc_digit:9 template_digit:0
    svc_digit:9 template_digit:0
    svc_digit:9 template_digit:0
    svc_digit:9 template_digit:8
    svc_digit:9 template_digit:0
    svc_digit:9 template_digit:8
    SVCDigitDetector    99.3342210386%
    TemplateDigitDetector   76.0319573901%


## Physical setup

* ODROID-U3
* Microsoft LifeCam HD-3000
* 3D printed cover from [MakerLab](http://makerslab.cz/) *TBC*
* LED strips
* Tons of epoxy glue

![Camera from the front side](docs/camera_front.jpg) ![Camera from the back side](docs/camera_back.jpg)