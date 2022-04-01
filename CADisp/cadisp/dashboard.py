# -*- coding: utf-8 -*-

#import des bibliothèques
import datetime
import os
import time
import datetime as d
import functools
from pathlib import Path
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QLineEdit
from .clients import PushClient
from .servers import ThreadedZMQServer
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Dashboard(QtWidgets.QMainWindow):
    """
    Ce script décrit la partie visuelle de l'application dans la première partie du code
    et dans la deuxième partie les fonctions callback rendant les boutons dynamiques sont décrites.

    La librairie Qt ayant besoin d'être importée pour que le scripte tourne, il est nécessaire de
    préalablement télécharger les packages.

    Voir la documentation pour plus d'informations
    """

    # definition de la taille de la fenetre et de la taille des marges
    __LAYOUT_MARGINS = 50  # in pixels
    __LOGO_WIDTH = 240  # in pixels
    __LOGO_HEIGHT = 240  # in pixels
    __NUM_SCREEN = 0  # 0 for main screen, 1 for secondary screen

    def __init__(self):
        """
        Constructor : création d'objets vides
        """
        # paramètres à modifier en cs de besoin
        self.numNavette = "navette1"

        # fenetre principale
        QtWidgets.QMainWindow.__init__(self)

        # widget
        self._main = QtWidgets.QWidget(self)

        #Compteur glabal de passager
        self.countGlobal=0


        ## Layout:
        layout = QGridLayout(self._main)

        # Definition of the different modes
        self._current_mode = ''
        pictures_folder = Path(__file__).parent.parent.resolve().joinpath('media', 'pictures')

        self._image = QtWidgets.QLabel()

        # image pour le codage temps réel
        self._QLabelimageBiengere = (str(pictures_folder / "shuttle.png"))
        self._QLabelimageMalgere = (str(pictures_folder / "shuttle_red.png"))
        self._QLabelimageRetourArr = (str(pictures_folder / "retour-arriere.png"))
        self._QLabelimagePlus = (str(pictures_folder / "plus.PNG"))
        self._QLabelimageMoins = (str(pictures_folder / "moins.PNG"))
        self._QLabelimageIncident = (str(pictures_folder / "situation_accidentelle.png"))

        # Image pour le codage si pas d'événement
        self._QLabelimageZeroEvent = (str(pictures_folder / "zero_event.png"))

        # Image commune à tous les codages pour allumer/eteindre
        self._QLabelimagePower = (str(pictures_folder / "power.png"))
        self._QLabelimageExit = (str(pictures_folder / "exit.png"))

        # Images pour les codages des véhicules en mouvement
        self._QLabelimageREfusPrioMvt = str(pictures_folder / "refus_prio_new.png")
        self._QLabelimageSortieStatioMvt = str(pictures_folder / "garage.png")
        self._QLabelimageRabattementMvt = str(pictures_folder / "no_overtaking.png")
        self._QLabelimageDepassementProcheMvt = str(pictures_folder / "remontee_file.png")
        self._QLabelimageNonRespectPrioRPMvt = str(pictures_folder / "crossroad.png")
        self._QLabelimageVitesseExcessiveMvt = str(pictures_folder / "fast.png")

        # Images pour le codage des intéractions avec les usagers vulnérables
        self._QLabelimageTraveePPVul = str(pictures_folder / "pedestrian.png")
        self._QLabelimageTraveeHorsPPVul = str(pictures_folder / "hurry.png")
        self._QLabelimageTraverseeMasquageVul = str(pictures_folder / "traversee_masquage.png")
        self._QLabelimageUsagerSortantVehiculeVul = str(pictures_folder / "sortie_vehicule_new.png")

        # Images pour le codages des événements en lien avec l'environnement
        self._QLabelimageTravauxEnvi = str(pictures_folder / "traffic-cone.png")
        self._QLabelimageIntemperiesEnvi = str(pictures_folder / "thunderstorm.png")
        self._QLabelimageVegetationEnvi = str(pictures_folder / "tree.png")
        self._QLabelimageEblouissementEnvi = str(pictures_folder / "eblouissement.png")
        self._QLabelimageStationnementGenantEnvi = str(pictures_folder / "no-car.png")
        self._QLabelimageAnimalEnvi = str(pictures_folder / "pigeon.png")

        # partie qui demarre le client (script zmq_client)
        self._server = ThreadedZMQServer()
        self._server.start()
        self._zmq_client = PushClient()

        # Configure the widgets
        screen_res = QtWidgets.QApplication.desktop().screenGeometry(self.__NUM_SCREEN)

        # paramètres liés aux options d'affichage des images
        self._image_size = QtCore.QSize(self.__LOGO_WIDTH, self.__LOGO_HEIGHT)
        self._image.setFixedSize(self._image_size)
        self._image.setAlignment(QtCore.Qt.AlignHCenter)

        # Disposition en quadrillage (5 lignes/8 colonnes):
        for row in range(4):
            for column in range(7):
                layout.addWidget(self._image, row, column)


########## Positionnement des boutons:
        """ 1ere ligne"""
        """ 
        Chaque image a la même structure de code, le 1er sera detaillé et les suivants sont identiques
        """

        ############ 1er #################
        #ajout d'une image définie à partir des lignes 64 appartenant à la classe dashboard (self) en tant que Pixmap
        scaledpixmapBienGere = QtGui.QPixmap(self._QLabelimageBiengere).scaled(self._image_size,
                                                                               QtCore.Qt.KeepAspectRatio,
                                                                               QtCore.Qt.SmoothTransformation)
        #Création d'un type bouton dans lequel on ajoutera un icone avec l'image
        self.buttonGere = QPushButton()
        #ajout de l'icone avec l'image
        self.buttonGere.setIcon(QtGui.QIcon(scaledpixmapBienGere))
        #ajuster la taille définie plus haut dans la classe
        self.buttonGere.setIconSize(self._image_size)
        #definir le nom du bouton qui sera inscrit dans le csv
        self.buttonGere.setObjectName("Bien_gérée")
        #appel d'un callback nommé "._on_click" avec paramètre suplémenataire inséré à l'aide de "functools.partial"
        self.buttonGere.mousePressEvent = functools.partial(self._on_click, name=self.buttonGere.objectName())
        #le placer a la bonne position dans le quadrillage
        layout.addWidget(self.buttonGere, 0, 1)

        ############
        scaledpixmapMalGere = QtGui.QPixmap(self._QLabelimageMalgere).scaled(self._image_size,
                                                                             QtCore.Qt.KeepAspectRatio,
                                                                             QtCore.Qt.SmoothTransformation)
        self.buttonMalGere = QPushButton()
        self.buttonMalGere.setIcon(QtGui.QIcon(scaledpixmapMalGere))
        self.buttonMalGere.setIconSize(self._image_size)
        self.buttonMalGere.setObjectName("Mal_gérée")
        self.buttonMalGere.mousePressEvent = functools.partial(self._on_click, name=self.buttonMalGere.objectName())
        layout.addWidget(self.buttonMalGere, 0, 2)
        
        
        ############
        scaledpixmapIncident = QtGui.QPixmap(self._QLabelimageIncident).scaled(self._image_size,
                                                                             QtCore.Qt.KeepAspectRatio,
                                                                             QtCore.Qt.SmoothTransformation)
        self.buttonIncident = QPushButton()
        self.buttonIncident.setIcon(QtGui.QIcon(scaledpixmapIncident))
        self.buttonIncident.setIconSize(self._image_size)
        self.buttonIncident.setObjectName("Incident")
        self.buttonIncident.mousePressEvent = functools.partial(self._on_click, name=self.buttonIncident.objectName())
        layout.addWidget(self.buttonIncident, 0, 3)


        ############
        scaledpixmapPower = QtGui.QPixmap(self._QLabelimagePower).scaled(self._image_size,
                                                                         QtCore.Qt.KeepAspectRatio,
                                                                         QtCore.Qt.SmoothTransformation)
        self.buttonPower = QPushButton()
        self.buttonPower.setIcon(QtGui.QIcon(scaledpixmapPower))
        self.buttonPower.setIconSize(self._image_size)
        self.buttonPower.setStyleSheet(_fromUtf8("background-color: rgb(255, 90, 90);"))
        self.buttonPower.mousePressEvent = self.powerCallback
        layout.addWidget(self.buttonPower, 0, 0)

        ############
        scaledpixmapPlus = QtGui.QPixmap(self._QLabelimagePlus).scaled(self._image_size,
                                                                       QtCore.Qt.KeepAspectRatio,
                                                                       QtCore.Qt.SmoothTransformation)
        self.buttonPlus = QPushButton()
        self.buttonPlus.setIcon(QtGui.QIcon(scaledpixmapPlus))
        self.buttonPlus.setIconSize(self._image_size)
        self.buttonPlus.setObjectName("Plus")
        self.buttonPlus.mousePressEvent = functools.partial(self._counter, name=self.buttonPlus.objectName())
        layout.addWidget(self.buttonPlus, 0, 6)

        ############
        scaledpixmapMoins = QtGui.QPixmap(self._QLabelimageMoins).scaled(self._image_size,
                                                                         QtCore.Qt.KeepAspectRatio,
                                                                         QtCore.Qt.SmoothTransformation)
        self.buttonMoins = QPushButton()
        self.buttonMoins.setIcon(QtGui.QIcon(scaledpixmapMoins))
        self.buttonMoins.setIconSize(self._image_size)
        self.buttonMoins.setObjectName("Moins")
        self.buttonMoins.mousePressEvent = functools.partial(self._counter, name=self.buttonMoins.objectName())
        layout.addWidget(self.buttonMoins, 0, 4)


        """3eme ligne"""
        scaledpixmapAnimal = QtGui.QPixmap(self._QLabelimageAnimalEnvi).scaled(self._image_size,
                                                                               QtCore.Qt.KeepAspectRatio,
                                                                               QtCore.Qt.SmoothTransformation)
        self.buttonAnimal = QPushButton()
        self.buttonAnimal.setIcon(QtGui.QIcon(scaledpixmapAnimal))
        self.buttonAnimal.setIconSize(self._image_size)
        self.buttonAnimal.setObjectName("Animal")
        self.buttonAnimal.mousePressEvent = functools.partial(self._on_click, name=self.buttonAnimal.objectName())
        layout.addWidget(self.buttonAnimal, 2, 5)

        ############
        scaledpixmapVegetation = QtGui.QPixmap(self._QLabelimageVegetationEnvi).scaled(self._image_size,
                                                                                       QtCore.Qt.KeepAspectRatio,
                                                                                       QtCore.Qt.SmoothTransformation)
        self.buttonVegetation = QPushButton()
        self.buttonVegetation.setIcon(QtGui.QIcon(scaledpixmapVegetation))
        self.buttonVegetation.setIconSize(self._image_size)
        self.buttonVegetation.setObjectName("Végétation")
        self.buttonVegetation.mousePressEvent = functools.partial(self._on_click,
                                                                  name=self.buttonVegetation.objectName())
        layout.addWidget(self.buttonVegetation, 2, 2)

        ############
        scaledpixmapEblouissementEnvi = QtGui.QPixmap(self._QLabelimageEblouissementEnvi).scaled(self._image_size,
                                                                                                 QtCore.Qt.KeepAspectRatio,
                                                                                                 QtCore.Qt.SmoothTransformation)

        self.buttonEblouissement = QPushButton()
        self.buttonEblouissement.setIcon(QtGui.QIcon(scaledpixmapEblouissementEnvi))
        self.buttonEblouissement.setIconSize(self._image_size)
        self.buttonEblouissement.setObjectName("Eblouissement")
        self.buttonEblouissement.mousePressEvent = functools.partial(self._on_click,
                                                                     name=self.buttonEblouissement.objectName())
        layout.addWidget(self.buttonEblouissement, 2, 3)

        ############
        scaledpixmapTravauxEnvi = QtGui.QPixmap(self._QLabelimageTravauxEnvi).scaled(self._image_size,
                                                                                     QtCore.Qt.KeepAspectRatio,
                                                                                     QtCore.Qt.SmoothTransformation)
        self.buttonTravaux = QPushButton()
        self.buttonTravaux.setIcon(QtGui.QIcon(scaledpixmapTravauxEnvi))
        self.buttonTravaux.setIconSize(self._image_size)
        self.buttonTravaux.setObjectName("Travaux")
        self.buttonTravaux.mousePressEvent = functools.partial(self._on_click, name=self.buttonTravaux.objectName())
        layout.addWidget(self.buttonTravaux, 2, 6)

        ############
        scaledpixmapIntemperiesEnvi = QtGui.QPixmap(self._QLabelimageIntemperiesEnvi).scaled(self._image_size,
                                                                                             QtCore.Qt.KeepAspectRatio,
                                                                                             QtCore.Qt.SmoothTransformation)
        self.buttonIntemperies = QPushButton()
        self.buttonIntemperies.setIcon(QtGui.QIcon(scaledpixmapIntemperiesEnvi))
        self.buttonIntemperies.setIconSize(self._image_size)
        self.buttonIntemperies.setObjectName("Intempéries")
        self.buttonIntemperies.mousePressEvent = functools.partial(self._on_click,
                                                                   name=self.buttonIntemperies.objectName())
        layout.addWidget(self.buttonIntemperies, 2, 1)

        ############
        scaledpixmapStationnementGenantEnvi = QtGui.QPixmap(self._QLabelimageStationnementGenantEnvi).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonStationnementGenant = QPushButton()
        self.buttonStationnementGenant.setIcon(QtGui.QIcon(scaledpixmapStationnementGenantEnvi))
        self.buttonStationnementGenant.setIconSize(self._image_size)
        self.buttonStationnementGenant.setObjectName("Stationnement")
        self.buttonStationnementGenant.mousePressEvent = functools.partial(self._on_click,
                                                                           name=self.buttonStationnementGenant.objectName())
        layout.addWidget(self.buttonStationnementGenant, 2, 4)

        """ 4eme ligne"""
        ############
        scaledpixmapExit = QtGui.QPixmap(self._QLabelimageExit).scaled(self._image_size,
                                                                       QtCore.Qt.KeepAspectRatio,
                                                                       QtCore.Qt.SmoothTransformation)
        self.buttonExit = QPushButton()
        self.buttonExit.setIcon(QtGui.QIcon(scaledpixmapExit))
        self.buttonExit.setIconSize(self._image_size)
        self.buttonExit.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        # self.buttonGere.mousePressEvent = self._on_click  # Action triggered on mouse click
        self.buttonExit.mousePressEvent = self._shutdown
        layout.addWidget(self.buttonExit, 3, 0)

        ############
        scaledpixmapTraveePPVul = QtGui.QPixmap(self._QLabelimageTraveePPVul).scaled(self._image_size,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
        self.buttonTraveePP = QPushButton()
        self.buttonTraveePP.setIcon(QtGui.QIcon(scaledpixmapTraveePPVul))
        self.buttonTraveePP.setIconSize(self._image_size)
        self.buttonTraveePP.setObjectName("Traversée_PP")
        self.buttonTraveePP.mousePressEvent = functools.partial(self._on_click, name=self.buttonTraveePP.objectName())
        layout.addWidget(self.buttonTraveePP, 3, 1)

        ############
        scaledpixmapTraveeHorsPPVul = QtGui.QPixmap(self._QLabelimageTraveeHorsPPVul).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonTraveeHorsPP = QPushButton()
        self.buttonTraveeHorsPP.setIcon(QtGui.QIcon(scaledpixmapTraveeHorsPPVul))
        self.buttonTraveeHorsPP.setIconSize(self._image_size)
        self.buttonTraveeHorsPP.setObjectName("Traversée_hors")
        self.buttonTraveeHorsPP.mousePressEvent = functools.partial(self._on_click,
                                                                    name=self.buttonTraveeHorsPP.objectName())
        layout.addWidget(self.buttonTraveeHorsPP, 3, 2)

        ############
        scaledpixmapTraverseeMasquageVul = QtGui.QPixmap(self._QLabelimageTraverseeMasquageVul).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonTraverseeMasquage = QPushButton()
        self.buttonTraverseeMasquage.setIcon(QtGui.QIcon(scaledpixmapTraverseeMasquageVul))
        self.buttonTraverseeMasquage.setIconSize(self._image_size)
        self.buttonTraverseeMasquage.setObjectName("Traversée_masque")
        self.buttonTraverseeMasquage.mousePressEvent = functools.partial(self._on_click,
                                                                         name=self.buttonTraverseeMasquage.objectName())
        layout.addWidget(self.buttonTraverseeMasquage, 3, 3)

        ############
        scaledpixmapUsagerSortantVehiculeVul = QtGui.QPixmap(self._QLabelimageUsagerSortantVehiculeVul).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonUsagerSortantVehicule = QPushButton()
        self.buttonUsagerSortantVehicule.setIcon(QtGui.QIcon(scaledpixmapUsagerSortantVehiculeVul))
        self.buttonUsagerSortantVehicule.setIconSize(self._image_size)
        self.buttonUsagerSortantVehicule.setObjectName("Usager_sortant")
        self.buttonUsagerSortantVehicule.mousePressEvent = functools.partial(self._on_click,
                                                                             name=self.buttonUsagerSortantVehicule.objectName())
        layout.addWidget(self.buttonUsagerSortantVehicule, 3, 4)

        """ 2eme ligne """

        ###########
        scaledpixmapRefusPrioMvt = QtGui.QPixmap(self._QLabelimageREfusPrioMvt).scaled(self._image_size,QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.buttonRefusPrio = QPushButton()
        self.buttonRefusPrio.setIcon(QtGui.QIcon(scaledpixmapRefusPrioMvt))
        self.buttonRefusPrio.setIconSize(self._image_size)
        self.buttonRefusPrio.setObjectName("Refus_prio")
        self.buttonRefusPrio.mousePressEvent = functools.partial(self._on_click, name=self.buttonRefusPrio.objectName())
        layout.addWidget(self.buttonRefusPrio, 1, 6)

        ############
        scaledpixmapRabattementMvt = QtGui.QPixmap(self._QLabelimageRabattementMvt).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonRabat = QPushButton()
        self.buttonRabat.setIcon(QtGui.QIcon(scaledpixmapRabattementMvt))
        self.buttonRabat.setIconSize(self._image_size)
        self.buttonRabat.setObjectName("Rabattemt_proche")
        self.buttonRabat.mousePressEvent = functools.partial(self._on_click, name=self.buttonRabat.objectName())
        layout.addWidget(self.buttonRabat, 1, 2)

        ############
        scaledpixmapSortieStatioMvt = QtGui.QPixmap(self._QLabelimageSortieStatioMvt).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonSortieStatio = QPushButton()
        self.buttonSortieStatio.setIcon(QtGui.QIcon(scaledpixmapSortieStatioMvt))
        self.buttonSortieStatio.setIconSize(self._image_size)
        self.buttonSortieStatio.setObjectName("Sortie_parking")
        self.buttonSortieStatio.mousePressEvent = functools.partial(self._on_click,
                                                                    name=self.buttonSortieStatio.objectName())
        layout.addWidget(self.buttonSortieStatio, 1, 1)

        ############
        scaledpixmapDepassementProcheMvt = QtGui.QPixmap(self._QLabelimageDepassementProcheMvt).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonDepassementProche = QPushButton()
        self.buttonDepassementProche.setIcon(QtGui.QIcon(scaledpixmapDepassementProcheMvt))
        self.buttonDepassementProche.setIconSize(self._image_size)
        self.buttonDepassementProche.setObjectName("Depassemt_proche")
        self.buttonDepassementProche.mousePressEvent = functools.partial(self._on_click,
                                                                    name=self.buttonDepassementProche.objectName())
        layout.addWidget(self.buttonDepassementProche, 1, 3)

        ############
        scaledpixmapNonRespectPrioRPMvt = QtGui.QPixmap(self._QLabelimageNonRespectPrioRPMvt).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonNonRespectPrioRP = QPushButton()
        self.buttonNonRespectPrioRP.setIcon(QtGui.QIcon(scaledpixmapNonRespectPrioRPMvt))
        self.buttonNonRespectPrioRP.setIconSize(self._image_size)
        self.buttonNonRespectPrioRP.setObjectName("Non_respect_prio")
        self.buttonNonRespectPrioRP.mousePressEvent = functools.partial(self._on_click,
                                                                        name=self.buttonNonRespectPrioRP.objectName())
        layout.addWidget(self.buttonNonRespectPrioRP, 1, 4)

        ############
        scaledpixmapTVitesseExcessiveMvt = QtGui.QPixmap(self._QLabelimageVitesseExcessiveMvt).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonVitesseExcessive = QPushButton()
        self.buttonVitesseExcessive.setIcon(QtGui.QIcon(scaledpixmapTVitesseExcessiveMvt))
        self.buttonVitesseExcessive.setIconSize(self._image_size)
        self.buttonVitesseExcessive.setObjectName("Vitesse_excessive")
        self.buttonVitesseExcessive.mousePressEvent = functools.partial(self._on_click,
                                                                        name=self.buttonVitesseExcessive.objectName())
        layout.addWidget(self.buttonVitesseExcessive, 1, 5)

        ############
        scaledpixmapRetourArr = QtGui.QPixmap(self._QLabelimageRetourArr).scaled(self._image_size,
                                                                                 QtCore.Qt.KeepAspectRatio,
                                                                                 QtCore.Qt.SmoothTransformation)
        self.buttonRetourArr = QPushButton()
        self.buttonRetourArr.setIcon(QtGui.QIcon(scaledpixmapRetourArr))
        self.buttonRetourArr.setIconSize(self._image_size)
        # self.buttonRetourArr.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.buttonRetourArr.setObjectName("taguage_supprimé")
        # self.buttonGere.mousePressEvent = self._on_click  # Action triggered on mouse click
        self.buttonRetourArr.mousePressEvent = functools.partial(self._on_click, name=self.buttonRetourArr.objectName())
        layout.addWidget(self.buttonRetourArr, 3, 6)

        ############
        scaledpixmapTZeroEvent = QtGui.QPixmap(self._QLabelimageZeroEvent).scaled(
            self._image_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.buttonZeroEvent = QPushButton()
        self.buttonZeroEvent.setIcon(QtGui.QIcon(scaledpixmapTZeroEvent))
        self.buttonZeroEvent.setIconSize(self._image_size)
        self.buttonZeroEvent.setObjectName("Zero_event")
        self.buttonZeroEvent.mousePressEvent = functools.partial(self._on_click,
                                                                        name=self.buttonZeroEvent.objectName())
        layout.addWidget(self.buttonZeroEvent, 1, 0)

        #mettre en place toute la disposition fabriquée
        self.setLayout(layout)
        self.setGeometry(50, 50, 320, 200)
        self.setWindowTitle("PyQT show image")
        self.show()
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(p)

        # ajout du widget et création de toute la fenetre
        self.setCentralWidget(self._main)
        self.move(QtCore.QPoint(screen_res.x(), screen_res.y()))
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        # rendre visible tout ça
        self.setVisible(True)
        self.layout = layout
        # Connect the methods to the different signals
        # self._server.sig_mode.connect(self._change_mode)
        self._server.sig_shutdown.connect(self._shutdown)

        # ecrit le nom des boutons dans la case 4eme ligne 6eme colonne
        # creation d'un type bouton pour inserer le texte dedans
        self.buttonInfos = QPushButton()

        # style du bouton texte, couleur jaune et en gras pour etre visible
        self.buttonInfos.setStyleSheet('QPushButton {background-color: yellow; color: black; border: none; font: bold 30px;}')
        # ajout du bouton texte dans sa case définie
        self.layout.addWidget(self.buttonInfos, 3, 5)

        # ecrit le nombre de passagers dans la case 1eme ligne 5eme colonne
        # creation d'un type bouton pour inserer le texte dedans
        self.buttonNbPassager = QPushButton()
        # style du bouton texte, couleur jaune et en gras pour etre visible
        self.buttonNbPassager.setStyleSheet('QPushButton {background-color: yellow; color: black; border: none; font: bold 100px;}')
        # ajout du bouton texte dans sa case définie
        self.layout.addWidget(self.buttonNbPassager, 0, 5)

    @QtCore.pyqtSlot()
    def _shutdown(self):
        """
        callback pour eteindre
        """
        self._zmq_client.quit()
        # self._server.quit()
        self.close()


    def _on_click(self, event, name):
        """
        callback pour tout les boutons de situations rencontrées
        """
        #recuperer l'heure pour l'inserer dans le csv
        TimeCode = d.datetime.now().time()

        #envoi des données sous forme de dictionnaire:
        data = {'TC': TimeCode, 'click': "situation", 'numNavette': self.numNavette, 'donnee': name, 'nbPassagers':self.countGlobal }# Changer le numero de navette en fonction de la navette utilisée
        self._zmq_client.send(data, name)

        """
         #ecrit le nom des boutons dans la case 4eme ligne 6eme colonne
        #creation d'un type bouton pour inserer le texte dedans
        self.buttonInfos = QPushButton()
        """

        #inserer le texte dedans, name étant le nom du bouton passé en argument de la fonction callback
        self.buttonInfos.setText(str(name))

        """
        #style du bouton texte, couleur jaune et en gras pour etre visible
        self.buttonInfos.setStyleSheet('QPushButton {background-color: yellow; color: black; border: none; font: bold 19px;}')
        #ajout du bouton texte dans sa case définie
        self.layout.addWidget(self.buttonInfos, 3 , 5)
        """

        #le rendre visible pendant 20secondes
        self.setVisible(True)



    def _counter(self, event, name):
        """
        callback pour compter le nombre de passagers, appelé par les boutons (+) et (-)
        """

        if name == "Plus" :
            self.countGlobal=self.countGlobal+1

        elif name  == "Moins":
            self.countGlobal = self.countGlobal - 1

        self.buttonNbPassager.setText(str(self.countGlobal))

        # envoi des données sous forme de dictionnaire:
        #recuperer l'heure
        TimeCode = d.datetime.now().time()
        print(name)
        data = {'TC': TimeCode, 'click': "passagers", 'numNavette': self.numNavette, 'donnee': name,
                'nbPassagers': self.countGlobal}  # Changer le numero de navette en fonction de la navette utilisée
        self._zmq_client.send(data, name)


    def powerCallback(self, event):
        """
        ce callback allume l'ecriture des données et l'application
        :param event: bouton power l'a appelé
        :return: ecrit le fichier de données dans le dossier correspondant
        """

        #compteurs à 0:
        self.countGlobal = 0

        #Passe les boutons au vert
        self.buttonPower.setStyleSheet(_fromUtf8('background-color: rgb(176, 242, 182);'))
        self.buttonMalGere.setStyleSheet(_fromUtf8('background-color: rgb(176, 242, 182);'))
        self.buttonGere.setStyleSheet(_fromUtf8('background-color: rgb(176, 242, 182);'))

        #mise au format date qui passe dans un nom de fichier
        txtDate = str(datetime.datetime.now())
        x = txtDate.replace(" ", "_")
        formatDate = x.replace(":", "_")
        formatDateFixe = str(formatDate)

        # Création d'un dossier pour stocker les données de la journée
        nomRepertoire = formatDateFixe[0:10]
        repertoire = r'C:\Users\ena\Desktop\resultatsAppliOperateur_csv\sortie_' + nomRepertoire

        # 1 repertoire par jour, le créer s'il n'existe pas encore
        if not os.path.exists(repertoire):
            os.makedirs(repertoire)

        #nom du fichier csv créé
        self.fdateName = os.path.join(repertoire, formatDateFixe + ".csv")

        #on ouvre et ecrit dans le fichier en question
        f = open(self.fdateName, 'w')#ouverture du fichier en mode écriture "w"

        # transfere des données vers le deuxieme script /clients/zmq_client
        self._zmq_client.sendFileCsvName(self.fdateName)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self._shutdown()


"""
                ######################## titres colonne gauche
        self.buttonTitreUsager = QLineEdit("Usagers vulnérables")
        layout.addWidget(self.buttonTitreUsager, 3, 0)
        self.buttonTitreVehicules = QLineEdit("Véhicules en mouvement")
        layout.addWidget(self.buttonTitreVehicules, 1, 0)
        self.buttonTitreEnvironnement = QLineEdit("Environnement")
        layout.addWidget(self.buttonTitreEnvironnement, 2, 0)
"""