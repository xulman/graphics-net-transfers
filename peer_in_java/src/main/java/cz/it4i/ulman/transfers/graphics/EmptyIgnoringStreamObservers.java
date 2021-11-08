package cz.it4i.ulman.transfers.graphics;

import io.grpc.stub.StreamObserver;
import cz.it4i.ulman.transfers.graphics.protocol.PointsAndLinesOuterClass;

public class EmptyIgnoringStreamObservers implements StreamObserver<PointsAndLinesOuterClass.Empty> {
	@Override
	public void onNext(PointsAndLinesOuterClass.Empty empty) { /* EMPTY */ }

	@Override
	public void onError(Throwable throwable) { /* EMPTY */ }

	@Override
	public void onCompleted() { /* EMPTY */ }
}