import sys
from urllib import parse
import http.server
import prometheus_client

TOTAL_REQUESTS = prometheus_client.Counter('app_http_total_requests', "Total number of http request hit", ('method', 'path', 'status_code'))

class MyHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    path_meta = parse.urlparse(self.path)
    print(path_meta)
    if path_meta.path == "/":
      TOTAL_REQUESTS.labels('GET', path_meta.path, 200).inc()
      self.send_response(200)
      self.end_headers()
      self.wfile.write(b"Hello World")
    elif path_meta.path == "/welcome":
      TOTAL_REQUESTS.labels('GET', path_meta.path, 200).inc()
      self.send_response(200)
      self.end_headers()
      self.wfile.write(b"Hello user")
    else:
      TOTAL_REQUESTS.labels('GET', path_meta.path, 404).inc()
      self.send_error(404, "Path: {}".format(path_meta.path))

def main():
  try:  
    if len(sys.argv) == 3:
      web_port = int(sys.argv[1])
      exporter_port = int(sys.argv[2])
      print("Starting api exporter on port: {}".format(exporter_port))
      prometheus_client.start_http_server(exporter_port)
      print("Starting app server on port: {}".format(web_port))
      server = http.server.HTTPServer(('localhost', web_port), MyHandler)
      server.serve_forever()
    else:
      print("Usage: python3 api_app.py <web_port> <exporter_port>")
      sys.exit(0)
  except Exception as e:
    print("Error: {}".format(e))
    sys.exit(1)

if __name__ == '__main__':
  main()
