#include <chrono>
#include <grpcpp/grpcpp.h>
#include <iostream>
#include <string>
#include <thread>
#include <sstream>

#include "buckets_with_graphics.grpc.pb.h"
#include "buckets_with_graphics.pb.h"

// namespace alias
namespace proto = transfers_graphics_protocol;

// this is where it should be listening at
constexpr int SERVER_PORT = 9083;

std::string print_coord(const proto::Vector3D& vec) {
    std::ostringstream oss;
    oss << "[" << vec.x() << ", " << vec.y() << ", " << vec.z() << "]";
    return oss.str();
}

class IncomingGraphicsProcessor final : public proto::ClientToServer::Service {
  public:
    grpc::Status introduceClient(grpc::ServerContext*,
                                 const proto::ClientHello* request,
                                 proto::Empty*) override {

        std::cout << "Server registers '" << request->clientid().clientname() << "'\n";
        if (request->returnurl().empty())
            std::cout << "  -> with NO callback\n";
        else
            std::cout << "  -> with callback to >>" << request->returnurl() << "<<\n";

        return grpc::Status::OK;
    }

	grpc::Status addGraphics(grpc::ServerContext*,
	                      grpc::ServerReader<proto::BatchOfGraphics>* reader,
	                      proto::Empty*) override {

		proto::BatchOfGraphics batch;
		while (reader->Read(&batch)) {
		    std::cout << "Incoming communication from '" << batch.clientid().clientname()
                      << "' to display into the collection '" << batch.collectionname() << "'\n";
            std::cout << "Creating object '" << batch.dataname()
                      << "' (ID: " << batch.dataid() << ") with "
                      << batch.spheres_size() << " spheres, "
                      << batch.lines_size() << " lines and "
                      << batch.vectors_size() << " vectors.\n";

            for (const auto & sph : batch.spheres()) {
                std::cout << "Sphere at " << print_coord(sph.centre())
                          << "@" << sph.time() << ", radius=" << sph.radius() << "\n";
            }
            for (const auto & line : batch.lines()) {
               std::cout << "Line from " << print_coord(line.startpos())
                         << " to " << print_coord(line.endpos())
                         << "@" << line.time() << ", radius=" << line.radius() << "\n";
            }
            for (const auto & vec : batch.vectors()) {
                std::cout << "Vector from " << print_coord(vec.startpos())
                          << " to " << print_coord(vec.endpos())
                          << "@" << vec.time() << ", radius=" << vec.radius() << "\n";
            }
		}

		return grpc::Status::OK;
	}


    grpc::Status showMessage(grpc::ServerContext*,
                             const proto::SignedTextMessage* msg,
                             proto::Empty*) override {

        std::cout << "Message from '" << msg->clientid().clientname() << "': "
                  << msg->clientmessage().msg() << "\n";

        return grpc::Status::OK;
    }
};

int main() {
	const std::string server_address = "0.0.0.0:" + std::to_string(SERVER_PORT);
	IncomingGraphicsProcessor service;

	grpc::ServerBuilder builder;
	builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
	builder.RegisterService(&service);

	std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
	std::cout << "Server listening on: " << server_address
	          << " for next 120 secs\n";

	std::this_thread::sleep_for(std::chrono::seconds(120));
	server->Shutdown();

	std::cout << "Done.\n";
}
