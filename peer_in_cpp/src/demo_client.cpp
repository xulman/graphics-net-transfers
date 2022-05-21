#include <grpcpp/grpcpp.h>

#include <cassert>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include "points_and_lines.grpc.pb.h"
#include "points_and_lines.pb.h"

// this is where it should be transfered to
const std::string SERVER_URL = "localhost:9081";

// namespace alias
namespace tgp = transfers_graphics_protocol;

void print_status_err(const grpc::Status& status) {
	assert(!status.ok());

	std::cout << "GRPC failed with code: " << status.error_code()
	          << "\nMessage: " << status.error_message()
	          << "\nDetails: " << status.error_details() << '\n';
}

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

int main() {
	// a test point to be transfered over
	auto point = tgp::PointAsBall();

	point.set_id(10);
	point.set_x(1.2);
	point.set_y(1.3);
	point.set_z(1.4);
	point.set_t(2);
	point.set_label("testing point");
	point.set_color_r(0.9);
	point.set_color_g(0.1);
	point.set_color_b(0.05);
	point.set_radius(3.1);

	// the transfer itself

	auto stub = tgp::PointsAndLines::NewStub(
	    grpc::CreateChannel(SERVER_URL, grpc::InsecureChannelCredentials()));

	std::vector<tgp::PointAsBall> points;
	for (int i = 0; i < 5; ++i) {
		point.set_x((i % 50) * 5);
		point.set_y((i / 50) * 5);
		point.set_id(i + 10);
		point.set_label("testing point #" + std::to_string(point.id()));

		points.push_back(point);
	}

	grpc::ClientContext context;
	tgp::Empty empty;

	std::unique_ptr<grpc::ClientWriter<tgp::PointAsBall>> writer(
	    stub->sendBall(&context, &empty));

	for (const auto& p : points) {
		print_point(p);
		std::cout << '\n';
		if (!writer->Write(p))
			break; // broken stream
	}

	writer->WritesDone();
	grpc::Status status = writer->Finish();

	if (!status.ok()) {
		print_status_err(status);
		return 1;
	}

	auto msg = tgp::TickMessage();
	msg.set_message("Demo sent you " + std::to_string(points.size()) +
	                " items");

	grpc::ClientContext context2;
	grpc::Status status2 = stub->sendTick(&context2, msg, &empty);
	if (!status2.ok()) {
		print_status_err(status2);
		return 1;
	}

	std::cout << "done.\n";
}
