package cz.it4i.ulman.transfers.graphics;

import cz.it4i.ulman.transfers.graphics.protocol.BucketsWithGraphics;
import cz.it4i.ulman.transfers.graphics.protocol.ServerToClientGrpc;
import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;

import java.io.IOException;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

public class DemoServer extends ServerToClientGrpc.ServerToClientImplBase {
	private static final Logger LOGGER = Logger.getLogger(DemoClient.class.getName());

	@Override
	public void showMessage(BucketsWithGraphics.TextMessage message,
	                        StreamObserver<BucketsWithGraphics.Empty> responseObserver) {
		LOGGER.info("Received a MESSAGE: "+message.getMsg());
		provideEmptyReply(responseObserver);
	}

	@Override
	public void focusEvent(BucketsWithGraphics.ClickedIDs request,
	                       StreamObserver<BucketsWithGraphics.Empty> responseObserver) {
		LOGGER.info("Received a request to FOCUS ids: "+request.getObjIDsList());
		provideEmptyReply(responseObserver);
	}

	@Override
	public void unfocusEvent(BucketsWithGraphics.Empty empty,
	                         StreamObserver<BucketsWithGraphics.Empty> responseObserver) {
		LOGGER.info("Received a request to UNFOCUS everything");
		provideEmptyReply(responseObserver);
	}

	@Override
	public void selectEvent(BucketsWithGraphics.ClickedIDs request,
	                        StreamObserver<BucketsWithGraphics.Empty> responseObserver) {
		LOGGER.info("Received a request to SELECT ids: "+request.getObjIDsList());
		provideEmptyReply(responseObserver);
	}

	@Override
	public void unselectEvent(BucketsWithGraphics.ClickedIDs request,
	                          StreamObserver<BucketsWithGraphics.Empty> responseObserver) {
		LOGGER.info("Received a request to UNSELECT ids: "+request.getObjIDsList());
		provideEmptyReply(responseObserver);
	}

	public static void provideEmptyReply(final StreamObserver<BucketsWithGraphics.Empty> responseObserver) {
		responseObserver.onNext(BucketsWithGraphics.Empty.getDefaultInstance());
		responseObserver.onCompleted();
	}


	public static void main(String[] args) {
		// Create a service running on port 9085
		final int listeningPort = 9085;
		try {
			final DemoServer serviceImpl = new DemoServer();

			final Server trueServer = ServerBuilder
				.forPort(listeningPort)
				.addService(serviceImpl)
				.build();

			trueServer.start();
			LOGGER.info("client's listener started on port "+listeningPort
				+" and will wait 2 minutes");

			trueServer.awaitTermination(2, TimeUnit.MINUTES);
			LOGGER.info("client's listener stopped now");
		} catch (IOException | InterruptedException e) {
			LOGGER.warning("RPC server-side failed, details follow:");
			LOGGER.warning(e.getMessage());
		}
	}
}
