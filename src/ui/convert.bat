python -m PyQt5.uic.pyuic main_ui/ui_main.ui -o main_ui/ui_main.py --from-imports
::python -m PyQt5.uic.pyuic scann_ui/ui_nsfw_scann.ui -o scann_ui/ui_nsfw_scann.py --from-imports
::python -m PyQt5.uic.pyuic widgets/NsfwCard.ui -o widgets/NsfwCard.py --from-imports
::python3 -m PyQt5.uic.pyuic src/ui/main_ui/ui_main.ui -o src/ui/main_ui/ui_main.py --from-imports 
::python3 -m PyQt5.uic.pyuic src/ui/scann_ui/ui_nsfw_scann.ui -o src/ui/scann_ui/ui_nsfw_scann.py --from-imports

:: RESOURCES
:: /home/max/.local/bin/pyrcc5 -o src/ui/resources_rc.py src/ui/resources.qrc