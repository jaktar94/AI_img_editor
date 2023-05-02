import datetime
import os
import pathlib
from http.server import HTTPServer, SimpleHTTPRequestHandler
from logging import info, basicConfig, DEBUG
from threading import Thread

from flask import Flask, jsonify
from flask import request as flask_request
from flask_cors import CORS

from src.backend import Backend
from src.filter_manager import FilterManager
from src.local_storage import LocalStorage
from src.queue import Queue

log_dir = os.path.join(pathlib.Path().resolve(), "logs")
pathlib.Path(log_dir).mkdir(parents=True, exist_ok=True)
log_file = os.path.join(log_dir, f"log_file-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log")
print(f"Logging to {log_file}")

basicConfig(filename=log_file, encoding='utf-8', level=DEBUG)
tmp_folder_path = os.path.join(pathlib.Path().resolve(), "tmp")
filters_folder_path = os.path.join(pathlib.Path().resolve(), "ai_filters", "Style_GAN", "images")
pathlib.Path(tmp_folder_path).mkdir(parents=True, exist_ok=True)
info(msg=f"tmp folder path: {tmp_folder_path}")
info(msg=f"filters folder path: {filters_folder_path}")

info(msg="Creating LocalStorage")
storage = LocalStorage(tmp_folder_path=tmp_folder_path, filters_folder_path=filters_folder_path)
info(msg="Creating Queue")
queue = Queue()

filter_manager = FilterManager(storage=storage, queue=queue)
filter_manager.import_filters()
filter_manager.run()
backend = Backend(storage=storage, queue=queue)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=tmp_folder_path, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)


def run_http_server(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


Thread(target=lambda: run_http_server()).start()

app = Flask(__name__)

# enable CORS
CORS(app)


@app.route('/ping')
def ping():
    return jsonify(success=True)


@app.route('/get_size', methods=["POST"])
def get_image_size():
    w, h = backend.get_image_size(flask_request_local=flask_request)
    return jsonify(w=w, h=h)


@app.route('/get_last_saved', methods=["GET"])
def get_last_saved_image():
    id = backend.get_last_saved_image()
    if id:
        return jsonify(error="NO", id=id)
    return jsonify(error="YES")


@app.route('/', methods=["POST"])
def get_image():
    path, output_image_id = backend.get_image(flask_request_local=flask_request)

    # Thread(target=lambda: backend.delete_image(image_id=output_image_id)).start()

    return jsonify(id=output_image_id)
    # return path


@app.route('/save_image', methods=["POST"])
def save_image():
    return jsonify(success=backend.save_image(flask_request_local=flask_request))


@app.route('/reset', methods=["GET"])
def reset():
    return jsonify(error="NO" if backend.reset() else "YES")


app.run(host='localhost', port=5000, threaded=True, processes=1, debug=False)
