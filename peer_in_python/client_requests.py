from grpc import insecure_channel, RpcError
from copy import copy
import buckets_with_graphics_pb2
import buckets_with_graphics_pb2_grpc


def rgb_to_integer(r,g,b):
    return r*65536 + g*256 + b

def main() -> None:
    # this is where it should be transfered to
    clientName = "colorReporter"
    clientURL = "localhost:9085"
    noOfSpheres = 3

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

        print("waiting for Enter key")
        input()

        msg = buckets_with_graphics_pb2.SignedTextMessage()
        msg.clientID.clientName = clientName
        msg.clientMessage.msg = f"I'm sending you {noOfSpheres} spheres"
        comm.showMessage(msg)

        print("waiting for Enter key")
        input()

        batches = list()
        #
        elem_group = buckets_with_graphics_pb2.BatchOfGraphics()
        elem_group.clientID.clientName = clientName
        elem_group.collectionName = "the first spheres"
        elem_group.dataName = "spheres at TP=1"
        elem_group.dataID = 13
        for i in range(noOfSpheres):
            sphParams = buckets_with_graphics_pb2.SphereParameters()
            sphParams.centre.x = 2.1 + i*1.5
            sphParams.centre.y = 0
            sphParams.centre.z = -1.5
            sphParams.time = 1
            sphParams.radius = 1.1
            sphParams.colorIdx = (1 + i%3) * 20
            elem_group.spheres.append(sphParams)
        batches.append(elem_group)
        #
        elem_group = buckets_with_graphics_pb2.BatchOfGraphics()
        elem_group.clientID.clientName = clientName
        elem_group.collectionName = "the second spheres"
        elem_group.dataName = "spheres at TP=2"
        elem_group.dataID = 14
        for i in range(noOfSpheres):
            sphParams = buckets_with_graphics_pb2.SphereParameters()
            sphParams.centre.x = 2.1 + i*1.5
            sphParams.centre.y = 0.5
            sphParams.centre.z = 0.1
            sphParams.time = 2
            sphParams.radius = 1.3
            sphParams.colorIdx = (0 + i%3) * 15
            elem_group.spheres.append(sphParams)
        batches.append(elem_group)
        #
        #comm.addGraphics(iter(batches))

        #print("waiting for Enter key")
        #input()

        #batches = list()
        elem_group = buckets_with_graphics_pb2.BatchOfGraphics()
        elem_group.clientID.clientName = clientName
        elem_group.collectionName = "a couple of vectors"
        elem_group.dataName = "vecs at TP = 3"
        elem_group.dataID = 15
        for i in range(noOfSpheres):
            vecParams = buckets_with_graphics_pb2.VectorParameters()
            vecParams.startPos.x = 2.1 + i*1.5
            vecParams.startPos.y = 0.5
            vecParams.startPos.z = 0.1
            vecParams.endPos.x = 2.1 + i*1.5
            vecParams.endPos.y = 0.5
            vecParams.endPos.z = 5.1
            vecParams.time = 4
            vecParams.radius = 0.2
            colorShade = (1 + i%3) * 80
            vecParams.colorXRGB = rgb_to_integer(255//(i+1),0,colorShade)
            elem_group.vectors.append(vecParams)
        batches.append(elem_group)
        comm.addGraphics(iter(batches))

        print("waiting for Enter key")
        input()

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
