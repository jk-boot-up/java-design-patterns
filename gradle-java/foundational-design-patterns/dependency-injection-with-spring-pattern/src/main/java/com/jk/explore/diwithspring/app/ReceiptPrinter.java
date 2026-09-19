package com.jk.explore.diwithspring.app;

import org.springframework.stereotype.Component;

import com.jk.explore.diwithspring.domain.Notifier;

@Component
public class ReceiptPrinter {

    private final Notifier notifier;

    public ReceiptPrinter(Notifier notifier) {
        this.notifier = notifier;
    }

    public void print(String receipt) {
        notifier.send("receipt " + receipt);
    }
}
