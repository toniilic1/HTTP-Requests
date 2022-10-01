from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

names_dict = {'john': 'smith',
              'david': 'jones',
              'michael': 'johnson',
              'chris': 'lee'}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_message("Incoming GET request...")
        try:
            name = parse_qs(self.path[2:])['name'][0]

        except:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
            return

        if name in names_dict.keys():
            self.send_response_to_client(200, names_dict[name])

        else:
            self.send_response_to_client(404, 'Name not found')
            self.log_message("Name not found")

    def do_POST(self):
        self.log_message('Incoming POST request...')
        data = parse_qs(self.path[2:])

        try:
            names_dict[data['name'][0]] = data['last_name'][0]
            self.send_response_to_client(200, names_dict)

        except KeyError:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")

    def do_DELETE(self):
        self.log_message('Incoming DELETE request...')
        try:
            name = parse_qs(self.path[2:])['name'][0]
        except KeyError:
            self.send_response_to_client(404, self.path[2:])
            self.log_message("Incorrect parameters provided")
            return

        for key, value in names_dict.items():
            if name in names_dict.keys() or names_dict.values():

                if key == name:
                    del names_dict[key]
                    self.send_response_to_client(200, f'Name found and deleted {names_dict}')
                    self.log_message("Name found and deleted")
                    break

                elif value == name:
                    del names_dict[key]
                    self.send_response_to_client(200, f'Last Name found and deleted {names_dict}')
                    self.log_message("Last Name found and deleted")
                    break

        else:
            self.send_response_to_client(404, 'Name does not exist')
            self.log_message("Name does not exist")


    def send_response_to_client(self, status_code, data):
        # Send OK status
        self.send_response(status_code)
        # Send headers
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        # Send the response
        self.wfile.write(str(data).encode())


server_address = ('127.0.0.1', 8080)
http_server = HTTPServer(server_address, RequestHandler)
http_server.serve_forever()