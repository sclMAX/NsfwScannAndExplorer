# NsfwScannAndExplorer
Escanea imagenes en Directorio o Reporte VIC 1.3 y las clasifica por score con CNN Nsfw

Descargar el siguiente Archivo dentro de la carpeta "model"
    http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_19_layers.caffemodel

# INSTALAR EN FEDORA 

## Actualizar pip
sudo pip3 install --upgrade pip 
#Configuracion para desarrollo gcc c/c++
sudo dnf install redhat-rpm-config 
# Instalar las cabeceras de desarrollo python
sudo dnf install python3-devel 
# Crear el entorno virtual
python3 -m venv NSFW_Env
cd NSFW_Env
# Clonar el repo
git clone https://github.com/sclMAX/NsfwScannAndExplorer.git
# Activar el entorno virtual
source ./bin/activate
# Instalar dependencias
cd NsfwScannAndExplorer
pip3 install --upgrade -r require.txt
