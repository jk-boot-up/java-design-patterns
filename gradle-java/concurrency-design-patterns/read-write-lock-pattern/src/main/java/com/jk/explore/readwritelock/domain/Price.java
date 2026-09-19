package com.jk.explore.readwritelock.domain;

import java.math.BigDecimal;

/**
 * A catalogue price: an amount in a currency. Two fields that must change
 * together — a price update that changes the amount but not the currency,
 * or the other way round, is not a smaller update, it is a wrong one.
 */
public record Price(BigDecimal amount, String currency) {
}
