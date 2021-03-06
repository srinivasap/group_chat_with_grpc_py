# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import messenger_pb2 as messenger__pb2


class MessengerStub(object):
  """Service
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.AuthUserGroup = channel.unary_unary(
        '/messenger.Messenger/AuthUserGroup',
        request_serializer=messenger__pb2.Message.SerializeToString,
        response_deserializer=messenger__pb2.Message.FromString,
        )
    self.ReceiveMsg = channel.unary_stream(
        '/messenger.Messenger/ReceiveMsg',
        request_serializer=messenger__pb2.Blank.SerializeToString,
        response_deserializer=messenger__pb2.Message.FromString,
        )
    self.SendMsg = channel.unary_unary(
        '/messenger.Messenger/SendMsg',
        request_serializer=messenger__pb2.Message.SerializeToString,
        response_deserializer=messenger__pb2.Blank.FromString,
        )


class MessengerServicer(object):
  """Service
  """

  def AuthUserGroup(self, request, context):
    """authentication
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReceiveMsg(self, request, context):
    """operation - receive messages as stream
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendMsg(self, request, context):
    """operation - send message and with blank response
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MessengerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'AuthUserGroup': grpc.unary_unary_rpc_method_handler(
          servicer.AuthUserGroup,
          request_deserializer=messenger__pb2.Message.FromString,
          response_serializer=messenger__pb2.Message.SerializeToString,
      ),
      'ReceiveMsg': grpc.unary_stream_rpc_method_handler(
          servicer.ReceiveMsg,
          request_deserializer=messenger__pb2.Blank.FromString,
          response_serializer=messenger__pb2.Message.SerializeToString,
      ),
      'SendMsg': grpc.unary_unary_rpc_method_handler(
          servicer.SendMsg,
          request_deserializer=messenger__pb2.Message.FromString,
          response_serializer=messenger__pb2.Blank.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'messenger.Messenger', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
