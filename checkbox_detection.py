def checkboxes_locked(imgF2):
    
    """ this function allows us to get a json file
        which gives labels and values of checkboxes
    """
    
    from PIL import Image
    import pytesseract as PT  
    import sys  
    from pdf2image import convert_from_path as CFP 
    import os 
    import cv2
    import matplotlib.pyplot as plt
    
    list_of_checkboxes = ["Autres", "Perspective d'evolution", "Ressenti entretien", "Rémunération",
     "Localisation du poste", "Taille de l'entreprise", "Suivi de carrière",
     "Projet / Poste","Reconversion prodessionnelle","Mobile", "Manager IT", "Infrastructure",
     "Gestion de projet IT","Dev. PHP/Web","Dev. Java/J2ee", "Dev. cobol", "Dev. c#.net",
     "Dev. -autres technos","CDP PHP/Web", "CDP Marketing/Digital","CDP Java/J2ee","CDP C#.net","Supply chain",
     "Sécurité. Environnement", "Qualité", "Physique Matériaux", "Méthodes Industrialisation",
     "Maint, Prod", "Gestion de projet, planification", "Génie électrique & électronique",
     "Génie chimique, es procédés", "Essais", "Conception Mécanique", "Calcul, Mécanique des fluides",
     "Bât, GC, Travaux Neufs", "Automatisme & Info Indus", "Achats"]
    
    original = imgF2.copy()
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Find contours and filter using contour area filtering to remove noise
    cnts, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    AREA_THRESHOLD = 10
    for c in cnts:
        area = cv2.contourArea(c)
        if area < AREA_THRESHOLD:
            cv2.drawContours(thresh, [c], -1, 0, -1)

    # Repair checkbox horizontal and vertical walls
    repair_kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3,1))
    repair = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, repair_kernel1, iterations=1)
    repair_kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3))
    repair = cv2.morphologyEx(repair, cv2.MORPH_CLOSE, repair_kernel2, iterations=1)

    # Detect checkboxes using shape approximation and aspect ratio filtering
    checkbox_contours = []
    cnts, _ = cv2.findContours(repair, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    list_of_values = []
    for idx, c in enumerate(cnts):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.052 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if len(approx) == 4 and (aspect_ratio >= 0.82 and aspect_ratio <= 1.8) and (cv2.countNonZero(thresh[y:y+h,x:x+w]) > 28) and (thresh[y:y+h,x:x+w].shape == (13, 12) or thresh[y:y+h,x:x+w].shape == (12, 12)):
            cv2.rectangle(original, (x, y), (x + w, y + h), (36,255,12), 3)
            if cv2.countNonZero(thresh[y:y+h,x:x+w]) > 100:
                list_of_values.append(1)
            else:
                list_of_values.append(0)
            checkbox_contours.append(c)
    result = {str(k):v for k,v in zip(list_of_checkboxes, list_of_values)}
    return result
