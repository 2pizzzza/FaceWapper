from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import concurrent.futures
import cv2
import numpy as np
import requests
import os
import insightface
from insightface.app import FaceAnalysis

app = Flask(__name__)
CORS(app)

os.makedirs("image", exist_ok=True)
os.makedirs("sample_faces", exist_ok=True)

FACE_PATH = "sample_faces/Prof.Grimm-1.jpg"
if not os.path.exists(FACE_PATH):
    raise FileNotFoundError("sample_faces/face.jpg missing")

print("Loading models...")
app_insight = FaceAnalysis(name="buffalo_l")
app_insight.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model("inswapper_128.onnx", download=False)
print("Models ready")


def read_image_from_url(url):
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return None
        img_arr = np.frombuffer(resp.content, np.uint8)
        return cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def swap_face_task(face_src, url, idx):
    img_target = read_image_from_url(url)
    if img_target is None:
        return None

    src_faces = app_insight.get(face_src)
    target_faces = app_insight.get(img_target)

    if not src_faces or not target_faces:
        print(f"No face in {url}")
        return None

    result = img_target.copy()
    result = swapper.get(result, target_faces[0], src_faces[0], paste_back=True)
    output_path = f"image/swapped_{idx}.jpg"
    cv2.imwrite(output_path, result)
    return f"http://127.0.0.1:5000/{output_path}"


@app.route("/swap-images", methods=["POST"])
def swap_images():
    data = request.get_json()
    urls = data.get("urls", [])
    urls = urls[:30]

    print(f"Received {len(urls)} URLs")

    img_src = cv2.imread(FACE_PATH)

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(swap_face_task, img_src, url, i) for i, url in enumerate(urls)]
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            if res:
                results.append(res)

    print(f"Done ({len(results)} swapped)")
    return jsonify({"new_urls": results})


@app.route("/image/<path:filename>")
def serve_image(filename):
    return send_from_directory("image", filename)


if __name__ == "__main__":
    app.run(port=5000)
