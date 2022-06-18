import pickle
import cv2

def predict(img):
    
    model = pickle.load(open('model.pkl','rb'))
    CATEGORIES = ['bad', 'god']
    
    def prepare(filepath):
        IMG_SIZE = 50
        img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    
    prepared_img = prepare(img)
    
    predict = model.predict([prepared_img])
    prediction = CATEGORIES[int(predict[0][0])]
    
    return prediction    
