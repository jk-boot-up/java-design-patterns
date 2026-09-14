package com.jk.explore.bulkhead;

import java.util.concurrent.Callable;

/**
 * The nightly job that imports the supplier's catalogue.
 *
 * Nobody is waiting for it. It is not urgent, it is not customer-facing, and if it
 * finished an hour late nothing bad would happen. It also calls a partner API that is
 * occasionally very slow — which, in a shop where everything shares one pool of
 * threads, is enough to stop the shop selling.
 *
 * <p>Here the slowness is a {@link Gate} rather than a real partner. A job waiting at
 * a closed gate holds its thread exactly the way a job waiting on a slow network
 * does.
 */
public final class SupplierFeed {

    private final Gate partnerApi;

    public SupplierFeed(Gate partnerApi) {
        this.partnerApi = partnerApi;
    }

    /** One batch of products from the supplier, once the partner answers. */
    public Callable<String> importBatch(int batchNumber) {
        return () -> {
            partnerApi.awaitOpen();
            return "batch " + batchNumber + " imported";
        };
    }
}
