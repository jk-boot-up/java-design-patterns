package com.jk.explore.diwithspring.app;

import org.springframework.stereotype.Component;

import com.jk.explore.diwithspring.domain.Notifier;

@Component
public class Auditor {

    private final Notifier notifier;

    public Auditor(Notifier notifier) {
        this.notifier = notifier;
    }

    public void audit(String event) {
        notifier.send("audit " + event);
    }
}
