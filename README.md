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

## How does it work

### Source image

![Gas meter](docs/board7.png)

### Marker detection

![Gas meter with markers](docs/image_with_markers.png)

### Gas meter with fixed perspective

![Fixed perspective](docs/fixed_perspective.png)

### Digits

![Digits in color](docs/digits_area.png)

### Digits in black and white

![Digits in black and white](docs/white_digits.png)

### Single digits

![Digits 5](docs/5.png) ![Digit 7](docs/7.png) ![Digit 3](docs/3.png) ![Digit 9](docs/9.png)

## Physical setup

* ODROID-U3
* Microsoft LifeCam HD-3000
* 3D printed cover from [MakerLab](http://makerslab.cz/) *TBC*
* LED strips
* Tons of epoxy glue

![Camera from the front side](docs/camera_front.jpg) ![Camera from the back side](docs/camera_back.jpg)