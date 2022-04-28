from audioop import avg
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


PATH_FOLDER = "./data/"


# Canny edge detection
def CannyProcess(filename):
    # filename = "source.jpg"
    src = cv.imread(PATH_FOLDER + filename)
    # cv.namedWindow("input", cv.WINDOW_NORMAL)
    # cv.imshow("input", src)

    edge = cv.Canny(src, 100, 300)
    # cv.namedWindow("edge", cv.WINDOW_NORMAL)
    # cv.imshow("edge", edge)
    cv.imwrite(PATH_FOLDER + "Edge-" + filename, edge)
    edge_src = cv.bitwise_and(src, src, mask=edge)
    result = edge_src
    # cv.namedWindow("result", cv.WINDOW_NORMAL)
    # cv.imshow("result", result)
    cv.imwrite(PATH_FOLDER + "EdgeResult-" + filename, result)
    return {'msg': '666', 'src': PATH_FOLDER + "EdgeResult-" + filename}


# Harris corner detection
def HarrisProcess(filename):
    # input
    # filename = "source.jpg"
    image = cv.imread(PATH_FOLDER + filename)
    # Detector parameters
    blockSize = 2
    apertureSize = 3
    k = 0.04
    # Detecting corners
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    dst = cv.cornerHarris(gray, blockSize, apertureSize, k)
    # Normalizing
    dst_norm = np.empty(dst.shape, dtype=np.float32)
    cv.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)

    # Drawing a circle around corners
    for i in range(dst_norm.shape[0]):
        for j in range(dst_norm.shape[1]):
            if int(dst_norm[i, j]) > 120:
                cv.circle(image, (j, i), 7, (0, 255, 0), 2)
    # output
    cv.imwrite(PATH_FOLDER + 'HarrisProcessResult-' + filename, image)
    return {'msg': '666', 'src': PATH_FOLDER + 'HarrisProcessResult-' + filename}


# Shi-Tomasi corner detection
def SubPixProcess(filename):
    # input
    # filename = "source.jpg"
    image = cv.imread(PATH_FOLDER + filename)
    # Detecting corners
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray, 100, 0.05, 10)
    # print(len(corners))
    for pt in corners:
        # print(pt)
        # b = np.random.random_integers(0, 256)
        # g = np.random.random_integers(0, 256)
        # r = np.random.random_integers(0, 256)
        x = np.int32(pt[0][0])
        y = np.int32(pt[0][1])
        cv.circle(image, (x, y), 7, (0, 254, 0), 2)

    # detect sub-pixel
    winSize = (3, 3)
    zeroZone = (-1, -1)

    # Stop condition
    criteria = (cv.TERM_CRITERIA_EPS + cv.TermCriteria_COUNT, 40, 0.001)
    # Calculate the refined corner locations
    corners = cv.cornerSubPix(gray, corners, winSize, zeroZone, criteria)

    # output
    cv.imwrite(PATH_FOLDER + 'SubPixProcessResult-' + filename, image)
    return {'msg': '666', 'src': PATH_FOLDER + 'SubPixProcessResult-' + filename}

    """
    # For video:
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv.imwrite("input.png", frame)
        cv.imshow('input', frame)
        result = harris(frame)
        cv.imshow('result', result)
        k = cv.waitKey(5)&0xff
        if k == 27:
            break
    cap.release()
    cv.destroyAllWindows()
    """


# face detection
def FaceDetect(filename):

    # input
    # filename = "source.jpg"
    image = cv.imread(PATH_FOLDER + filename)
    h = image.shape[0]
    w = image.shape[1]

    # model input
    model_bin = "./face_detector/opencv_face_detector_uint8.pb"
    config_text = "./face_detector/opencv_face_detector.pbtxt"

    # load tensorflow model
    net = cv.dnn.readNetFromTensorflow(model_bin, config=config_text)

    # 人脸检测
    blobImage = cv.dnn.blobFromImage(
        image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)
    net.setInput(blobImage)
    Out = net.forward()

    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(image, label, (0, 20),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 绘制检测矩形
    for detection in Out[0, 0, :, :]:
        score = float(detection[2])
        objIndex = int(detection[1])
        if score > 0.5:
            left = detection[3]*w
            top = detection[4]*h
            right = detection[5]*w
            bottom = detection[6]*h

            # 绘制
            cv.rectangle(image, (int(left), int(top)), (int(
                right), int(bottom)), (255, 0, 0), thickness=3)
            cv.putText(image, "score:%.2f" % score, (int(left), int(
                top)-1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # output
    cv.imwrite(PATH_FOLDER + 'FaceDetectResult-' + filename, image)
    return {'msg': '666', 'src': PATH_FOLDER + 'FaceDetectResult-' + filename}

# image-similarity
# 图像相似度


# aHash similarity
def aHashSimilarity(img):
    img = cv.resize(img, (8, 8))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Calculate the average pixel value of the image
    s = 0
    hash_str = ''
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    avg = s / 64
    # pixel value > average pixel value is 1, otherwise is 0
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# dHash similarity
def dHashSimilarity(img):
    img = cv.resize(img, (9, 8))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    hash_str = ''
    # Each row is calculated as the difference between the current pixel and the next pixel
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# pHash similarity
def pHashSimilarity(img):
    img = cv.resize(img, (32, 32))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    dct = cv.dct(np.float32(gray))
    # dct_roi operation
    dct_roi = dct[0:8, 0:8]
    hash = []
    avg = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avg:
                hash.append('1')
            else:
                hash.append('0')
    return hash


# Compare the hash values
def compareHash(hash1, hash2):
    n = 0
    if len(hash1) != len(hash2):
        return -1
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n


def ImageSimilarity(filename, filename2):
    # input
    # filename = "source.jpg"
    # filename2 = "target.jpg"
    image1 = cv.imread(PATH_FOLDER + filename)
    image2 = cv.imread(PATH_FOLDER + filename2)

    # Three hash methods which is more similar to the image should be lower
    # aHash
    hash1 = aHashSimilarity(image1)
    hash2 = aHashSimilarity(image2)
    aHashValue = compareHash(hash1, hash2)
    # dHash
    hash1 = dHashSimilarity(image1)
    hash2 = dHashSimilarity(image2)
    dHashValue = compareHash(hash1, hash2)
    # pHash
    hash1 = pHashSimilarity(image1)
    hash2 = pHashSimilarity(image2)
    pHashValue = compareHash(hash1, hash2)

    # Value to percentage
    aHashValue = 1 - aHashValue / 64
    dHashValue = 1 - dHashValue / 64
    pHashValue = 1 - pHashValue / 64

    # output
    print('aHash: {:.2%}'.format(aHashValue))
    print('dHash: {:.2%}'.format(dHashValue))
    print('pHash: {:.2%}'.format(pHashValue))

    # average values
    result = (aHashValue + dHashValue + pHashValue) / 3
    # Softmax function
    result = result * result
    print('average: {:.2%}'.format(result))
    return {'msg': '666', 'result': result, 'src': PATH_FOLDER + filename2}

    # cv.imwrite(PATH_FOLDER + 'ImageSimilarityResult-' + filename, image1)


# CannyProcess()
# HarrisProcess()
# SubPixProcess()
# FaceDetect()
# ImageSimilarity()
