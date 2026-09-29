package com.jk.explore.gatewayoffloading;

/**
 * A back-end service of the online store.
 */
public interface Service {

    Response handle(Request request);
}
