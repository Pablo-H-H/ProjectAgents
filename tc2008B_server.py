# TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
# Python server to interact with Unity via POST
# Sergio Ruiz-Loza, Ph.D. March 2021

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from MultiAgentes.main import dict

class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        position = {
            "Grids" : [1],
            "Index" : [0,0,0,    1,1,1,  2,2,2, 3,3,3,  4,4,4,  5,5,5,  0,2,0, 0, 0, 0],
            "Size" : [3,    3,  3,  3,  3,  3,2, 1, 1, 1],
            "ID": [-3,-3,-3,-3,-3, -3, 2, 6, 5, 5]
        }
        #position = {'Grids': [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 4, 1, 4, 0, 0, 1, 0, 0, 1, 6, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 4, 0, 4, 1, 0, 0, 0, 1, 0, 0, 0, 4, 1, 0, 6, 0, 0, 0, 0, 0, 4, 1, 4, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 4, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 1, 4, 0, 4, 1, 0, 0, 0, 1, 6, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 6, 0, 0, 0, 1, 0, 0, 0, 1, 4, 0, 4, 1, 0, 0, 0, 1, 4, 0, 4, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 2, 4, 0, 0, 0, 0, 3, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 5, 0, 0, 0, 0, 2, 2, 4, 0, 0, 3, 0, 0, 2, 0, 0], 'Index': [6, 8, 4, 6, 8, 5, 0, 5, 0, 5, 0, 5, 1, 5, 1, 6, 1, 6, 1, 7, 1, 4, 5, 4, 5, 0, 2, 0, 2, 0, 2, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 3, 2, 1, 3, 2, 3, 1, 1, 2, 7, 3, 7, 3, 7, 3, 6, 3, 6, 3, 1, 5, 6, 3, 6, 3, 5, 3, 7, 4, 7, 4, 7, 4, 7, 1, 2, 5, 1, 5, 4, 0, 0, 1, 3, 2, 0, 2, 3, 1, 2, 2, 2, 3, 3, 3, 2, 3, 3, 4, 0, 3, 4, 3, 2, 5, 1, 5, 7, 4, 0, 2, 7, 3, 2, 2, 7, 4, 1, 2, 6, 4, 3, 2, 7, 5, 7, 4, 3, 2, 3, 4, 3, 4, 0, 2, 5, 2, 5, 2, 1, 5, 0, 5, 0, 5, 1, 4, 3, 0, 6, 5, 1, 5, 0, 5, 0, 5, 1, 4, 4, 4, 3, 5, 4, 5, 2, 2, 4, 5, 3, 3, 5, 5, 1, 3, 5, 2, 0, 2, 5, 1, 2, 2, 2, 2, 1, 3, 1, 2, 3, 3, 5, 3, 5, 2, 3, 2, 6, 2, 1, 2, 4, 4, 0, 2, 4, 3, 2, 2, 2, 5, 4, 5, 2, 3, 6, 5, 4, 4, 0, 3, 4, 3, 2, 3, 1, 5, 6, 5, 3, 3, 7, 5, 1, 3, 1, 4, 0, 4, 0, 4, 6, 0, 1, 3, 6, 3, 6, 3, 6, 4, 0, 2, 6, 3, 2, 2, 5, 4, 1, 2, 4, 4, 3, 2, 6, 5, 2, 2, 6, 4, 3, 3, 7, 4, 1, 3, 1, 4, 0, 4, 0, 4, 1, 3, 3, 2, 0, 3, 3, 1, 2, 3, 0, 2, 3, 5, 2, 2, 5, 2, 3, 3, 6, 2, 1, 3, 3, 1, 2, 4, 3, 5, 2, 3, 4, 4, 3, 3, 5, 4, 1, 3], 'Size': [3, 2, 4, 4, 4, 4, 2, 2, 4, 4, 4, 4, 2, 2, 2, 4, 4, 4, 4, 4, 2, 4, 2, 2, 2, 2, 4, 2, 2, 4, 4, 2, 4, 4, 2, 4, 4, 4, 4, 4, 2, 4, 2, 2, 2, 2, 2, 4, 4, 2, 2, 4, 4, 2, 2, 4, 4, 4, 4, 4, 4, 4, 2, 4, 4, 4, 4, 2, 4, 2, 4, 4, 2, 4, 4, 4, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 4, 4, 4, 2, 2, 4, 4, 4], 'ID': [-1, -2, 2, 2, 2, 2, 0, 1, 2, 2, 2, 2, 1, 1, 1, 4, 4, 2, 2, 4, 6, 2, 0, 1, 7, 8, 2, 0, 3, 4, 4, 1, 4, 4, 1, 2, 4, 4, 4, 4, 1, 4, 0, 1, 0, 0, 1, 2, 2, 0, 0, 2, 2, 1, 1, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4, 1, 4, 1, 4, 4, 1, 4, 4, 2, 7, 8, 3, 0, 1, 4, 4, 4, 4, 4, 4, 4, 2, 2, 4, 4, 1, 4, 4, 4, 1, 1, 4, 4, 4]}
        
        datos = dict
        # print(datos)

        self._set_response()
        #self.wfile.write(str(datos).encode('utf-8'))
        self.wfile.write(json.dumps(position).encode('utf-8'))
        #self.wfile.write("{}".format(datos)).encode('utf-8')



def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()


