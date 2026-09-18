package com.jk.explore.cleanspring.usecases;

/**
 * The use case's own contract — declared here, in the use case layer,
 * implemented by {@link PlaceOrderInteractor}, and called by a controller
 * in the outer {@code adapters} layer. A controller depends on this
 * interface, never on {@code PlaceOrderInteractor} directly, so the
 * interactor could be replaced without the controller's source changing at
 * all.
 */
public interface PlaceOrderInputBoundary {

    PlaceOrderOutput execute(PlaceOrderInput input);
}
