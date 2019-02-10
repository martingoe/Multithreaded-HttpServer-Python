import json


class Request:
    response_headers = {}

    def __init__(self, conn, addr):
        # Set the global variables to the specified ones
        self.conn = conn
        self.addr = addr

        # Receive the data from the client
        self.data = self.receive_data()
        # Get information about the client
        information = self.get_information()

        self.attributes = self.get_request_headers()

        # Set global variables according to the information
        self.path = information["path"]
        self.protocol = information["protocol"]
        self.query = information["query"]

    def get_request_headers(self):
        # Remove the first line of the data
        data = self.data[self.data.index("\\r\\n"):].replace("\\r\\n", "", 1)

        # Change the data to be used as JSON
        data = data.replace("\\r\\n", "\", \"").replace(": ", "\": \"")

        # Remove the last 9 characters which is useless junk
        data = data[:len(data) - 9]
        # Set the data to be seen as a JSON Object
        data = "{\"" + data + "\"}"

        return json.loads(data)

    def get_information(self):
        data = {}
        request_str = self.data.replace("b'GET ", "", 1)

        index_after_url = request_str.index(" ")
        data["protocol"] = request_str[index_after_url:request_str.index("\\r\\n")]

        url = request_str[:index_after_url]

        if "?" in url:
            split_data = url.split("?")

            data["path"] = split_data[0]
            data["query"] = split_data[1]
        else:
            data["path"] = url
            data["query"] = None

        return data

    # Add a new response header to the response headers
    def add_response_header(self, key, value):
        self.response_headers[key] = value

    # Send the response to the client
    def send_response(self, string, r_code):
        print("Sending response")

        # Add a response header specifying the content length if it is not yet present
        if "Content-Length" not in self.response_headers:
            self.add_response_header("Content-Length", str(len(string)))

        # Format the headers to be usable
        headers = ""
        for key, value in self.response_headers.items():
            headers += "{}: {}\r\n".format(key, value)

        # Format all the necessary data to a response
        response = "{} {}\r\n{}\r\n{}".format(self.protocol, r_code, headers, string)

        # Send the response and close the connection
        self.conn.send(str.encode(response))
        self.conn.close()

    # Receive the data sent and return it
    def receive_data(self, buffer_time=2048):
        data = self.conn.recv(buffer_time)
        return str(data)
