from grpc import insecure_channel, RpcError
import buckets_with_graphics_pb2 as PROTOCOL
import buckets_with_graphics_pb2_grpc
from math import sin


def rgb_to_integer(r,g,b):
    return r*65536 + g*256 + b


def get_xy(index:int):
    line_length = 250
    x = 2.1 + (index % line_length)*1.5
    y = 3.0 * (index // line_length)
    return x,y


def main() -> None:
    # this is the name of the source (this code) and where it is listening (for feedback events)
    # (however, I haven't here implemented the feedback listening...)
    # (...which doesn't matter 'cause I haven't implemented the feedback sending in Blender either ): )
    clientName = "source_of_50k"
    clientURL = "localhost:9085"

    # this is where the sink (Blender) is listening (for display elem requests)
    serverURL = "localhost:9083"


    try:
        comm = buckets_with_graphics_pb2_grpc.ClientToServerStub( insecure_channel(serverURL) )

        print("going to send the 'introduce me' message... (press Enter key)")
        input()

        clientGreeting = PROTOCOL.ClientHello()
        clientGreeting.clientID.clientName = clientName
        clientGreeting.returnURL = clientURL
        comm.introduceClient(clientGreeting)

        print("going to send one more 'introduce me' message...")
        input()

        # re-introduce ourselves again, this time we don't provide feedback URL
        # (which a signal that we don't want to be getting any feedback events)
        clientGreeting = PROTOCOL.ClientHello()
        clientGreeting.clientID.clientName = clientName
        comm.introduceClient(clientGreeting)


        print("going to send a text message...")
        input()

        noOfSpheres = 50000
        msg = PROTOCOL.SignedTextMessage()
        msg.clientID.clientName = clientName
        msg.clientMessage.msg = f"I'm sending you {noOfSpheres} spheres"
        comm.showMessage(msg)


        print(f"going to send {noOfSpheres} spheres, like for real... (press Enter key)")
        input()

        # the protocol expects multiple messages to be sent in one "physical grpc call"
        messages = list()

        # the first message, it will request to show 'noOfSpheres'
        # in 'the first spheres' collection of ours, the spheres will
        # appear as Blender object/node with the name 'spheres at TP=1'
        one_message = PROTOCOL.BatchOfGraphics()
        one_message.clientID.clientName = clientName  # gprc is REST -> no sessions -> inform who is sending
        one_message.collectionName = "the spheres"    # our own arbitrary (but mandatory!) grouping of content
        one_message.dataName = "spheres at TP=1"      # name of the object that will represent the content
        one_message.dataID = 13                       # our own ID that Blender will use in the feedback messages
        #
        # start requesting the spheres to be displayed
        for i in range(noOfSpheres):
            sphParams = PROTOCOL.SphereParameters()
            sphParams.centre.x,sphParams.centre.y = get_xy(i)
            sphParams.centre.z = 0.1
            sphParams.time = 1
            sphParams.radius = 1.1
            sphParams.colorIdx = (1 + i%10) * 6
            one_message.spheres.append(sphParams)

        # enlist/schedule this particular message to be sent shortly
        messages.append(one_message)

        # the second message, it will request... well... spheres again
        one_message = PROTOCOL.BatchOfGraphics()
        one_message.clientID.clientName = clientName
        one_message.collectionName = "the spheres"  # yes, we're going to add more stuff into the same/one collection
        one_message.dataName = "spheres at TP=2"    # just under different Blender object
        one_message.dataID = 14
        for i in range(noOfSpheres):
            sphParams = PROTOCOL.SphereParameters()
            sphParams.centre.x,sphParams.centre.y = get_xy(i)
            sphParams.centre.z = 0.1
            sphParams.time = 2
            sphParams.radius = 1.3
            sphParams.colorIdx = (0 + i%10) * 4
            one_message.spheres.append(sphParams)

        # enlist/schedule this particular message to be sent shortly
        messages.append(one_message)

        # send the all enlisted messages now
        comm.addGraphics(iter(messages))


        print(f"going to send {noOfSpheres} vectors and lines...")
        input()

        messages = list()
        one_message = PROTOCOL.BatchOfGraphics()
        one_message.clientID.clientName = clientName
        one_message.collectionName = "mixed content"
        one_message.dataName = "vecs and lines at TP = 2"
        one_message.dataID = 15
        #
        for i in range(0,noOfSpheres,2):
            vecParams = PROTOCOL.VectorParameters()
            vecParams.startPos.x,vecParams.startPos.y = get_xy(i)
            vecParams.startPos.z = 1.4
            vecParams.endPos.x = vecParams.startPos.x
            vecParams.endPos.y = vecParams.startPos.y + sin(3.14159*float(i)/20.0)
            vecParams.endPos.z = 2.1
            vecParams.time = 2
            vecParams.radius = 0.2
            colorShade = (1 + i%3) * 80
            vecParams.colorXRGB = rgb_to_integer(255//(i+1),0,colorShade)
            one_message.vectors.append(vecParams)
        #
        for i in range(1,noOfSpheres,2):
            lineParams = PROTOCOL.LineParameters()
            lineParams.startPos.x,lineParams.startPos.y = get_xy(i)
            lineParams.startPos.z = 1.4
            lineParams.endPos.x = lineParams.startPos.x
            lineParams.endPos.y = lineParams.startPos.y + sin(3.14159*float(i)/20.0)
            lineParams.endPos.z = 2.1
            lineParams.time = 2
            lineParams.radius = 0.2
            colorShade = (1 + i%3) * 80
            lineParams.colorXRGB = rgb_to_integer(255//(i+1),0,colorShade)
            one_message.lines.append(lineParams)
        # notice that we were requesting _both_ vectors and lines in _one_ message,
        # both will appear under the one Blender object;
        # in other words, the Blender object need not show content of only one shape...
        #
        messages.append(one_message)
        comm.addGraphics(iter(messages))


        print("going to send a request to select some of the previously sent objects...")
        input()

        select = PROTOCOL.SignedClickedIDs()
        select.clientID.clientName = clientName
        select.clientClickedIDs.objIDs.append(14)
        select.clientClickedIDs.objIDs.append(15)
        comm.selectEvent(select)

        name = PROTOCOL.ClientIdentification()
        name.clientName = clientName
        comm.unfocusEvent(name)


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
