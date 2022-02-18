from PyQt5 import QtGui, QtCore
import pygame.mixer


class Mode:
    """
    This class stores the logo and sound associated to a mode, and is able to update the display or play a sound
    """

    def __init__(self, image_file, sound_file, looped=False):
        """
        Constructor
        """
        self._image = str(image_file)  # PyQt5 does not seem to support Path objects
        self._sound = str(sound_file)  # PyQt5 does not seem to support Path objects
        self._looped = looped
        pygame.mixer.init()  # Required to play audio files

    def update_display(self, qlabel, qsize):
        """
        Display the mode's logo on the screen
        """

    def play_sound(self):
        """"
        Play the mode's audio file
        """
        if self._sound != "":
            pygame.mixer.music.load(self._sound)
            if self._looped:
                pygame.mixer.music.play(loops=-1)
            else:
                pygame.mixer.music.play()

        else:
            pygame.mixer.music.stop()


class StaticImage(Mode):
    """
    Specific case of a static image
    """

    def update_display(self, qlabel, qsize):
        """
        Display the mode's static logo on the screen
        """
        scaledpixmap = QtGui.QPixmap(self._image).scaled(qsize, QtCore.Qt.KeepAspectRatio,
                                                         QtCore.Qt.SmoothTransformation)
        qlabel.setPixmap(scaledpixmap)


class AnimatedImage(Mode, QtCore.QThread):
    """
    Specific case of an animated image
    """
    sig_end_animation = QtCore.pyqtSignal()

    def __init__(self, image_file, sound_file, looped=False, parent=None):
        """
        Constructor
        """
        QtCore.QThread.__init__(self, parent)
        Mode.__init__(self, image_file, sound_file, looped)

    def update_display(self, qlabel, qsize):
        """
        Display the mode's animated logo on the screen
        """
        scaledmovie = QtGui.QMovie(self._image)

        # Get the QSize object defining the QMovie size
        # /!\ The QSize obtained below is (-1,-1), so aspect ratio will be broken if it is not a square
        size = scaledmovie.scaledSize()
        # Scale to height the QSize object
        size.scale(qsize, QtCore.Qt.KeepAspectRatio)
        # Scale the QMovie object to the QSize one
        scaledmovie.setScaledSize(size)
        qlabel.setMovie(scaledmovie)
        scaledmovie.start()

        # Link the signal to the one emitted at the end of QMovie
        # noinspection PyUnresolvedReferences
        scaledmovie.finished.connect(self.sig_end_animation)
