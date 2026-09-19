package com.jk.explore.registryspring.domain;

/** A second Notifier, so asking the registry for "the" Notifier is ambiguous. Not a component: only one act registers it. */
public class SmsNotifier implements Notifier {

    @Override
    public void send(String message) {
    }
}
