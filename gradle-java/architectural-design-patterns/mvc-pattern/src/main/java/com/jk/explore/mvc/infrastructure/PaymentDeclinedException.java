package com.jk.explore.mvc.infrastructure;

/**
 * The card network said no.
 *
 * <p>This is not the same thing as the shop refusing the order, and it lives in
 * a different package on purpose. "We have only two grinders" is a rule of the
 * shop and belongs to the domain. "The card was declined" is a fact about the
 * outside world arriving through a wire, and belongs down here.
 */
public class PaymentDeclinedException extends RuntimeException {

    public PaymentDeclinedException(String reason) {
        super(reason);
    }
}
