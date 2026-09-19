package com.jk.explore.servicelocator.pattern;

import com.jk.explore.servicelocator.domain.Notifier;

/** And another. */
public class Auditor {

    public void audit(String event) {
        ServiceLocator.find(Notifier.class).send("audit " + event);
    }
}
