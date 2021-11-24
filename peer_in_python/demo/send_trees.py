from grpc import insecure_channel, RpcError
from copy import copy
import points_and_lines_pb2
import points_and_lines_pb2_grpc

# this is where it should be transfered to
serverURL = "localhost:9081"

sourceData = "data/small_tree.dat"
#sourceData = "data/medium_tree.dat"
#sourceData = "data/large_tree.dat"

# skeleton structures whos copies are to be transfered over
p = points_and_lines_pb2.PointAsBall()
li = points_and_lines_pb2.LineWithIDs()
lp = points_and_lines_pb2.LineWithPositions()
m = points_and_lines_pb2.TickMessage()

ps = list()
lis = list()
lps = list()

try:
    comm = points_and_lines_pb2_grpc.PointsAndLinesStub( insecure_channel(serverURL) )

    data = open(sourceData,"r")
    datum = data.readline()
    while datum is not None and len(datum) > 0:
        elems = datum.split(";")
        datum = data.readline()

        if elems[0] == "BALL":
            p.ID = int(elems[1])
            p.x = float(elems[2])
            p.y = float(elems[3])
            p.z = float(elems[4])
            p.t = int(elems[5])
            p.label = elems[6]
            p.color_r = float(elems[7])
            p.color_g = float(elems[8])
            p.color_b = float(elems[9])
            p.radius = float(elems[10])
            ps.append(copy(p))

        elif elems[0] == "IDLINE":
            li.ID = int(elems[1])
            li.from_pointID = int(elems[2])
            li.to_pointID = int(elems[3])
            li.label = elems[4]
            li.color_r = float(elems[5])
            li.color_g = float(elems[6])
            li.color_b = float(elems[7])
            li.radius = float(elems[8])
            lis.append(copy(li))

        elif elems[0] == "POSLINE":
            lp.ID = int(elems[1])
            lp.from_x = float(elems[2])
            lp.from_y = float(elems[3])
            lp.from_z = float(elems[4])
            lp.to_x = float(elems[5])
            lp.to_y = float(elems[6])
            lp.to_z = float(elems[7])
            lp.label = elems[8]
            lp.color_r = float(elems[9])
            lp.color_g = float(elems[10])
            lp.color_b = float(elems[11])
            lp.radius = float(elems[12])
            lps.append(copy(lp))

        elif elems[0] == "HEADER":
            m.message = elems[1].rstrip()

        else:
            print("Don't know how to process this line: "+datum)
    data.close()

    print(f"Going to send data pack for >>{m.message}<< that"\
          f" consists of {len(ps)}, {len(lis)} and {len(lps)}"\
          " balls, lineIDs and linePOSs, respectively.")
    comm.sendTick(m)
    comm.sendBall( iter(ps) )
    comm.sendLineWithIDs( iter(lis) )
    comm.sendLineWithPos( iter(lps) )

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

print("Transfer is finished.")
