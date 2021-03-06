import numpy as np
import cv2
#from matplotlib import pyplot as plt
import argparse
import datetime
import json
import urllib


def feature_matching(ref, img, local=False):
    start = datetime.datetime.now()
    print "ref: " + ref
    print "img: " + img

    if ref.startswith('http'):
        print "ref is a url"
        resp_ref = urllib.urlopen(ref)
        img1 = np.asarray(bytearray(resp_ref.read()), dtype="uint8")
        img1 = cv2.imdecode(img1, cv2.IMREAD_COLOR)
    else:
        img1 = cv2.imread(ref,0)          # queryImage
    print img1.shape


    if img.startswith('http'):
        print "img is a url"
        resp_img = urllib.urlopen(img)
        img2 = np.asarray(bytearray(resp_img.read()), dtype="uint8")
        img2 = cv2.imdecode(img2, cv2.IMREAD_COLOR)
    else:
        img2 = cv2.imread(img,0)          # queryImage
    print img2.shape

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        # print "dist: " + str(m.distance) + " < 0.75*" + str(n.distance) + " => " + str(m.distance < 0.75*n.distance)
        if m.distance < 0.75*n.distance:
            good.append([m])
    stop = datetime.datetime.now()
    delta = stop - start
    res = '' + str(int(delta.total_seconds() * 1000)) + ' ms, ' +  str(len(good)) + " matchs"
    return len(good),  int(delta.total_seconds() * 1000)


def lambda_handler(event, context):
    try:
        body = event.get("body", "")
        if body:
            #print 'Received message body:' + str(body)
            body = json.loads(body)
        else :
            return {"errorMessage": "body not found in event", "statusCode": 400}
        
        threshold = body.get("thr", 150)
        if isinstance(threshold, str) or isinstance(threshold, unicode):
            threshold = int(threshold)

        matches, elaps = feature_matching(body["ref"], body["img"])

        res = { 
            "version": "OpenCV " + cv2.__version__,
            "message": "Made a sift matching with ref " + body["ref"] + " and image " + body["img"],
            "matches": matches,
            "elaps": elaps,
            "status": "match" if matches > threshold else "nomatch",
            "threshold": threshold
        }
        print "Returning : " + str(res)
        response = {
            'body': json.dumps(res),
            'statusCode': 200
        }
    except Exception as e:
        res = { 
            "version": "OpenCV " + cv2.__version__,
            "message": str(e),
            "matches": "nomatches",
            "elaps": elaps,
            "status": "error",
            "threshold": threshold
        }
        print "Returning : " + str(res)
        response = {
            'body': json.dumps(res),
            'statusCode': 200 # for now fo the client api
        }

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sift sample')
    parser.add_argument('-r','--ref', help='reference image', required=True)
    parser.add_argument('-i','--img', help='imput image', required=True)
    parser.add_argument('-t','--thr', help='matches threshold', required=False)
    args = vars(parser.parse_args())
    print lambda_handler(event={"body": {"ref": args["ref"], "img": args["img"], "thr": args["thr"]}}, context=0)
