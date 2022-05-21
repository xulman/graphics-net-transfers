package cz.it4i.ulman.transfers.graphics;

import cz.it4i.ulman.transfers.graphics.protocol.PointsAndLinesGrpc;
import cz.it4i.ulman.transfers.graphics.protocol.PointsAndLinesOuterClass;
import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;

import java.io.IOException;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

public class DemoServer extends PointsAndLinesGrpc.PointsAndLinesImplBase {
	private static final Logger LOGGER = Logger.getLogger(DemoServer.class.getName());

	private Server governingOuterServer;
	public void setGoverningOuterServer(final Server server) {
		governingOuterServer = server;
	}


	@Override
	public StreamObserver<PointsAndLinesOuterClass.PointAsBall>
	sendBall(StreamObserver<PointsAndLinesOuterClass.Empty> responseObserver) {
		return new StreamObserver<PointsAndLinesOuterClass.PointAsBall>() {
			@Override
			public void onNext(PointsAndLinesOuterClass.PointAsBall request) {
				LOGGER.info("Server point:");
				LOGGER.info("ID = "+request.getID()+"\n"+
						"X = "+request.getX()+"\n"+
						"Y = "+request.getY()+"\n"+
						"Z = "+request.getZ()+"\n"+
						"T = "+request.getT()+"\n"+
						"Label = "+request.getLabel()+"\n"+
						"ColorR = "+request.getColorR()+"\n"+
						"ColorG = "+request.getColorG()+"\n"+
						"ColorB = "+request.getColorB()+"\n"+
						"Radius = "+request.getRadius());

				if (request.getLabel().startsWith("stop")) {
					LOGGER.info("Server reads STOP, so stopping...");
					//creates async run that requests stop after handling this request is over
					new Thread(() -> governingOuterServer.shutdownNow()).start();
				}
			}

			@Override
			public void onError(Throwable throwable) {
				LOGGER.warning("Server error when reading points (as balls):");
				LOGGER.warning(throwable.getMessage());
			}

			@Override
			public void onCompleted() {
				PointsAndLinesOuterClass.Empty reply =
						PointsAndLinesOuterClass.Empty.newBuilder().build();
				responseObserver.onNext(reply);
				responseObserver.onCompleted();
			}
		};
	}


	@Override
	public void
	sendTick(PointsAndLinesOuterClass.TickMessage request,
	         StreamObserver<PointsAndLinesOuterClass.Empty> responseObserver) {
		LOGGER.info("Got tick message: "+request.getMessage());

		responseObserver.onNext( PointsAndLinesOuterClass.Empty.newBuilder().build() );
		responseObserver.onCompleted();
	}


	public static void main(String[] args) {
		// Run a service running on the local machine on port 9081
		//NB: local machine is actually an obvious hostname, hence it is not specified anywhere explicitly
		final int serverPort = 9081;

		try {
			final DemoServer trueServer = new DemoServer();

			final Server server = ServerBuilder
				.forPort(serverPort)
				.addService(trueServer)
				.build();
			trueServer.setGoverningOuterServer(server);

			server.start();
			LOGGER.info("server started");
			server.awaitTermination(2, TimeUnit.MINUTES);
			LOGGER.info("server ended");
		} catch (IOException | InterruptedException e) {
			e.printStackTrace();
		}
	}
}
