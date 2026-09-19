package com.jk.explore.servicelayer.domain;

import java.util.List;

/** What a customer, or a support agent, asks for. */
public record OrderRequest(int customerId, List<CartLine> lines) {
}
