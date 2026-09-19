package com.jk.explore.dependencyinjection.app;

import com.jk.explore.dependencyinjection.domain.Notifier;

public class Auditor {

    private final Notifier notifier;

    public Auditor(Notifier notifier) {
        this.notifier = notifier;
    }

    public void audit(String event) {
        notifier.send("audit " + event);
    }
}
