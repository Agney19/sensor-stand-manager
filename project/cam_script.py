import cv2

capture = cv2.VideoCapture(2)

while 1:
    _, f = capture.read()
    cv2.imshow('e2', f)
    if cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()
