import bridge

bridge = bridge.Bridge()

class ChatServer(bridge.Service):
    def join(self, name, handler, callback):
        print('%s is joining the lobby.' % (name))
        bridge.join_channel('lobby', handler, callback)

def start_server():
    def on_client_join():
        print("I joined the lobby!")

    bridge.publish_service('chatserver', ChatServer, on_client_join)

bridge.ready(start_server)