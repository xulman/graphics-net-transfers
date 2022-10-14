from grpc import insecure_channel, RpcError
from copy import copy
import buckets_with_graphics_pb2
import buckets_with_graphics_pb2_grpc_orig as buckets_with_graphics_pb2_grpc


def main() -> None:
    # this is where it should be transfered to
    clientName = "largeNumberSpheres"
    clientURL = "localhost:9085"
    noOfSpheres = 10000

    serverURL = "localhost:9083"

    try:
        comm = buckets_with_graphics_pb2_grpc.ClientToServerStub( insecure_channel(serverURL) )

        clientGreeting = buckets_with_graphics_pb2.ClientHello()
        clientGreeting.clientID.clientName = clientName
        clientGreeting.returnURL = clientURL
        comm.introduceClient(clientGreeting)

        msg = buckets_with_graphics_pb2.SignedTextMessage()
        msg.clientID.clientName = clientName
        msg.clientMessage.msg = f"I'm sending you {noOfSpheres} spheres"
        comm.showMessage(msg)

        buckets = list()
        for j in range(3):
            bucket = buckets_with_graphics_pb2.BucketOfSpheres()
            bucket.clientID.clientName = clientName
            bucket.bucketID = 121
            bucket.label = f"many spheres, row {j+1}"
            bucket.time = 8
            for i in range(noOfSpheres):
                x = i // 100
                y = i % 100
                sphParams = buckets_with_graphics_pb2.SphereParameters()
                sphParams.centre.x = x
                sphParams.centre.y = y
                sphParams.centre.z = j
                sphParams.radius = 0.3
                sphParams.colorIdx = i % 3
                bucket.spheres.append(sphParams)
            buckets.append(bucket)
        comm.addSpheres(iter(buckets))

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
