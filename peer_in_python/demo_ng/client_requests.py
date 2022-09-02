from grpc import insecure_channel, RpcError
from copy import copy
import buckets_with_graphics_pb2
import buckets_with_graphics_pb2_grpc


def main() -> None:
    # this is where it should be transfered to
    clientName = "fakeMastodonRequester"
    clientURL = "localhost:9085"
    noOfSpheres = 2

    serverURL = "localhost:9083"

    try:
        comm = buckets_with_graphics_pb2_grpc.ClientToServerStub( insecure_channel(serverURL) )

        clientGreeting = buckets_with_graphics_pb2.ClientHello()
        clientGreeting.clientID.clientName = clientName
        clientGreeting.returnURL = clientURL
        comm.introduceClient(clientGreeting)

        clientGreeting = buckets_with_graphics_pb2.ClientHello()
        clientGreeting.clientID.clientName = clientName
        comm.introduceClient(clientGreeting)

        msg = buckets_with_graphics_pb2.SignedTextMessage()
        msg.clientID.clientName = clientName
        msg.clientMessage.msg = f"I'm sending you {noOfSpheres} spheres"
        comm.showMessage(msg)

        buckets = list()
        #
        bucket = buckets_with_graphics_pb2.BucketOfSpheres()
        bucket.clientID.clientName = clientName
        bucket.bucketID = 13
        bucket.label = "a couple of spheres"
        bucket.time = 2
        for i in range(noOfSpheres):
            sphParams = buckets_with_graphics_pb2.SphereParameters()
            sphParams.centre.x = 2.1 + i*1.5
            sphParams.centre.y = 0
            sphParams.centre.z = 0.1
            sphParams.radius = 1.1
            sphParams.colorIdx = i % 3
            bucket.spheres.append(sphParams)
        buckets.append(bucket)
        #
        bucket = buckets_with_graphics_pb2.BucketOfSpheres()
        bucket.clientID.clientName = clientName
        bucket.bucketID = 14
        bucket.label = "a couple of spheres"
        bucket.time = 3
        for i in range(noOfSpheres):
            sphParams = buckets_with_graphics_pb2.SphereParameters()
            sphParams.centre.x = 2.1 + i*1.5
            sphParams.centre.y = 0.5
            sphParams.centre.z = 0.1
            sphParams.radius = 1.3
            sphParams.colorIdx = i % 3
            bucket.spheres.append(sphParams)
        buckets.append(bucket)
        #
        comm.addSpheres(iter(buckets))

        buckets = list()
        bucket = buckets_with_graphics_pb2.BucketOfVectors()
        bucket.clientID.clientName = clientName
        bucket.bucketID = 15
        bucket.label = "a couple of vectors"
        bucket.time = 3
        for i in range(noOfSpheres):
            vecParams = buckets_with_graphics_pb2.VectorParameters()
            vecParams.startPos.x = 2.1 + i*1.5
            vecParams.startPos.y = 0.5
            vecParams.startPos.z = 0.1
            vecParams.endPos.x = 2.1 + i*1.5
            vecParams.endPos.y = 0.5
            vecParams.endPos.z = 5.1
            vecParams.radius = 0.2
            vecParams.colorIdx = i % 3
            bucket.vectors.append(vecParams)
        buckets.append(bucket)
        comm.addVectors(iter(buckets))

        select = buckets_with_graphics_pb2.SignedClickedIDs()
        select.clientID.clientName = clientName
        select.clientClickedIDs.objIDs.append(14)
        select.clientClickedIDs.objIDs.append(15)
        comm.selectEvent(select)
        #comm.focusEvent(select)

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
