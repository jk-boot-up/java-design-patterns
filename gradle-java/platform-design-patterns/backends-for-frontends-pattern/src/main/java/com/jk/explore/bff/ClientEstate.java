package com.jk.explore.bff;

import java.util.ArrayList;
import java.util.List;

/**
 * The clients the shop has, and what each additional backend actually costs.
 *
 * <p>Two backends is a pattern. Nine is a department. The rule that keeps the count
 * honest is not "one backend per device" and it is not "one per team" -- it is **one
 * per screen that genuinely disagrees about what a product is**. A tablet that shows
 * the same fields as the phone in a wider column does not disagree about anything; it
 * is the same backend and a different stylesheet.
 *
 * <p>The cost of getting that wrong is not paid in servers, which are cheap. It is
 * paid in the row below: every backend is a deployment, an on-call rota, a dependency
 * upgrade every time the shop's services change, and a place a bug can hide.
 */
public final class ClientEstate {

    public record Client(String name, boolean disagreesAboutTheProduct, String reason) {
    }

    private final List<Client> clients = new ArrayList<>();

    public ClientEstate add(String name, boolean disagrees, String reason) {
        clients.add(new Client(name, disagrees, reason));
        return this;
    }

    public List<Client> clients() {
        return List.copyOf(clients);
    }

    /** How many backends this estate justifies. */
    public int backendsJustified() {
        return (int) clients.stream().filter(Client::disagreesAboutTheProduct).count();
    }

    /** How many it would have if every client got one on principle. */
    public int backendsIfOnePerClient() {
        return clients.size();
    }

    /**
     * The recurring cost of a backend, stated as things a team does rather than as
     * money, because a reader can check these against their own week.
     */
    public static List<String> whatEachBackendCosts() {
        return List.of(
                "a pipeline to build and deploy it",
                "a place in the on-call rota",
                "a dependency upgrade every time a shop service changes",
                "one more process to look at during an incident");
    }
}
