# TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
# Python server to interact with Unity via POST
# Sergio Ruiz-Loza, Ph.D. March 2021

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

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
            "x" : 1,
            "y" : 2,
            "z" : 3
        }


        """paredes = [[[[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 4], [1, 4, 0, 1], [1, 1, 0, 0], [6, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0]],
                   [[0, 0, 0, 1], [1, 1, 1, 1], [0, 1, 1, 0], [0, 0, 1, 1], [0, 1, 1, 4], [0, 4, 1, 1], [0, 0, 1, 0], [0, 1, 4, 0]],
                   [[1, 6, 0, 0], [0, 1, 0, 4], [1, 4, 0, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 1], [4, 1, 0, 0]],
                   [[0, 0, 1, 1], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 4, 0], [0, 0, 1, 0], [0, 1, 1, 4], [0, 4, 1, 1], [0, 1, 1, 6]],
                   [[1, 0, 0, 1], [1, 0, 0, 0], [1, 0, 0, 0], [4, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 1], [2, 2, 1, 1], [1, 1, 0, 1]],
                   [[0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 6, 0], [0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 1, 1, 0], [0, 1, 1, 1]]],
                   [[0, 0, 2, 0, 0, 3, 0, 0],
                    [0, 2, 2, 4, 0, 1, 0, 0],
                    [3, 2, 2, 2, 2, 0, 0, 1],
                    [0, 0, 2, 2, 0, 0, 0, 0],
                    [5, 0, 0, 0, 2, 2, 2, 4],
                    [1, 0, 3, 0, 0, 2, 2, 0]]]"""
        
        combine_grids = [1, 0, 0, 1,   1, 0, 0, 0,    1, 1, 0, 4,   1, 4, 0, 1,    1, 1, 0, 0,    6, 0, 0, 1,     1, 0, 0, 0,     1, 1, 0, 0,
                        0, 0, 0, 1,   1, 1, 1, 1,    0, 1, 1, 0,   0, 0, 1, 1,    0, 1, 1, 4,    0, 4, 1, 1,     0, 0, 1, 0,     0, 1, 4, 0,
                        1, 6, 0, 0,   0, 1, 0, 4,    1, 4, 0, 1,   1, 0, 0, 0,    1, 0, 0, 0,    1, 1, 0, 0,     1, 0, 0, 1,     4, 1, 0, 0,
                        0, 0, 1, 1,   0, 1, 1, 0,    0, 0, 1, 1,   0, 0, 4, 0,    0, 0, 1, 0,    0, 1, 1, 4,     0, 4, 1, 1,     0, 1, 1, 6,
                        1, 0, 0, 1,   1, 0, 0, 0,    1, 0, 0, 0,   4, 0, 0, 0,    1, 1, 0, 0,    1, 0, 0, 1,     2, 2, 1, 1,     1, 1, 0, 1,
                        0, 0, 1, 1,   0, 0, 1, 0,    0, 0, 6, 0,   0, 0, 1, 0,    0, 1, 1, 0,    0, 0, 1, 1,     0, 1, 1, 0,     0, 1, 1, 1,
                0, 0, 2, 0, 0, 3, 0, 0,
                0, 2, 2, 4, 0, 1, 0, 0,
                3, 2, 2, 2, 2, 0, 0, 1,
                0, 0, 2, 2, 0, 0, 0, 0,
                5, 0, 0, 0, 2, 2, 2, 4,
                1, 0, 3, 0, 0, 2, 2, 0]
        

        index = [6, 8, 4,    6, 8,   0, 0, 0, 2]

        tamanio = [3, 2, 4]

        id = [-1, -2, 4]
        
        datos = {
            "Combine_grids":combine_grids,
            "Index":index,
            "Tamanio":tamanio,
            "ID":id
        }
        
        #print(datos)

        self._set_response()
        #self.wfile.write(str(datos).encode('utf-8'))
        self.wfile.write(json.dumps(datos).encode('utf-8'))
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


