package com.jk.explore.apicomposition;

import java.util.List;

/**
 * The finished page, assembled from three services' answers.
 *
 * The field worth noticing is {@link #missingSections()}. A composed page is not simply
 * present or absent — it can arrive with a hole in it, and the page has to say so. A
 * page that quietly drops the delivery section when Shipping is down looks identical to
 * a page for an order that has not shipped yet, and the shopper cannot tell the
 * difference. Naming the gap is what makes a partial answer honest.
 */
public record OrderDetailsPage(String orderId, List<PageLine> lines, Money total,
                               DeliveryStatus delivery, List<String> missingSections) {

    /** One line as the shopper sees it: the sku's name, not just its code. */
    public record PageLine(String sku, String productName, int quantity, Money lineTotal) {
    }

    public boolean isComplete() {
        return missingSections.isEmpty();
    }
}
