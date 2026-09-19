package com.jk.explore.dependencyinjection.app;

import com.jk.explore.dependencyinjection.domain.Notifier;

public class ReceiptPrinter {

    private final Notifier notifier;

    public ReceiptPrinter(Notifier notifier) {
        this.notifier = notifier;
    }

    public void print(String receipt) {
        notifier.send("receipt " + receipt);
    }
}
