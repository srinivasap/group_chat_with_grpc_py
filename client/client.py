import threading
import sys

import grpc

import yaml
from ratelimit import limits, RateLimitException
from Crypto.Cipher import AES

import messenger_pb2
import messenger_pb2_grpc

address = 'localhost'
# limit number of messages to 3 per user in 30 sec interval
ratelimit_per_user = 1
# rate limit interval 1 sec (for testing)
ratelimit_interval_sec = 1

class Client:

    """
    Initiaizes class member with with command line args and config.xml
    """
    def __init__(self, u, g, p, k, i):
        # set username and group
        self.username = u
        self.groupname = g
        # override default port
        self.port = p
        # initialize encryption suite
        self.enc_suite = AES.new(k, AES.MODE_CBC, i)
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(address + ':' + str(p))
        self.conn = messenger_pb2_grpc.MessengerStub(channel)
        self.auth_user_group()

    """
    Before connecting user to group, validate if user is part of group to initiate group chat
    """
    def auth_user_group(self):
        m = messenger_pb2.Message()
        m.name = self.username
        m.group = self.groupname
        resp = self.conn.AuthUserGroup(m)
        """
        ERROR in response message is treated as error, if yes print and exit
        Otherwise, connect user to group
        """
        if not resp.msg.startswith('[ERROR]'):
            print("[Spartan] Connected to Spartan Server at port {}.".format(self.port))
            print("[Spartan] You are now connected with group {}.".format(self.groupname))
            print("[Spartan] You are ready to chat with {}.".format(resp.msg))
            # run __listen_for_messages in a separate thread
            threading.Thread(target=self.__listen_for_messages, daemon=True).start()
            self.send_message()
        else:
            print(resp.msg)

    """
    Stream messages in the group
    """    
    def __listen_for_messages(self):
        b = messenger_pb2.Blank()
        b.group = self.groupname
        for message in self.conn.ReceiveMsg(b):
            if message.name != self.username:
                print("\n[{}] > {}".format(message.name, message.msg))
                #print("[{}] > ".format(self.username))

    """
    Sending group message
    """
    def send_message(self):
        try:
            while True:
                message = input("[{}] > ".format(self.username))
                if message is not '':
                    m = messenger_pb2.Message()
                    m.name = self.username
                    m.msg = message
                    #m.msg = self.enc_suite.encrypt(self.pad_message_to_16x(message))
                    m.group = self.groupname
                    #self.conn.SendMsg(m)
                    try:
                        self.ratelimit_sendMessages(m)
                    except RateLimitException:
                        print("Ratelimit triggered")
        except KeyboardInterrupt:
            exit(0)

    """
    Limit number of messages sent by the user to the group
    """
    @limits(calls=ratelimit_per_user, period=ratelimit_interval_sec)
    def ratelimit_sendMessages(self, m):
        self.conn.SendMsg(m)

    """
    Pad with nil to make string multiple of 16
    """
    def pad_message_to_16x(self, s):
        pad = str(b"\0" * (AES.block_size - len(s) % AES.block_size), "utf-8")
        return s + pad

"""
GRPC Client
"""
def client():
    # read port server port from config file
    with open("config.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
            port = config['port']
            key = config['aes_secret_key']
            iv = config['aes_secret_kwargs']
        except yaml.YAMLError as exc:
            print(exc)
    # read and set command line args
    c = Client(sys.argv[1], sys.argv[2], port, key, iv)

"""
Main - the entry point
"""
if __name__ == '__main__':
    client()  