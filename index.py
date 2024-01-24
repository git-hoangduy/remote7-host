from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pyautogui
import threading

# connected_lock = threading.Lock()
# connected = "close"

class GUIController:
    def __init__(self, data):
        self.data = data

    def processRequest(self):
        # global connected
        # with connected_lock:
        #     if self.data['action'] in ['open', 'close']:
        #         connected = self.data['action']
        #     if connected == "close":
        #         return None
        
        print(self.data['action'])

        if self.data['action'] == "onmousemove":
            self.onmousemove(self.data['data'])
        elif self.data['action'] == "onmousedown":
            self.onmousedown(self.data['data'])
        elif self.data['action'] == "onmouseup":
            self.onmouseup(self.data['data'])
        elif self.data['action'] == "contextmenu":
            self.contextmenu(self.data['data'])
        elif self.data['action'] == "onmousewheel":
            self.onmousewheel(self.data['data'])
        elif self.data['action'] == "keydown":
            self.keydown(self.data['data'])
        elif self.data['action'] == "keyup":
            self.keyup(self.data['data'])

    def onmousemove(self, data):
        pyautogui.moveTo(data['offsetX'], data['offsetY'])

    def onmousedown(self, data):
        pyautogui.mouseDown(x=data['offsetX'], y=data['offsetY'])

    def onmouseup(self, data):
        pyautogui.mouseUp(x=data['offsetX'], y=data['offsetY'])

    def contextmenu(self, data):
        pyautogui.click(button='right', x=data['offsetX'], y=data['offsetY'])

    def onmousewheel(self, data):
        pyautogui.scroll(data['deltaY'], x=data['offsetX'], y=data['offsetY'])

    def keydown(self, data):
        keys = data['keyName'].lower().split('+')
        for key in keys:
            pyautogui.keyDown(key)

    def keyup(self, data):
        keys = data['keyName'].lower().split('+')
        for key in keys:
            pyautogui.keyUp(key)

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
