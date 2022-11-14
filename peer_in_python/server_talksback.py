from grpc import insecure_channel, RpcError
import buckets_with_graphics_pb2 as PROTOCOL
import buckets_with_graphics_pb2_grpc


def main() -> None:
    # this is the (hypothetical) client that talked to use previously (and sent some data here)
    clientName = "source_of_50k"
    clientURL = "localhost:9085"


    try:
        comm = buckets_with_graphics_pb2_grpc.ServerToClientStub( insecure_channel(clientURL) )

        print("going to send a text message...")
        input()

        msg = PROTOCOL.TextMessage()
        msg.msg = "Thank you, I have received all your data and now I'm showing it..."
        comm.showMessage(msg)


        print("going to send a request to select some of the previously sent objects...")
        input()

        select = PROTOCOL.ClickedIDs()
        select.objIDs.append(14)
        select.objIDs.append(15)
        comm.selectEvent(select)


        print("going to send a request not to focus on anything particular...")
        input()

        nothing = PROTOCOL.Empty()
        comm.unfocusEvent(nothing)


    except RpcError as e:
        print("Some connection error, details follow:")
        print("==============")
        print(e)
        print("==============")
    except Exception as e:
        print("Some general error, details follow:")
        print("==============")
        print(e)
        print("==============")

    print("this demo is over now, thanks ;-)")


if __name__ == '__main__':
    main()
