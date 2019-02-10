from Handler import Handler
from Server import Server


class Handle(Handler):
    def handle(self, request):
        request.add_response_header("Access-Allow-Content-Origin", "*")
        request.add_response_header("Content-Type", "text/html")
        request.send_response("<p>{}</p>".format(request.query), 200)


server = Server(2021, 20)
server.create_context("/test", Handle)
server.start()
