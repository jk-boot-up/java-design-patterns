package com.jk.explore.chain;

import java.util.Optional;

/**
 * The risk model's opinion — and the link with three possible answers.
 *
 * <p>At 80 or above it rejects. Between 55 and 79 it refers: a person will look
 * at the order. Below 55 it says nothing and the order carries on. A method
 * returning {@code boolean} cannot express that middle case, which is exactly
 * what {@link NaiveScreening} gets wrong.
 */
public final class FraudScoreCheck extends ScreeningHandler {

    private static final int REFER_AT = 55;
    private static final int REJECT_AT = 80;

    @Override
    public String name() {
        return "fraud-score";
    }

    @Override
    protected Optional<Decision> check(CheckoutRequest request) {
        int score = request.fraudScore();
        if (score >= REJECT_AT) {
            return Optional.of(Decision.rejected(name(),
                    "risk score " + score + " is at or above the " + REJECT_AT + " limit"));
        }
        if (score >= REFER_AT) {
            return Optional.of(Decision.referred(name(),
                    "risk score " + score + " is in the " + REFER_AT + "-"
                            + (REJECT_AT - 1) + " review band"));
        }
        return Optional.empty();
    }
}
