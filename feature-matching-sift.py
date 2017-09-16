import numpy as np
import cv2
#from matplotlib import pyplot as plt
import argparse
import datetime
import json
import urllib
import boto3

sns = boto3.client('sns')
match_result_arn =  'arn:aws:sns:eu-west-2:458847123929:match-result' #[t["TopicArn"] for t in sns.list_topics()['Topics'] if t["TopicArn"].endswith(':' + 'match-result')][0] 


def feature_matching(ref, img):
    start = datetime.datetime.now()

    print "ref: " + ref
    print "img: " + img
    resp_ref = urllib.urlopen(ref)
    img1 = np.asarray(bytearray(resp_ref.read()), dtype="uint8")
    img1 = cv2.imdecode(img1, cv2.IMREAD_COLOR)
    print img1.shape

    resp_img = urllib.urlopen(img)
    img2 = np.asarray(bytearray(resp_img.read()), dtype="uint8")
    img2 = cv2.imdecode(img2, cv2.IMREAD_COLOR)
    print img2.shape

    # img1 = cv2.imread(ref,0)          # queryImage
    # img2 = cv2.imread(img,0)          # queryImage

    # Initiate SIFT detector
    #sift = cv2.SIFT()
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
    message = json.loads(event['Records'][0]['Sns']['Message'])
    print message
    cid = message.get("cid", "")
    ref_url = "https://s3.eu-west-2.amazonaws.com/th-" + str(cid) + "/ref.jpg"
    settings_url = "https://s3.eu-west-2.amazonaws.com/th-" + str(cid) + "/settings.json" # to put some settings like the threshold for the number of matching points
    print "ref_url = " + ref_url
    img_url = message.get("image_url", "")
    matches, elaps = feature_matching(ref_url, img_url)

    res = {
        "match_result": {
            "version": "OpenCV " + cv2.__version__,
            "matches": matches,
            "time": elaps,
            "status": "match" if matches > 100 else "nomatch"
        },
        "participation_message": message
    }

    sns.publish(
        TopicArn=match_result_arn,
        Message=json.dumps(res),
        Subject='Feature matching result',
        MessageStructure="raw"
    )

    print "Returning : " + str(res)
    return res

# def lambda_handler(event, context):
#     matches, elaps = feature_matching(event["ref"], event["img"])
#     res = { 
#         "version": "OpenCV " + cv2.__version__,
#         "message": event["ref"] + " and " + event["img"] + " are matching!",
#         "matches": matches,
#         "time": elaps,
#         "status": "match"
#     }
#     return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sift sample')
    parser.add_argument('-r','--ref', help='reference image', required=True)
    parser.add_argument('-i','--img', help='imput image', required=True)
    args = vars(parser.parse_args())
    print lambda_handler(event={"ref": args["ref"], "img": args["img"]}, context=0)
