# Gas measurement in Paralelni Polis

## Why

 *Work in progress...*

## Getting things ready
    sudo apt-get install ipython python-opencv python-scipy python-numpy python-pygame python-setuptools python-pip
    sudo pip install https://github.com/sightmachine/SimpleCV/zipball/develop
    sudo pip install svgwrite
    git clone git@github.com:ParalelniPolis/ppplyn.git
    cd ppplyn

## Test image recognition on images included in repository
    ./test.py
    ./images/input/camera_1449323822.png    1474643
    ./images/input/camera_1449323828.png    147464
    ./images/input/camera_1449323833.png    1474648
    ./images/input/camera_1449323838.png    147465
    ./images/input/camera_1449323843.png    1474652
    ./images/input/camera_1449323848.png    147465
    ./images/input/camera_1449323854.png    147465
    ./images/input/camera_1449323859.png    14746
    ./images/input/camera_1449323864.png    1474662
    ./images/input/camera_1449323870.png    147466
    ...
    ...

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

### Digits
We crop the image to contain only digits

![Digits in color](docs/digits_area.png)

### Digits in black and white
Digits are white, lets ignore anything else

![Digits in black and white](docs/white_digits.png)

### Single digits
Now we are ready find blobs (digits) in the image. With some black magic we can ignore blobs which are not digits, reflections and crap we are not interested in.

![Digits 5](docs/5.png) ![Digit 7](docs/7.png) ![Digit 3](docs/3.png) ![Digit 9](docs/9.png)

## Machine learning
 *Work in progress...*

## Physical setup

* ODROID-U3
* Microsoft LifeCam HD-3000
* 3D printed cover from [MakerLab](http://makerslab.cz/) *TBC*
* LED strips
* Tons of epoxy glue

![Camera from the front side](docs/camera_front.jpg) ![Camera from the back side](docs/camera_back.jpg)