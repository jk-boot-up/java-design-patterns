package com.jk.explore.authorization;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;

/**
 * The pattern: every access decision is made here, from rules that can look at the user, the order and the amount
 * (attribute-based access control, ABAC). Anything no rule allows is denied.
 */
public final class Policy {

    private final List<Rule> rules = new ArrayList<>();
    private final List<String> auditLog = new ArrayList<>();

    public Policy allow(String action, String description, Predicate<Request> condition) {
        rules.add(new Rule(action, description, condition));
        return this;
    }

    public Decision decide(Request request) {
        Decision decision = rules.stream()
                .filter(r -> r.action().equals(request.action()) && r.condition().test(request))
                .findFirst()
                .map(r -> new Decision(true, r.description()))
                .orElse(new Decision(false, "no rule allows it"));
        auditLog.add(request.user().name() + " " + request.action() + " " + request.order().id() + ": " + decision);
        return decision;
    }

    public List<String> auditLog() {
        return auditLog;
    }

    /** The store's policy, all in one place. */
    public static Policy shop() {
        return new Policy()
                .allow("order:view", "owner", r -> r.user().name().equals(r.order().owner()))
                .allow("order:view", "support staff", r -> r.user().role().equals("SUPPORT"))
                .allow("order:view", "admin", r -> r.user().role().equals("ADMIN"))
                .allow("order:cancel", "owner", r -> r.user().name().equals(r.order().owner()))
                .allow("order:cancel", "admin", r -> r.user().role().equals("ADMIN"))
                .allow("refund:issue", "support, up to 100", r -> r.user().role().equals("SUPPORT") && r.amount() <= 100)
                .allow("refund:issue", "admin", r -> r.user().role().equals("ADMIN"));
    }
}
