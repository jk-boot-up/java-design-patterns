package com.jk.explore.chainspring;

import java.util.Optional;

/** One link. Empty means no opinion, pass it on. A present answer stops the chain. */
public interface ScreeningCheck {

    String name();

    Optional<Outcome> check(CheckoutRequest request, StringBuilder reason);
}
