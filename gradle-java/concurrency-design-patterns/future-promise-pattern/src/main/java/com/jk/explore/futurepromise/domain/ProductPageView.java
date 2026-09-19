package com.jk.explore.futurepromise.domain;

import java.math.BigDecimal;

/** Everything the product page renders, plus how long assembling it took. */
public record ProductPageView(BigDecimal price, int stock, double rating, long elapsedNanos) {
}
