# ENA - Application Opérateur



<img src=".\Image\Ena-logo-devNoMarge-rvb.jpg" alt="Ena-logo-devNoMarge-rvb" style="zoom:50%;" />



## 1. Description

Cette application sert à tagguer des événements de roulage et à compter des passagers. Les événements taggués peuvent concerner des situations de roulage avec des usagers vulnérables, des usagers en mouvement et des situations liées à l'environnement. 

Les tags créés sont enregistrés dans un fichier csv dans un dossier avec le nom de la journée

<img src=".\Image\Application_Main.png" style="zoom:50%;" />



Cette application reprend une application [CADisp](https://github.com/uge-lescot/CADisp) développée par Bertrand Richard, [@brifsttar](https://github.com/brifsttar) et Romain Derollepot, [@rderollepot](https://github.com/rderollepot)



## 2. Pré-requis / Logiciel utilisé pour développer l'application

Pour pouvoir utiliser cette application, vous aurez besoin de :

- **Python 3.9** (https://www.python.org/downloads/) ou encore mieux, préférez l'utilisation de **Anaconda** (https://docs.anaconda.com/anaconda/install/windows/)
- **PyCharm** (https://www.jetbrains.com/fr-fr/pycharm/download/#section=windows) ou **Spyder** (déjà installé si vous utilisez Anaconda)
- **Git** (https://git-scm.com/downloads) en option
- **TortoiseGit** (https://tortoisegit.org/) en option



L'application ne fonctionnera que si le dossier ``C:\Users\ena\Desktop\resultatsAppliOperateur_csv\`` existe sur votre environnement Windows. Opération à réaliser :

- Créer un utilisateur ena dans les utilisateurs Windows. Il faudra ensuite créer le dossier ``\resultatsAppliOperateur_csv`` sur le Bureau
- Créer dans le lecteur ``C:\`` le dossier ``C:\Users\ena\Desktop\resultatsAppliOperateur_csv\``. Attention, il faudra ouvrir les droits de modification / contrôle total sur ce dossier afin que l'application puisse écrire à l'intérieur (par défaut, Windows ne l'autorise pas)



## 3. Comment l'installer ?

- Installer ``Python`` ou ``Anaconda``
- Installer les packages à l'aide du fichier ``requirements.txt`` 
  - si vous avez installé ``python``, vous devrez créer un ``venv`` (https://docs.python.org/fr/3/library/venv.html)
  - si vous avez installé ``anaconda`` :
    - par défaut, vous n'aurez pas besoin d'installer les packages. Cette librairie utilise en général les packages fournis de base avec Anaconda
    - si besoin, vous pouvez ajouter les packages à l'aide du fichier ``requirements.txt``  : 
      - 1. Ouvrir une ligne de commande dans ce dossier
      - 2. Exécuter la commande : ``conda install --file requirements.txt``
- Installer ``git`` sur la machine
- Cloner le répertoire : https://github.com/uge-lescot/ENA-Application-Operateur.git.
- Créer le dossier ``C:\Users\ena\Desktop\resultatsAppliOperateur_csv\`` en se reportant à la procédure ci-dessus



## 4. Comment l'utiliser ?

- Lancer le fichier : ``\CADisp\batch\launch.bat``
- Vous arrivez normalement sur cet écran :

<img src=".\Image\Application_Main.png" style="zoom:50%;" />

- Appuyer sur le bouton ``Démarrage`` 
- Lorsque vous avez fini, cliquer sur le bouton ``Exit``
- Pour récupérer les données, aller dans le dossier : ``C:\Users\ena\Desktop\resultatsAppliOperateur_csv\``



## 5. Comment faire des évolutions ?

*(A COMPLETER)*



## 6. Contributeurs

Personnes ayant travaillés sur cette application :

- Noëlle FAVIER, [@NoelleUGE](https://github.com/NoelleUGE)
- Anaïs HOARAU, [@Anais-Hoarau](https://github.com/Anais-Hoarau)
- Romain DEROLLEPOT, [@rderollepot](https://github.com/rderollepot)
- Fabien MOREAU, [@fmoreau69](https://github.com/fmoreau69)
- Cao Tri DO, [@malganis35](https://github.com/malganis35)
- Bertrand Richard,  [@brifsttar](https://github.com/brifsttar) 



Origine des icônes : https://www.flaticon.com/

## 7. Licence

*(A COMPLETER)*