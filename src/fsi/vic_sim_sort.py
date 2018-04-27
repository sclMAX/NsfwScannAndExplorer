from keras.models import Model
from src.fsi.vgg19 import VGG19
from src.fsi.kNN import kNN
from src.utils.sort_utils import find_topk_unique

class ImageCNN(object):
    def __init__(self, img_file: str, target_size: tuple):
        self.__file_path: str = img_file
        self.__cnn_img = None
        self.width, self.height = target_size
        self.__processImg()
        self.features = None

    def __processImg(self):
        import numpy as np
        from keras.preprocessing import image
        from src.utils.imagenet_utils import preprocess_input
        # Read image file
        __img = image.load_img(self.__file_path, target_size=(
            self.width, self.height))  # load
        # Pre-process for model input
        __img = image.img_to_array(__img)  # convert to array
        __img = np.expand_dims(__img, axis=0)
        self.__cnn_img = preprocess_input(__img)

    def getFilePath(self):
        return self.__file_path

    def getData(self):
        return self.__cnn_img

class VICMediaSimSort(object):

    def __init__(self):
        self.query_img: ImageCNN = None
        self.VICMedia: list = None
        self.__img_list: list = []
        self.__model: Model = None

    def __loadModel(self):
        base_model = VGG19(weights='imagenet')
        self.__model = Model(inputs=base_model.input, outputs=base_model.get_layer('block4_pool').output)

    def __loadAllImages(self):
        if not self.model:
            self.__loadModel()
        for item in self.VICMedia:
            try:
                img_file = str(item['RelativeFilePath']).replace('\\', '/')
                img = ImageCNN(img_file, (224, 224))
                img.features = self.__model.predict(img.getData()).flatten()
                self.__img_list.append(img)
            except ValueError:
                continue

    def emitStatus(self):
        pass

    def sortData(self, query_img: ImageCNN, media: list):
        self.query_img = query_img
        self.__img_list.clear()
        self.__img_list.append(self.query_img)
        self.VICMedia = media
        self.__loadAllImages()


''' X.append(features)  # append feature extractor

    X = np.array(X)  # feature vectors
    imgs = np.array(imgs)  # images
    print("imgs.shape = {}".format(imgs.shape))
    print("X_features.shape = {}\n".format(X.shape))

    # ===========================
    # Find k-nearest images to each image
    # ===========================
    n_neighbours = 10  # +1 as itself is most similar
    knn = kNN()  # kNN model
    knn.compile(n_neighbors=n_neighbours, algorithm="brute", metric="cosine")
    knn.fit(X)

    # ==================================================
    # Plot recommendations for each image in database
    # ==================================================
    output_rec_dir = os.path.join("output", "rec")
    if not os.path.exists(output_rec_dir):
        os.makedirs(output_rec_dir)
    n_imgs = len(imgs)
    ypixels, xpixels = imgs[0].shape[0], imgs[0].shape[1]
   # for ind_query in range(n_imgs):
    ind_query = 0
    # Find top-k closest image feature vectors to each vector
    print("[{}/{}] Plotting similar image recommendations for: {}".format(ind_query+1, n_imgs, filename_heads[ind_query]))
    distances, indices = knn.predict(np.array([X[ind_query]]))
    distances = distances.flatten()
    indices = indices.flatten()
    indices, distances = find_topk_unique(indices, distances, n_neighbours) '''