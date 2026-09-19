package com.jk.explore.servicelocator.pattern;

import com.jk.explore.servicelocator.domain.Notifier;

/** Another class that needs a collaborator, so it too depends on the locator. */
public class ReceiptPrinter {

    public void print(String receipt) {
        ServiceLocator.find(Notifier.class).send("receipt " + receipt);
    }
}
