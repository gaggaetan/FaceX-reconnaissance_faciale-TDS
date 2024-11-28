import cv2
import os
import time
import json

NBR_SAMPLE = 30

def get_cam() :
    ret, img = cam.read()
    return ret, img

def show_img(img):
    cv2.imshow('image', img)


def get_user_name():
    """
    Avoir le user name du sample vérifier qu'il n'est pas déja utilisé et sauver dans fichier le fichier
    """

    user_name = input('\n Enter user name : ')

    while True :
        with open('users_names.json', 'r') as file:
            users_names = json.load(file)
        
        if user_name not in users_names :

            users_names["users_names"].append(user_name)

            # ajout du nom dans le json
            with open('users_names.json', 'w') as json_file:
                json.dump(users_names, json_file)

            print("user : ", user_name)
            break
    return user_name
    

# Reconaisance faciale xml file
haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialisation de la caméra
cam = cv2.VideoCapture(0)

# Avoir user name du sample et sauver dans fichier de nom
user_name = get_user_name()

# Affichage camera
ret, img = get_cam()
show_img(img)

# Lancement des photos
print("\n Start in 3 sec :")
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)

nbr_photos = 0
prev_time = time.time()

# Récupere les Samples
while(True):

    # Récuperation image 
    ret, img = get_cam()

    if cv2.waitKey(1) & 0xff == 27 :
        break
    

    grayIMG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Détection image
    faces = haar_cascade.detectMultiScale(grayIMG, 1.26, 5)

    # Rectangle
    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)    
        nbr_photos += 1

        # Sauve l'image
        cv2.imwrite("data/user." + str(user_name) + '.' + str(nbr_photos) + ".jpg", grayIMG[y:y+h,x:x+w])

        print("Photo ", nbr_photos)

    # Calcul du FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Afficher le FPS sur l'image
    cv2.putText(img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(img, f"Image: {nbr_photos}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    show_img(img)

    if nbr_photos >= NBR_SAMPLE-1: 
         break # fin du program si l'on à tous les samples
    
    time.sleep(0.3)
 
print("\n exit program")
cam.release()
cv2.destroyAllWindows()