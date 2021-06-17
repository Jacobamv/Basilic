from japronto import Application

class Broccoli(Application):
    
    def __init__(self, name):
        self.name = name
        super(Broccoli, self).__init__()

    def route(self, route, methods = ['GET']):
        def inner(func):
            self.router.add_route(route, func, methods = methods)
        return inner

