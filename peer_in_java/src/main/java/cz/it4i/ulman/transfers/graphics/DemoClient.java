package cz.it4i.ulman.transfers.graphics;

import cz.it4i.ulman.transfers.graphics.protocol.PointsAndLinesGrpc;
import cz.it4i.ulman.transfers.graphics.protocol.PointsAndLinesOuterClass;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
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
			final PointsAndLinesGrpc.PointsAndLinesBlockingStub comm = PointsAndLinesGrpc.newBlockingStub(channel);

			PointsAndLinesOuterClass.PointAsBall p = PointsAndLinesOuterClass.PointAsBall.newBuilder()
				.setID(20)
				.setX(11.2f)
				.setY(11.3f)
				.setZ(11.4f)
				.setT(3)
				.setLabel("testing point j")
				.setColorR(0.91f)
				.setColorG(0.11f)
				.setColorB(0.06f)
				.setRadius(3.2f)
				.build();
			LOGGER.info("Sending point: ");
			LOGGER.info( p.toString() );
			comm.sendBall( p );

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
