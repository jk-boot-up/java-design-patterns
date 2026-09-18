package com.jk.explore.bff;

import java.util.List;

/**
 * The whole lesson, in seven acts.
 *
 * <p>Acts 1 to 4 are the problem and the pattern. Acts 5 to 7 are the bill, because a
 * pattern taught without its costs is an advertisement. Every number printed below is
 * computed from the documents the program builds; nothing is a literal typed into a
 * string.
 */
public final class ProductScreenDemo {

    private static final String SKU = "SKU-4417";

    public static void main(String[] args) {
        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
        actSeven();
    }

    /** The phone talks to five services, over the customer's connection. */
    private static void actOne() {
        heading("Act 1 — one product screen, five calls from a phone");
        CallLog log = new CallLog();
        Doc everything = new ChattyPhone(new Shop(log), log).productScreen(SKU);

        System.out.println("  calls from the phone:   " + log.countFrom(CallLog.Origin.DEVICE));
        for (String target : log.targetsFrom(CallLog.Origin.DEVICE)) {
            System.out.println("    → " + target);
        }
        System.out.println("  downloaded:             " + everything.bytes() + " bytes");
        System.out.println("  fields available:       " + everything.paths().size());
        System.out.println("  fields drawn on screen: " + Screens.PHONE.size());
        System.out.println();
        System.out.println("  Five round trips before a single pixel. On a good connection");
        System.out.println("  nobody notices. On a train, each one is a wait of its own, and");
        System.out.println("  they happen one after another because the fifth call needs the");
        System.out.println("  first one's answer to know which product it is asking about.");
    }

    /** One shared endpoint fixes the round trips and cannot fix the shape. */
    private static void actTwo() {
        heading("Act 2 — one shared endpoint for every client");
        CallLog log = new CallLog();
        SharedApi api = new SharedApi(new Shop(log), log);

        Doc union = api.product(SKU);
        System.out.println("  calls from the phone:   " + log.countFrom(CallLog.Origin.DEVICE));
        System.out.println("  downloaded:             " + union.bytes() + " bytes");

        Doc drawn = union.select(Screens.PHONE_ON_SHARED_API);
        int wasted = union.bytes() - drawn.bytes();
        int percent = (wasted * 100) / union.bytes();
        System.out.println("  of that, actually drawn: " + drawn.bytes() + " bytes");
        System.out.println("  thrown away on arrival:  " + wasted + " bytes (" + percent + "%)");
        System.out.println();
        System.out.println("  Now the obvious fix — ask for only the fields you want:");
        Doc trimmed = api.product(SKU, Screens.PHONE_ON_SHARED_API);
        System.out.println("    GET /api/products/4417?fields=… → " + trimmed.bytes() + " bytes");
        System.out.println();
        System.out.println("  That works, and it is worth saying so. The size problem is");
        System.out.println("  solved. What is not solved is the next request the phone team");
        System.out.println("  makes: one line of text that says when the parcel arrives,");
        System.out.println("  joined across stock, delivery and the clock.");
        System.out.println("    delivery sentence: " + SharedApi.joinedDelivery());
        System.out.println();
        System.out.println("  A new field on a shared endpoint is a change to a document");
        System.out.println("  every other client also receives, so it joins a queue behind");
        System.out.println("  work that has nothing to do with the phone. The phone team");
        System.out.println("  could have written it in an afternoon, and waits five weeks.");
    }

    /** Two backends, two shapes, same shop. */
    private static void actThree() {
        heading("Act 3 — one backend per frontend");
        CallLog phoneLog = new CallLog();
        ClientBackend mobile = new MobileBff(new Shop(phoneLog), phoneLog);
        Doc phoneScreen = mobile.productScreen(SKU);

        CallLog webLog = new CallLog();
        ClientBackend web = new WebBff(new Shop(webLog), webLog);
        Doc webPage = web.productScreen(SKU);

        System.out.println("  " + mobile.client() + " asks its own backend, and is sent:");
        System.out.println(indent(phoneScreen.pretty()));
        System.out.println();
        System.out.println("  " + web.client() + " asks its own backend, and is sent " + webPage.names().size()
                + " fields including the");
        System.out.println("  description, the specification, five images and three reviews.");
        System.out.println();
        System.out.println("  Same five services underneath. Neither backend has data the");
        System.out.println("  other cannot get. What differs is the shape, and the shape is");
        System.out.println("  now owned by the team that owns the screen.");
        System.out.println();
        System.out.println("  Read the phone's price field again: it is the string \"" + phoneScreen.get("price") + "\".");
        System.out.println("  The shop's pricing service returned the number 4799. Somebody has");
        System.out.println("  to turn one into the other, and doing it here means it is done");
        System.out.println("  once, in a process that can be fixed this afternoon — not in an");
        System.out.println("  app that customers will still be running in two years.");
    }

    /** The numbers, side by side. */
    private static void actFour() {
        heading("Act 4 — the same product, three ways");

        CallLog chattyLog = new CallLog();
        Doc chatty = new ChattyPhone(new Shop(chattyLog), chattyLog).productScreen(SKU);

        CallLog sharedLog = new CallLog();
        Doc shared = new SharedApi(new Shop(sharedLog), sharedLog).product(SKU);

        CallLog bffLog = new CallLog();
        Doc bff = new MobileBff(new Shop(bffLog), bffLog).productScreen(SKU);

        System.out.printf("  %-26s %10s %8s %8s%n",
                "design", "bytes", "device", "internal");
        row("five calls from the phone", chatty, chattyLog);
        row("one shared endpoint", shared, sharedLog);
        row("a backend for the phone", bff, bffLog);
        System.out.println();
        int saved = 100 - (bff.bytes() * 100 / shared.bytes());
        System.out.println("  The phone's backend sends " + saved + "% less than the shared endpoint");
        System.out.println("  and asks the customer's connection for one round trip instead of");
        System.out.println("  five. The internal column barely moves — the work did not go");
        System.out.println("  away, it moved onto a network that costs nothing.");
        System.out.println();
        System.out.println("  And the field that started the argument:");
        System.out.println("    delivery: " + bff.get("delivery"));
    }

    private static void row(String label, Doc response, CallLog log) {
        System.out.printf("  %-26s %10d %8d %8d%n",
                label,
                response.bytes(),
                log.countFrom(CallLog.Origin.DEVICE),
                log.countFrom(CallLog.Origin.INTERNAL));
    }

    /** The bill, part one: the same rule, copied, and then changed in one place. */
    private static void actFive() {
        heading("Act 5 — the bill: two backends, one rule, two answers");
        CallLog log = new CallLog();
        Shop shop = new Shop(log);

        WebBff web = new WebBff(shop, log, SavingRules.current());
        MobileBff phone = new MobileBff(shop, log, SavingRules.copiedBeforeTheReview());

        System.out.println("  The shop's pricing service says the higher price has only been");
        System.out.println("  in force for eleven days, which is not long enough to advertise");
        System.out.println("  the difference as a saving. Both backends are told this.");
        System.out.println();
        System.out.println("  desktop store says:  " + describe(web.savingLabel(SKU)));
        System.out.println("  phone app says:      " + describe(phone.savingLabel(SKU)));
        System.out.println();
        System.out.println("  Same product, same price, same second, and one of those two");
        System.out.println("  screens is making a claim the shop is not allowed to make. The");
        System.out.println("  phone is running a copy of the discount rule taken before the");
        System.out.println("  pricing review, and the review added a condition the copy never");
        System.out.println("  heard about. Nothing throws. Nothing is logged. The only person");
        System.out.println("  who can see the difference is a customer with both screens open.");
        System.out.println();
        System.out.println("  Nothing about that copy is careless. It was right when it was");
        System.out.println("  written, it is well named, and its tests pass. It is wrong only");
        System.out.println("  in relation to a decision made months later by people with no");
        System.out.println("  reason to know a second copy existed.");
        System.out.println();
        System.out.println("  This is the real cost of the pattern, and it is not bytes. Two");
        System.out.println("  backends means two places for shared logic to live, and shared");
        System.out.println("  logic put in both of them will diverge. The rule: a backend for");
        System.out.println("  a frontend may hold the *shape*, and anything the shop would");
        System.out.println("  still believe with every client switched off belongs behind it.");
    }

    /** The bill, part two: the backend that quietly turns into a gateway. */
    private static void actSix() {
        heading("Act 6 — the bill: where the shared jobs go");
        int backends = 2;
        System.out.println("  Every request needs these done, whoever sent it:");
        for (String job : CrossCutting.JOBS) {
            System.out.println("    · " + job);
        }
        System.out.println();
        System.out.println("  each backend doing it itself: "
                + CrossCutting.copiesWhenEachBackendDoesIt(backends) + " copies across " + backends + " backends");
        System.out.println("  a gateway in front:           "
                + CrossCutting.copiesBehindAGateway() + " copies, whatever the number of backends");
        System.out.println();
        System.out.println("  The nearest place to put authentication is inside whichever");
        System.out.println("  backend you happen to be editing, and doing that once per");
        System.out.println("  backend puts the shop back where it was before it had a gateway.");
        System.out.println();
        System.out.println("  The line is one question. Does the code answer \"what does this");
        System.out.println("  screen need?\" — then it belongs in a backend for that frontend.");
        System.out.println("  Does it answer \"is this request allowed in at all?\" — then it");
        System.out.println("  belongs in front of all of them. A gateway is about entry. A");
        System.out.println("  backend for a frontend is about shape. They are neighbours, and");
        System.out.println("  they are not the same pattern.");
    }

    /** The bill, part three: how many of these a shop should have. */
    private static void actSeven() {
        heading("Act 7 — the bill: how many backends is too many");
        ClientEstate estate = new ClientEstate()
                .add("phone app", true, "six fields, one sentence, a four-inch screen")
                .add("desktop store", true, "description, specification, five images, reviews")
                .add("tablet app", false, "the phone's fields in a wider column")
                .add("smart TV app", true, "no keyboard, so no search, and pictures do the work")
                .add("in-store kiosk", false, "the desktop page with the basket hidden")
                .add("partner feed", false, "not a screen at all — a nightly file");

        for (ClientEstate.Client client : estate.clients()) {
            System.out.printf("  %-16s %-18s %s%n",
                    client.name(),
                    client.disagreesAboutTheProduct() ? "own backend" : "shares one",
                    client.reason());
        }
        System.out.println();
        System.out.println("  one per client:            " + estate.backendsIfOnePerClient() + " backends");
        System.out.println("  one per genuine disagreement: " + estate.backendsJustified() + " backends");
        System.out.println();
        System.out.println("  The test is not the device and it is not the team. It is whether");
        System.out.println("  the client disagrees about what a product *is*. A tablet showing");
        System.out.println("  the phone's fields in a wider column disagrees about nothing, so");
        System.out.println("  it is the same backend and a different stylesheet.");
        System.out.println();
        System.out.println("  Each extra backend costs, every week, for as long as it exists:");
        for (String cost : ClientEstate.whatEachBackendCosts()) {
            System.out.println("    · " + cost);
        }
        System.out.println();
        System.out.println("  Two backends is a pattern. Nine is a department.");
    }

    /** An empty label is a decision, not a missing value, so it gets printed as one. */
    private static String describe(String label) {
        return label.isEmpty() ? "(nothing — no saving may be claimed for this price)" : label;
    }

    private static void heading(String title) {
        System.out.println();
        System.out.println("=".repeat(72));
        System.out.println(title);
        System.out.println("=".repeat(72));
    }

    private static String indent(String block) {
        return List.of(block.split("\n")).stream()
                .map(line -> "    " + line)
                .reduce((a, b) -> a + "\n" + b)
                .orElse("");
    }

    private ProductScreenDemo() {
    }
}
