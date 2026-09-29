package com.jk.explore.authorization;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: checks scattered through the endpoints, roles alone, rules on attributes,
 * one change for every endpoint, and the bill.
 */
public final class AuthorizationDemo {

    static final User ANA = new User("ana", "CUSTOMER");
    static final User SAM = new User("sam", "SUPPORT");
    static final User ALEX = new User("alex", "ADMIN");
    static final Order BENS_ORDER = new Order("ORD-7", "ben", 250.00);

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Every endpoint checks access its own way.");
        out.add("  ana cancels ben's order: " + yesNo(ScatteredChecks.cancelOrder(ANA, BENS_ORDER)));
        out.add("  ana views ben's order:   " + yesNo(ScatteredChecks.viewOrder(ANA, BENS_ORDER))
                + "  <- the view endpoint forgot the owner check");
        out.add("  sam refunds 250.00:      " + yesNo(ScatteredChecks.refund(SAM, BENS_ORDER, 250))
                + "  <- no limit, though support should stop at 100");

        out.add("");
        out.add("TWO. Roles only (RBAC), in one place.");
        RolePolicy roles = new RolePolicy();
        out.add("  ana views ben's order: " + roles.decide(Request.of(ANA, "order:view", BENS_ORDER)));
        out.add("  a role can say \"customers may view orders\", but not \"their own\"");

        out.add("");
        out.add("THREE. Rules on attributes (ABAC): who, which order, how much.");
        Policy policy = Policy.shop();
        out.add("  ana views ben's order: " + policy.decide(Request.of(ANA, "order:view", BENS_ORDER)));
        out.add("  ben views ben's order: " + policy.decide(Request.of(new User("ben", "CUSTOMER"), "order:view", BENS_ORDER)));
        out.add("  sam refunds 80.00:     " + policy.decide(new Request(SAM, "refund:issue", BENS_ORDER, 80)));
        out.add("  sam refunds 250.00:    " + policy.decide(new Request(SAM, "refund:issue", BENS_ORDER, 250)));
        out.add("  alex refunds 250.00:   " + policy.decide(new Request(ALEX, "refund:issue", BENS_ORDER, 250)));

        out.add("");
        out.add("FOUR. Deny by default: an action nobody wrote a rule for.");
        out.add("  alex exports ben's order: " + policy.decide(Request.of(ALEX, "order:export", BENS_ORDER)));
        out.add("  a new endpoint is closed until the policy says otherwise");

        out.add("");
        out.add("FIVE. The bill: every request now asks the policy.");
        out.add("  " + policy.auditLog().size() + " decisions logged, each with its reason; e.g. "
                + policy.auditLog().get(0));
        out.add("  the policy must be fast, thoroughly tested, and kept readable as rules grow");
        return out;
    }

    private static String yesNo(boolean allowed) {
        return allowed ? "ALLOWED" : "denied";
    }

    private AuthorizationDemo() {
    }
}
