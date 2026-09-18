package com.jk.explore.bff;

/**
 * A backend that exists to serve exactly one frontend.
 *
 * <p>The interface is one method, and that is the whole pattern: something that takes
 * a product and returns a document. What makes it the pattern rather than a shared
 * endpoint is not in this file at all. It is that there is more than one implementation
 * of it, that each one is free to answer differently, and that each one is changed by
 * the team that owns the screen it feeds.
 *
 * <p>The name is worth reading literally. A backend *for* a frontend: it is not a
 * layer the shop provides and clients consume, it is a part of the client that happens
 * to run in the data centre. If you cannot say which single screen a backend belongs
 * to, it is not one of these.
 */
public interface ClientBackend {

    /** Which frontend this backend belongs to. */
    String client();

    /** One call, one document, shaped for that frontend's screen. */
    Doc productScreen(String sku);
}
