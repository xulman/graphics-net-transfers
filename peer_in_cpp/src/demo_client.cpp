#include <grpcpp/grpcpp.h>

#include <cassert>
#include <iostream>
#include <memory>
#include <string>

#include "buckets_with_graphics.grpc.pb.h"
#include "buckets_with_graphics.pb.h"

// namespace alias
namespace proto = transfers_graphics_protocol;

// this is where it should be transferred to
const std::string SERVER_URL = "localhost:9083";
const std::string CLIENT_NAME("demo C++ client");

void print_status_err(const grpc::Status& status) {
	assert(!status.ok());

	std::cout << "GRPC failed with code: " << status.error_code()
	          << "\nMessage: " << status.error_message()
	          << "\nDetails: " << status.error_details() << '\n';
}

void print_sphere(const proto::SphereParameters& sph) {
	std::cout << "Sphere: [" << sph.centre().x() << "," << sph.centre().y() << "," << sph.centre().z()
	          << "] @ " << sph.time() << ", radius: " << sph.radius() << '\n';
}

int main() {

	// the transfer itself
	auto stub = proto::ClientToServer::NewStub(
	       grpc::CreateChannel(SERVER_URL, grpc::InsecureChannelCredentials()) );

	//introduce ourselves
	proto::ClientHello helloMyNameIsMsg;
	helloMyNameIsMsg.mutable_clientid()->set_clientname(CLIENT_NAME);
	helloMyNameIsMsg.set_returnurl(""); //means no feedback
	grpc::ClientContext context0;
	proto::Empty empty0;
	stub->introduceClient(&context0, helloMyNameIsMsg, &empty0);

	//sending batches of graphics (collections of spheres)
	grpc::ClientContext context;
	proto::Empty empty;
	std::unique_ptr< grpc::ClientWriter<proto::BatchOfGraphics> > writer( stub->replaceGraphics(&context, &empty) );

	proto::Vector3D refCoord;
	refCoord.set_x(2.0f);
	refCoord.set_y(1.1f);
	refCoord.set_z(20);

	for (int id = 20; id < 25; ++id) {
		auto batch = proto::BatchOfGraphics();
		batch.mutable_clientid()->set_clientname(CLIENT_NAME);
		batch.set_collectionname("Spheres at 2,3; Vectors at 3-6");
		batch.set_dataname( std::string("testing batch id ").append( std::to_string(id) ) );
		batch.set_dataid(id);

		proto::SphereParameters* sph = batch.add_spheres();
		sph->mutable_centre()->CopyFrom(refCoord);
		sph->mutable_centre()->set_x(2.0f);
		sph->mutable_centre()->set_z(float(id));
		sph->set_time(2);
		sph->set_radius(0.9f);
		sph->set_coloridx(1);
		print_sphere(*sph);

		sph = batch.add_spheres();
		sph->mutable_centre()->CopyFrom(refCoord);
		sph->mutable_centre()->set_x(3.0f);
		sph->mutable_centre()->set_z(float(id));
		sph->set_time(3);
		sph->set_radius(0.9f);
		sph->set_coloridx(1);
		print_sphere(*sph);

		proto::VectorParameters* vec = batch.add_vectors();
		vec->mutable_startpos()->CopyFrom(refCoord);
		vec->mutable_endpos()->CopyFrom(refCoord);
		vec->mutable_endpos()->set_x(5*(id-19));
		vec->mutable_endpos()->set_z(23);
		vec->mutable_span()->set_timefrom(3);
		vec->mutable_span()->set_timetill(6.1);
		vec->set_radius(2.2);
		vec->set_coloridx(2);

		if (!writer->Write(batch)) {
			std::cout << "GRPC failed writing a batch of graphics\n";
			break; // broken stream
		}
	}

	writer->WritesDone();
	grpc::Status status = writer->Finish();
	if (!status.ok()) {
		print_status_err(status);
		return 1;
	}


	auto msg = proto::SignedTextMessage();
	msg.mutable_clientid()->set_clientname(CLIENT_NAME);
	msg.mutable_clientmessage()->set_msg("Demo sent you some items.");
	//
	grpc::ClientContext context2;
	grpc::Status status2 = stub->showMessage(&context2, msg, &empty);
	if (!status2.ok()) {
		print_status_err(status2);
		return 1;
	}

	std::cout << "done.\n";
}
