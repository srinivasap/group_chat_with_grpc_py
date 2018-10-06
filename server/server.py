from concurrent import futures

import time
import grpc
import yaml

import messenger_pb2
import messenger_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# default port, overriden by on one in config
port = 50051
# max number of messages to keep in memory for each group
lru_limit = 50

class Messenger(messenger_pb2_grpc.MessengerServicer):

    """
    Initialize class memebers with config.yml attributes
    """
    def __init__(self):
        self.messages = []
        self.group_messages = {}
        with open("config.yml", 'r') as stream:
            try:
                #print(yaml.load(stream))
                config = yaml.load(stream)
                # override default global port with one defined in config
                global port
                port = config['port']
                self.users = config['users']
                self.groups = config['groups']
                # initialize stack for each group to maintain history
                for key in self.groups.keys():
                    self.group_messages[key] = []
            except yaml.YAMLError as exc:
                print(exc)
    """
    Authenticate if user can connect to a specific group
    """
    def AuthUserGroup(self, request, context):
        resp = messenger_pb2.Message()
        # check in group is part of allowed groups
        if request.group not in self.groups:
            print("[ERROR] group {} is not one of allowed groups {}.".format(request.group, list(self.groups.keys())))
            resp.msg = "[ERROR] group {} is not one of allowed groups.".format(request.name)
            return resp
        # check if member is part of requested group
        elif request.name not in self.groups[request.group]:
            print("[ERROR] user {} is not part of group {}".format(request.name, request.group))
            resp.msg = "[ERROR] user {} is not part of group {}".format(request.name, request.group)
            return resp
        # if user is memeber of group, then return list of members in the group
        resp.msg = str(self.groups[request.group])
        return resp

    """
    Listen to group messages and applies lru_limit
    """  
    def ReceiveMsg(self, request, context):
        lastindex = 0
        g_messages = self.group_messages[request.group]
        while True:
            while len(g_messages) > lastindex:
                n = g_messages[lastindex]
                lastindex += 1
                # if number of messages in group specific stack is greater than lru_limit, then pop first element from the stack
                if len(g_messages) > lru_limit:
                    g_messages.pop()
                    lastindex -= 1
                yield n

    """
    Receive message from client and add to group messages stack
    """
    def SendMsg(self, request, context):
        print("[{}] {}".format(request.name, request.msg))
        g_messages = self.group_messages[request.group]
        g_messages.append(request)
        return messenger_pb2.Blank()

"""
Startup GRPC server
"""
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messenger_pb2_grpc.add_MessengerServicer_to_server(Messenger(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    print("Spartan server started on port {}.".format(port))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

"""
Main - entry point
"""
if __name__ == '__main__':
    serve()