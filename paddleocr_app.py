import os
import random
from datetime import datetime
import flask
import io
from PIL import Image
from flask import Flask
from paddleocr import PaddleOCR

app = Flask(__name__)


@app.route("/ocr_predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the view
    data = {"success": False}
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        image = flask.request.files.get("image")
        if image:
            # 生成随机数
            random_num = random.randint(0, 100)
            filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(random_num) + "_" + image.filename
            save_path = os.getcwd() + "/" + "uploads/" + filename
            ocr = PaddleOCR(use_angle_cls=True, lang="ch")
            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            image.save(save_path)
            lines = ocr.ocr(save_path, cls=True)
            result = [line[-1] for line in lines]
            print(result)
            data["result"] = result
            # indicate that the request was a success
            data["success"] = True
    # return the data dictionary as a JSON response
    return flask.jsonify(data)


if __name__ == "__main__":
    # 0.0.0.0表示你监听本机的所有IP地址上,通过任何一个IP地址都可以访问到.
    # port为端口号
    # debug=Fasle表示不开启调试模式
    app.run(host='0.0.0.0', port=8000, debug=False)