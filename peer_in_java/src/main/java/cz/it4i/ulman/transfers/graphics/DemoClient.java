package cz.it4i.ulman.transfers.graphics;

import cz.it4i.ulman.transfers.graphics.protocol.PointsAndLinesGrpc;
import cz.it4i.ulman.transfers.graphics.protocol.PointsAndLinesOuterClass;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import io.grpc.stub.StreamObserver;

import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

public class DemoClient {
	private static final Logger LOGGER = Logger.getLogger(DemoClient.class.getName());

	/**
	 * Greet server. If provided, the first element of {@code args} is the name to use in the
	 * greeting. The second argument is the target server.
	 */
	public static void main(String[] args) throws Exception {
		// Access a service running on the local machine on port 7000
		String target = "localhost:9081";

		// Create a communication channel to the server, known as a Channel. Channels are thread-safe
		// and reusable. It is common to create channels at the beginning of your application and reuse
		// them until the application shuts down.
		final ManagedChannel channel = ManagedChannelBuilder.forTarget(target)
			.usePlaintext()
			.build();

		try {
			final PointsAndLinesGrpc.PointsAndLinesStub comm = PointsAndLinesGrpc.newStub(channel);

			class EmptyIgnoringStreamObservers implements StreamObserver<PointsAndLinesOuterClass.Empty> {
				@Override
				public void onNext(PointsAndLinesOuterClass.Empty empty) {}
				@Override
				public void onError(Throwable throwable) {}
				@Override
				public void onCompleted() { LOGGER.info("got EMPTY response from the server"); }
			}

			StreamObserver<PointsAndLinesOuterClass.PointAsBall> requestStream = comm.sendBall(new EmptyIgnoringStreamObservers());
			for (int id = 20; id < 25; ++id) {
				PointsAndLinesOuterClass.PointAsBall p = PointsAndLinesOuterClass.PointAsBall.newBuilder()
					.setID(id)
					.setX(11.2f +id)
					.setY(11.3f)
					.setZ(11.4f)
					.setT(3)
					.setLabel("testing point "+id)
					.setColorR(0.91f)
					.setColorG(0.11f)
					.setColorB(0.06f)
					.setRadius(3.2f)
					.build();
				LOGGER.info("Sending point: ");
				LOGGER.info( p.toString() );
				requestStream.onNext(p);
			}
			requestStream.onCompleted();

			final PointsAndLinesOuterClass.TickMessage msg = PointsAndLinesOuterClass.TickMessage.newBuilder()
					.setMessage("Java demo client has sent this message.")
					.build();
			comm.sendTick(msg, new EmptyIgnoringStreamObservers());

			System.out.println("Waiting for the delivery before exit");
			Thread.sleep(500);
			System.out.println("Tired of waiting... giving up.");

		} catch (StatusRuntimeException e) {
			LOGGER.warning("RPC client-side failed, details follow:");
			LOGGER.warning(e.getMessage());
		} finally {
			// ManagedChannels use resources like threads and TCP connections. To prevent leaking these
			// resources the channel should be shut down when it will no longer be used. If it may be used
			// again leave it running.
			channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
		}
	}
}
