from grpc import server, RpcError
from concurrent import futures
from time import sleep
import points_and_lines_pb2
import points_and_lines_pb2_grpc

# this is where it should be listening at
serverName = "demoServer"
serverPort = 9081

class IncomingPLProcessor(points_and_lines_pb2_grpc.PointsAndLinesServicer):
    def sendBall(self, request_iter, context):
        for request in request_iter:
            print("Got Ball request with params:");
            print("ID = "+str(request.ID)+"\n"
                "x = "+str(request.x)+"\n"
                "y = "+str(request.y)+"\n"
                "z = "+str(request.z)+"\n"
                "t = "+str(request.t)+"\n"
                "label = "+str(request.label)+"\n"
                "color_r = "+str(request.color_r)+"\n"
                "color_g = "+str(request.color_g)+"\n"
                "color_b = "+str(request.color_b)+"\n"
                "radius = "+str(request.radius))
        return points_and_lines_pb2.Empty()

    def sendEllipsoid(self, request_iter, context):
        print("Ain't touching this now...")
        return points_and_lines_pb2.Empty()

    def sendLineWithPos(self, request_iter, context):
        for request in request_iter:
            print("Got Line-POS request with params:");
            print("ID = "+str(request.ID)+"\n"
                "from_x = "+str(request.from_x)+"\n"
                "from_y = "+str(request.from_y)+"\n"
                "from_z = "+str(request.from_z)+"\n"
                "to_x = "+str(request.to_x)+"\n"
                "to_y = "+str(request.to_y)+"\n"
                "to_z = "+str(request.to_z)+"\n"
                "label = "+str(request.label)+"\n"
                "color_r = "+str(request.color_r)+"\n"
                "color_g = "+str(request.color_g)+"\n"
                "color_b = "+str(request.color_b)+"\n"
                "radius = "+str(request.radius))
        return points_and_lines_pb2.Empty()

    def sendLineWithIDs(self, request_iter, context):
        for request in request_iter:
            print("Got Line-IDs request with params:");
            print("ID = "+str(request.ID)+"\n"
                "from_pointID = "+str(request.from_pointID)+"\n"
                "to_pointID = "+str(request.to_pointID)+"\n"
                "label = "+str(request.label)+"\n"
                "color_r = "+str(request.color_r)+"\n"
                "color_g = "+str(request.color_g)+"\n"
                "color_b = "+str(request.color_b)+"\n"
                "radius = "+str(request.radius))
        return points_and_lines_pb2.Empty()

    def sendTick(self, request, context):
        print("Got tick message: "+request.message)
        return points_and_lines_pb2.Empty()

try:
    # running the server
    serv = server( futures.ThreadPoolExecutor(2,serverName) )
    points_and_lines_pb2_grpc.add_PointsAndLinesServicer_to_server(IncomingPLProcessor(),serv)
    serv.add_insecure_port('[::]:%d'%serverPort)

    serv.start()
    print("Server ready, and listening for next 120 secs")
    sleep(120)
    serv.stop(5)

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
