# CADisp

**CADisp** stands for **C**abine **A**uxiliary **Disp**lay, and as such, its
purpose is to provide a simple framework to display _some stuff_
on an auxiliary screen inside a driving simulator cabine.

Further down the road, it also became used to set up a digital dashboard 
_(link to future fork)_ or eye tracker calibration _(link to future
fork)_.

![CADisp_header](https://user-images.githubusercontent.com/58741440/130824270-9ae9d6b0-0526-4263-8135-c8d72b99a5f7.jpg)

## How does it work ?

CADisp is essentially a `PyQt5` application to which a transportation
layer has been added, either using a Pub-Sub communication layer from
`pyzmq`, or a using a web server.

The `PyQt5` application takes care of what is displayed on the screen and
how to react to events.

The transportation layer is used to receive events from outside the
application, or to send application events to the outside world.

## How to install it ?

_The following suppose you have Python 3 installed. If not, start with that._

1. First, either get the code by cloning the repository with Git:

        $ git clone git@github.com:uge-lescot/CADisp.git

    or download it by clicking on `Code` then `Download ZIP`, and extract it.

2. Set up a virtual environment, then activate it:

        $ py -m venv .\CADisp\venv
        $ .\CADisp\venv\Scripts\activate

3. Install dependencies:

        $ py -m pip install -r .\CADisp\requirements.txt

## How to use it ?

To start the application, just run `main_server.py`:

    $ py main_server.py

This will start displaying the GUI defined in `cadisp\dashboard.py`, as well as
a server listening to outside events.

Once the application is running, one can send messages to the application server:

    $ py main_client.py -a autonomous
