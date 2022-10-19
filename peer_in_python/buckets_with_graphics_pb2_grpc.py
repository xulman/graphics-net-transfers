# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import buckets_with_graphics_pb2 as buckets__with__graphics__pb2


class ClientToServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.introduceClient = channel.unary_unary(
                '/transfers_graphics_protocol.ClientToServer/introduceClient',
                request_serializer=buckets__with__graphics__pb2.ClientHello.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.addSpheres = channel.stream_unary(
                '/transfers_graphics_protocol.ClientToServer/addSpheres',
                request_serializer=buckets__with__graphics__pb2.BucketOfSpheres.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.addLines = channel.stream_unary(
                '/transfers_graphics_protocol.ClientToServer/addLines',
                request_serializer=buckets__with__graphics__pb2.BucketOfLines.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.addVectors = channel.stream_unary(
                '/transfers_graphics_protocol.ClientToServer/addVectors',
                request_serializer=buckets__with__graphics__pb2.BucketOfVectors.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.showMessage = channel.unary_unary(
                '/transfers_graphics_protocol.ClientToServer/showMessage',
                request_serializer=buckets__with__graphics__pb2.SignedTextMessage.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.focusEvent = channel.unary_unary(
                '/transfers_graphics_protocol.ClientToServer/focusEvent',
                request_serializer=buckets__with__graphics__pb2.SignedClickedIDs.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.unfocusEvent = channel.unary_unary(
                '/transfers_graphics_protocol.ClientToServer/unfocusEvent',
                request_serializer=buckets__with__graphics__pb2.ClientIdentification.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.selectEvent = channel.unary_unary(
                '/transfers_graphics_protocol.ClientToServer/selectEvent',
                request_serializer=buckets__with__graphics__pb2.SignedClickedIDs.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.unselectEvent = channel.unary_unary(
                '/transfers_graphics_protocol.ClientToServer/unselectEvent',
                request_serializer=buckets__with__graphics__pb2.SignedClickedIDs.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )


class ClientToServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def introduceClient(self, request, context):
        """*
        client should start communication with this message,
        in this message the client may (not "must") additionally register
        a call back URL at which the server will be sending notifications

        if this message is omited, unmatched incoming requests will
        be placed into "unknown_source" collection
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addSpheres(self, request_iterator, context):
        """*
        one bucket of one-type-of-graphics is requested to be displayed,
        this request shall contain a burst/batch of instances that all
        shall appear in this created bucket

        since the display need not be able to distinguish among instances
        within a bucket, only an ID of the bucket is transfered and no IDs
        for the individual instances
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addLines(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addVectors(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def showMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def focusEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unfocusEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def selectEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unselectEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientToServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'introduceClient': grpc.unary_unary_rpc_method_handler(
                    servicer.introduceClient,
                    request_deserializer=buckets__with__graphics__pb2.ClientHello.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'addSpheres': grpc.stream_unary_rpc_method_handler(
                    servicer.addSpheres,
                    request_deserializer=buckets__with__graphics__pb2.BucketOfSpheres.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'addLines': grpc.stream_unary_rpc_method_handler(
                    servicer.addLines,
                    request_deserializer=buckets__with__graphics__pb2.BucketOfLines.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'addVectors': grpc.stream_unary_rpc_method_handler(
                    servicer.addVectors,
                    request_deserializer=buckets__with__graphics__pb2.BucketOfVectors.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'showMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.showMessage,
                    request_deserializer=buckets__with__graphics__pb2.SignedTextMessage.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'focusEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.focusEvent,
                    request_deserializer=buckets__with__graphics__pb2.SignedClickedIDs.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'unfocusEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.unfocusEvent,
                    request_deserializer=buckets__with__graphics__pb2.ClientIdentification.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'selectEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.selectEvent,
                    request_deserializer=buckets__with__graphics__pb2.SignedClickedIDs.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'unselectEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.unselectEvent,
                    request_deserializer=buckets__with__graphics__pb2.SignedClickedIDs.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'transfers_graphics_protocol.ClientToServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClientToServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def introduceClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ClientToServer/introduceClient',
            buckets__with__graphics__pb2.ClientHello.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addSpheres(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/transfers_graphics_protocol.ClientToServer/addSpheres',
            buckets__with__graphics__pb2.BucketOfSpheres.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addLines(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/transfers_graphics_protocol.ClientToServer/addLines',
            buckets__with__graphics__pb2.BucketOfLines.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addVectors(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/transfers_graphics_protocol.ClientToServer/addVectors',
            buckets__with__graphics__pb2.BucketOfVectors.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def showMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ClientToServer/showMessage',
            buckets__with__graphics__pb2.SignedTextMessage.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def focusEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ClientToServer/focusEvent',
            buckets__with__graphics__pb2.SignedClickedIDs.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def unfocusEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ClientToServer/unfocusEvent',
            buckets__with__graphics__pb2.ClientIdentification.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def selectEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ClientToServer/selectEvent',
            buckets__with__graphics__pb2.SignedClickedIDs.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def unselectEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ClientToServer/unselectEvent',
            buckets__with__graphics__pb2.SignedClickedIDs.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ServerToClientStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.showMessage = channel.unary_unary(
                '/transfers_graphics_protocol.ServerToClient/showMessage',
                request_serializer=buckets__with__graphics__pb2.TextMessage.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.focusEvent = channel.unary_unary(
                '/transfers_graphics_protocol.ServerToClient/focusEvent',
                request_serializer=buckets__with__graphics__pb2.ClickedIDs.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.unfocusEvent = channel.unary_unary(
                '/transfers_graphics_protocol.ServerToClient/unfocusEvent',
                request_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.selectEvent = channel.unary_unary(
                '/transfers_graphics_protocol.ServerToClient/selectEvent',
                request_serializer=buckets__with__graphics__pb2.ClickedIDs.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )
        self.unselectEvent = channel.unary_unary(
                '/transfers_graphics_protocol.ServerToClient/unselectEvent',
                request_serializer=buckets__with__graphics__pb2.ClickedIDs.SerializeToString,
                response_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                )


class ServerToClientServicer(object):
    """Missing associated documentation comment in .proto file."""

    def showMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def focusEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unfocusEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def selectEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unselectEvent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServerToClientServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'showMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.showMessage,
                    request_deserializer=buckets__with__graphics__pb2.TextMessage.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'focusEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.focusEvent,
                    request_deserializer=buckets__with__graphics__pb2.ClickedIDs.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'unfocusEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.unfocusEvent,
                    request_deserializer=buckets__with__graphics__pb2.Empty.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'selectEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.selectEvent,
                    request_deserializer=buckets__with__graphics__pb2.ClickedIDs.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
            'unselectEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.unselectEvent,
                    request_deserializer=buckets__with__graphics__pb2.ClickedIDs.FromString,
                    response_serializer=buckets__with__graphics__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'transfers_graphics_protocol.ServerToClient', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ServerToClient(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def showMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ServerToClient/showMessage',
            buckets__with__graphics__pb2.TextMessage.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def focusEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ServerToClient/focusEvent',
            buckets__with__graphics__pb2.ClickedIDs.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def unfocusEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ServerToClient/unfocusEvent',
            buckets__with__graphics__pb2.Empty.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def selectEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ServerToClient/selectEvent',
            buckets__with__graphics__pb2.ClickedIDs.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def unselectEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/transfers_graphics_protocol.ServerToClient/unselectEvent',
            buckets__with__graphics__pb2.ClickedIDs.SerializeToString,
            buckets__with__graphics__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
