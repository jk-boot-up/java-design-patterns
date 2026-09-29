package com.jk.explore.authorization;

import java.util.Map;
import java.util.Set;

/**
 * Role-based access control (RBAC): each role is granted a set of actions, and nothing else is looked at.
 */
public final class RolePolicy {

    private final Map<String, Set<String>> grants = Map.of(
            "CUSTOMER", Set.of("order:view", "order:cancel"),
            "SUPPORT", Set.of("order:view", "refund:issue"),
            "ADMIN", Set.of("order:view", "order:cancel", "refund:issue"));

    public Decision decide(Request request) {
        boolean allowed = grants.getOrDefault(request.user().role(), Set.of()).contains(request.action());
        return new Decision(allowed, allowed ? "role " + request.user().role() + " has " + request.action()
                : "role " + request.user().role() + " lacks " + request.action());
    }
}
