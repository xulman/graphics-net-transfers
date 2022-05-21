from grpc import insecure_channel, RpcError
from copy import copy
import points_and_lines_pb2
import points_and_lines_pb2_grpc


def main() -> None:
    # this is where it should be transfered to
    serverURL = "localhost:9081"

    # a test point to be transfered over
    p = points_and_lines_pb2.PointAsBall()
    p.ID = 10
    p.x = 1.2
    p.y = 1.3
    p.z = 1.4
    p.t = 2
    p.label = "testing point"
    p.color_r = 0.9
    p.color_g = 0.1
    p.color_b = 0.05
    p.radius = 3.1

    try:
        # the transfer itself
        print("Sending: "+str(p))
        comm = points_and_lines_pb2_grpc.PointsAndLinesStub( insecure_channel(serverURL) )

        Ps = list()
        for i in range(5):
            p.x = (i  % 50) *5
            p.y = (i // 50) *5
            p.ID = i+10
            p.label = "tesing point #"+str(p.ID)

            Ps.append(copy(p))

        comm.sendBall( iter(Ps) )

        msg = points_and_lines_pb2.TickMessage()
        msg.message = "Demo sent you "+str(len(Ps))+" items"
        comm.sendTick( msg )

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

    print("done.")

if __name__ == '__main__':
    main()
