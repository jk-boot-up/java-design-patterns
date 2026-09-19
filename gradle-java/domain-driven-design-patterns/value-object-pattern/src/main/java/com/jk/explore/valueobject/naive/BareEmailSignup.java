package com.jk.explore.valueobject.naive;

import java.util.ArrayList;
import java.util.List;

/** Emails as plain strings. Two methods check, and the third, written last, does not. */
public class BareEmailSignup {

    private final List<String> stored = new ArrayList<>();

    public void signUp(String email) {
        if (!email.contains("@")) {
            throw new IllegalArgumentException("bad email");
        }
        stored.add(email);
    }

    public void importFromFile(String email) {
        if (!email.contains("@")) {
            throw new IllegalArgumentException("bad email");
        }
        stored.add(email);
    }

    public void importFromPartner(String email) {
        stored.add(email);
    }

    public List<String> stored() {
        return stored;
    }
}
