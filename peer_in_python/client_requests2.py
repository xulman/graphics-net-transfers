from grpc import insecure_channel, RpcError
from copy import copy
import buckets_with_graphics_pb2
import buckets_with_graphics_pb2_grpc


def main() -> None:
    # this is where it should be transfered to
    clientName = "largeNumberSpheres_yetAgain!"
    clientURL = "localhost:9085"

    serverURL = "localhost:9083"



    noOfSpheres = 30000


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

        z_offset = 4.5


        buckets = list()
        for j in range(3):
            bucket = buckets_with_graphics_pb2.BatchOfGraphics()
            bucket.clientID.clientName = clientName
            bucket.collectionName = "Default collection"
            bucket.dataName = f"many spheres, row {j+1}"
            bucket.dataID = 121
            groupingSize = 1000
            for i in range(noOfSpheres):
                x = i // groupingSize
                y = i % groupingSize
                sphParams = buckets_with_graphics_pb2.SphereParameters()
                sphParams.centre.x = x+0.8
                sphParams.centre.y = y
                sphParams.centre.z = j + z_offset
                sphParams.time = 15+j
                sphParams.radius = 0.3
                sphParams.colorIdx = i % 65
                bucket.spheres.append(sphParams)
            buckets.append(bucket)
        comm.addGraphics(iter(buckets))


        bucket = buckets_with_graphics_pb2.BatchOfGraphics()
        bucket.clientID.clientName = clientName
        bucket.collectionName = "vectors and lines"
        bucket.dataName = "testing vectors"
        bucket.dataID = 128
        #
        vector = buckets_with_graphics_pb2.VectorParameters()
        vector.startPos.x = 10
        vector.startPos.y = 10
        vector.startPos.z = 16 + z_offset
        vector.endPos.x = 15
        vector.endPos.y = 10
        vector.endPos.z = 17 + z_offset
        vector.time = 18
        vector.radius = 2
        vector.colorIdx = 0
        bucket.vectors.append(vector)
        #
        vector = buckets_with_graphics_pb2.VectorParameters()
        vector.startPos.x = 10
        vector.startPos.y = 10
        vector.startPos.z = 15 + z_offset
        vector.endPos.x = 15
        vector.endPos.y = 10
        vector.endPos.z = 16 + z_offset
        vector.time = 18
        vector.radius = 2
        vector.colorXRGB = 0x00FFFFFE
        bucket.vectors.append(vector)
        #
        vector = buckets_with_graphics_pb2.VectorParameters()
        vector.startPos.x = 10
        vector.startPos.y = 15
        vector.startPos.z = 15 + z_offset
        vector.endPos.x = 15
        vector.endPos.y = 15
        vector.endPos.z = 16 + z_offset
        vector.time = 18
        vector.radius = 2
        vector.colorIdx = 1
        bucket.vectors.append(vector)
        #
        vector = buckets_with_graphics_pb2.VectorParameters()
        vector.startPos.x = 10
        vector.startPos.y = 15
        vector.startPos.z = 16 + z_offset
        vector.endPos.x = 15
        vector.endPos.y = 15
        vector.endPos.z = 17 + z_offset
        vector.time = 18
        vector.radius = 2
        vector.colorXRGB = 0x00FF0000
        bucket.vectors.append(vector)
        #
        stream_of_lines = list()
        stream_of_lines.append(bucket)
        comm.addGraphics(iter(stream_of_lines))


        bucket = buckets_with_graphics_pb2.BatchOfGraphics()
        bucket.clientID.clientName = clientName
        bucket.collectionName = "vectors and lines"
        bucket.dataName = "testing lines"
        bucket.dataID = 129
        #
        line = buckets_with_graphics_pb2.LineParameters()
        line.startPos.x = 10
        line.startPos.y = 10
        line.startPos.z = 16 + z_offset
        line.endPos.x = 15
        line.endPos.y = 10
        line.endPos.z = 17 + z_offset
        line.time = 19
        line.radius = 2
        line.colorIdx = 0
        bucket.lines.append(line)
        #
        line = buckets_with_graphics_pb2.LineParameters()
        line.startPos.x = 10
        line.startPos.y = 10
        line.startPos.z = 15 + z_offset
        line.endPos.x = 15
        line.endPos.y = 10
        line.endPos.z = 16 + z_offset
        line.time = 19
        line.radius = 2
        line.colorXRGB = 0x00FFFFFE
        bucket.lines.append(line)
        #
        line = buckets_with_graphics_pb2.LineParameters()
        line.startPos.x = 10
        line.startPos.y = 15
        line.startPos.z = 15 + z_offset
        line.endPos.x = 15
        line.endPos.y = 15
        line.endPos.z = 16 + z_offset
        line.time = 19
        line.radius = 2
        line.colorIdx = 1
        bucket.lines.append(line)
        #
        line = buckets_with_graphics_pb2.LineParameters()
        line.startPos.x = 10
        line.startPos.y = 15
        line.startPos.z = 16 + z_offset
        line.endPos.x = 15
        line.endPos.y = 15
        line.endPos.z = 17 + z_offset
        line.time = 19
        line.radius = 2
        line.colorXRGB = 0x00FF0000
        bucket.lines.append(line)
        #
        stream_of_graphics = list()
        stream_of_graphics.append(bucket)
        comm.addGraphics(iter(stream_of_graphics))

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
