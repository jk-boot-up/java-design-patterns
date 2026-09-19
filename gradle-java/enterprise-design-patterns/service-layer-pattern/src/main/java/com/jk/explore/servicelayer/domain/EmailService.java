package com.jk.explore.servicelayer.domain;

import java.util.ArrayList;
import java.util.List;

/** A fake email service that remembers what it sent. */
public class EmailService {

    private final List<String> sent = new ArrayList<>();

    public void confirm(int customerId, int orderId) {
        sent.add("confirmation of order " + orderId + " to customer " + customerId);
    }

    public int sentCount() {
        return sent.size();
    }
}
