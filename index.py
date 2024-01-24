from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pyautogui
import threading

class GUIController:
    def __init__(self, data):
        self.data = data

    def processRequest(self):
        global connected
        connected = self.data['action']
        if connected == "close":
            return None
        
        print(self.data['action'])

        # if self.data['action'] == "onmousemove":
        #     self.onmousemove(self.data['data'])
        # elif self.data['action'] == "onmousedown":
        #     self.onmousedown(self.data['data'])
        # elif self.data['action'] == "onmouseup":
        #     self.onmouseup(self.data['data'])
        # elif self.data['action'] == "onmousewheel":
        #     self.onmousewheel(self.data['data'])
        # elif self.data['action'] == "keydown":
        #     self.keydown(self.data['data'])
        # elif self.data['action'] == "keyup":
        #     self.keyup(self.data['data'])

    def onmousemove(self, data):
        print(data)
        # pyautogui.moveTo(data['offsetX'], data['offsetY'])

    def onmousedown(self, data):
        print(data)
        pyautogui.mouseDown()

    def onmouseup(self, data):
        pyautogui.mouseUp()

    def onmousewheel(self, data):
        print(data)

    def keydown(self, data):
        print(data)

    def keyup(self, data):
        print(data)

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        guiController = GUIController(data)
        threading.Thread(target=guiController.processRequest).start()
        self.wfile.write(json.dumps({'message': 'Success'}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=4321):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    run()
