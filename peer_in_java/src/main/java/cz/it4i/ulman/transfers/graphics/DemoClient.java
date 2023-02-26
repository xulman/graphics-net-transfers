package cz.it4i.ulman.transfers.graphics;

import cz.it4i.ulman.transfers.graphics.protocol.BucketsWithGraphics;
import cz.it4i.ulman.transfers.graphics.protocol.ClientToServerGrpc;
import io.grpc.ConnectivityState;
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
		// Access a service running on the local machine on port 9083
		String target = "localhost:9083";

		// Create a communication channel to the server, known as a Channel. Channels are thread-safe
		// and reusable. It is common to create channels at the beginning of your application and reuse
		// them until the application shuts down.
		final ManagedChannel channel = ManagedChannelBuilder.forTarget(target)
			.usePlaintext()
			.build();

		try {
			//advanced comm "channels" for small (blocking) and potentially large (continuous) messages
			final ClientToServerGrpc.ClientToServerBlockingStub commBlocking = ClientToServerGrpc.newBlockingStub(channel);
			final ClientToServerGrpc.ClientToServerStub commContinuous = ClientToServerGrpc.newStub(channel);

			//this obj will be re-used in fact in any outgoing message
			final BucketsWithGraphics.ClientIdentification clientIdentification
				= BucketsWithGraphics.ClientIdentification.newBuilder()
					.setClientName("demo Java client")
					.build();


			//setup and send the introduction message first,
			//this is a mandatory step!
			final BucketsWithGraphics.ClientHello helloMyNameIsMsg = BucketsWithGraphics.ClientHello.newBuilder()
					.setClientID(clientIdentification)
					.setReturnURL("no feedback")
					.build();
			commBlocking.introduceClient(helloMyNameIsMsg);


			//a template data structure for Vector3D (used, e.g., for coordinates of centres of spheres)
			final BucketsWithGraphics.Vector3D.Builder templateSphereCentre = BucketsWithGraphics.Vector3D.newBuilder();
			templateSphereCentre.setX(0.f).setY(1.1f).setZ(1.2f);
			//
			//a template for a full sphere
			final BucketsWithGraphics.SphereParameters.Builder templateSphere
				= BucketsWithGraphics.SphereParameters.newBuilder()
					.setTime(1)
					.setRadius(0.9f)
					.setColorIdx(1);


			StreamObserver<BucketsWithGraphics.BatchOfGraphics> submittingStream = commContinuous.addGraphics(new EmptyIgnoringStreamObservers());
			for (int id = 20; id < 25; ++id) {
				BucketsWithGraphics.BatchOfGraphics.Builder batchBuilder = BucketsWithGraphics.BatchOfGraphics.newBuilder()
						.setClientID(clientIdentification)
						.setCollectionName("default content")
						.setDataName("testing batch id "+id)
						.setDataID(id);

				templateSphereCentre.setX(2.f);
				templateSphereCentre.setZ(id);
				templateSphere.setTime(2);
				templateSphere.setCentre( templateSphereCentre ); //only now the instantiation/building takes place
				batchBuilder.addSpheres( templateSphere );

				templateSphereCentre.setX(3.f);
				templateSphere.setTime(3);
				templateSphere.setCentre( templateSphereCentre ); //only now the instantiation/building takes place
				batchBuilder.addSpheres( templateSphere );

				templateSphereCentre.setX(4.f);
				templateSphere.setTime(4);
				templateSphere.setCentre( templateSphereCentre ); //only now the instantiation/building takes place
				batchBuilder.addSpheres( templateSphere );

				final BucketsWithGraphics.BatchOfGraphics b = batchBuilder.build();
				LOGGER.info("Sending point: ");
				LOGGER.info( b.toString() );
				submittingStream.onNext(b);
			}
			submittingStream.onCompleted();

			System.out.println("Waiting for the delivery before exit");
			closeChannel(channel);
			System.out.println("Exiting...");

		} catch (StatusRuntimeException e) {
			LOGGER.warning("RPC client-side failed, details follow:");
			LOGGER.warning(e.getMessage());
		} finally {
			// ManagedChannels use resources like threads and TCP connections. To prevent leaking these
			// resources the channel should be shut down when it will no longer be used. If it may be used
			// again leave it running.
			//channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
			closeChannel(channel,0,2);
		}
	}


	public static void closeChannel(final ManagedChannel channel)
	throws InterruptedException {
		closeChannel(channel, 15, 2);
	}

	public static void closeChannel(final ManagedChannel channel,
	                                final int halfOfMaxWaitTimeInSeconds,
	                                final int checkingPeriodInSeconds)
	throws InterruptedException {
		//first, make sure the channel describe itself as "READY"
		int timeSpentWaiting = 0;
		while (channel.getState(false) != ConnectivityState.READY && timeSpentWaiting < halfOfMaxWaitTimeInSeconds) {
			timeSpentWaiting += checkingPeriodInSeconds;
			Thread.sleep(checkingPeriodInSeconds * 1000L); //seconds -> milis
		}
		//but even when it claims "READY", it still needs some grace time to finish any commencing transfers;
		//request it to stop whenever it can, then keep asking when it's done
		channel.shutdown();
		timeSpentWaiting = 0;
		while (!channel.isTerminated() && timeSpentWaiting < halfOfMaxWaitTimeInSeconds) {
			timeSpentWaiting += checkingPeriodInSeconds;
			Thread.sleep(checkingPeriodInSeconds * 1000L); //seconds -> milis
		}
		//last few secs extra before a hard stop (if it is still not yet closed gracefully)
		channel.awaitTermination(checkingPeriodInSeconds, TimeUnit.SECONDS);
	}
}
