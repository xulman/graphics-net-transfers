#include <chrono>
#include <grpcpp/grpcpp.h>
#include <iostream>
#include <string>
#include <thread>

#include "points_and_lines.grpc.pb.h"
#include "points_and_lines.pb.h"

// namespace alias
namespace tgp = transfers_graphics_protocol;

// this is where it should be listening at
const std::string SERVER_NAME = "demoServer";
constexpr int SERVER_PORT = 9081;

void print_point(const tgp::PointAsBall& point) {
	std::cout << "PointAsBall structure:"
	          << "\nid: " << point.id() << "\nx: " << point.x()
	          << "\ny: " << point.y() << "\nz: " << point.z()
	          << "\nt: " << point.t() << "\nlabel: " << point.label()
	          << "\ncolor_r: " << point.color_r()
	          << "\ncolor_g: " << point.color_g()
	          << "\ncolor_b: " << point.color_b()
	          << "\nradius: " << point.radius() << '\n';
}

void print_line(const tgp::LineWithPositions& line) {
	std::cout << "LineWithPosition structure:"
	          << "\nid: " << line.id() << "\nfrom_x: " << line.from_x()
	          << "\nfrom_y: " << line.from_y() << "\nfrom_z: " << line.from_z()
	          << "\nto_x: " << line.to_x() << "\nto_y: " << line.to_y()
	          << "\nto_z: " << line.to_z() << "\nlabel: " << line.label()
	          << "\ncolor_r: " << line.color_r()
	          << "\ncolor_g: " << line.color_g()
	          << "\ncolor_b: " << line.color_b()
	          << "\nradius: " << line.radius() << '\n';
}

void print_line(const tgp::LineWithIDs& line) {
	std::cout << "LineWithIDs structure:"
	          << "\nid: " << line.id()
	          << "\nfrom_pointID: " << line.from_pointid()
	          << "\nto_pointID: " << line.to_pointid()
	          << "\nlabel: " << line.label() << "\ncolor_r: " << line.color_r()
	          << "\ncolor_g; " << line.color_g()
	          << "\ncolor_b: " << line.color_b()
	          << "\nradius: " << line.radius() << '\n';
}

class IncomingPLProcessor final : public tgp::PointsAndLines::Service {
  public:
	grpc::Status sendBall(grpc::ServerContext*,
	                      grpc::ServerReader<tgp::PointAsBall>* reader,
	                      tgp::Empty*) override {

		tgp::PointAsBall point;
		while (reader->Read(&point)) {
			std::cout << "Got Ball request with params:\n";
			print_point(point);
			std::cout << '\n';
		}

		return grpc::Status::OK;
	}

	grpc::Status sendEllipsoid(grpc::ServerContext*,
	                           grpc::ServerReader<tgp::PointAsEllipsoid>*,
	                           tgp::Empty*) override {
		std::cout << "Got Ellipsoid request\nAin't touching it now...\n";
		return grpc::Status::OK;
	}

	grpc::Status
	sendLineWithPos(grpc::ServerContext*,
	                grpc::ServerReader<tgp::LineWithPositions>* reader,
	                tgp::Empty*) override {
		tgp::LineWithPositions line;

		while (reader->Read(&line)) {
			std::cout << "Got Line-POS request with params:\n";
			print_line(line);
			std::cout << '\n';
		}

		return grpc::Status::OK;
	}

	grpc::Status sendLineWithIDs(grpc::ServerContext*,
	                             grpc::ServerReader<tgp::LineWithIDs>* reader,
	                             tgp::Empty*) override {
		tgp::LineWithIDs line;

		while (reader->Read(&line)) {
			std::cout << "Got Line-IDs request with params:\n";
			print_line(line);
			std::cout << '\n';
		}

		return grpc::Status::OK;
	}

	grpc::Status sendTick(grpc::ServerContext*,
	                      const tgp::TickMessage* msg,
	                      tgp::Empty*) override {
		std::cout << "Got tick message: " << msg->message() << '\n';
		return grpc::Status::OK;
	}
};

int main() {
	std::string server_address = "0.0.0.0:" + std::to_string(SERVER_PORT);
	IncomingPLProcessor service;

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
