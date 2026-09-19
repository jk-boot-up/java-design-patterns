package com.jk.explore.proxyspring;

import org.springframework.stereotype.Component;

/** Who is calling. A plain holder, set by the demo and the tests. */
@Component
public class Session {

    private volatile Role role = Role.SHOPPER;

    public Role role() {
        return role;
    }

    public void actAs(Role role) {
        this.role = role;
    }
}
