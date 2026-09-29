package com.jk.explore.blackboard;

import java.util.List;
import java.util.Map;

/**
 * The shop's fraud checks, each written without knowing the others exist.
 */
public final class Checks {

    /** A small check built from its pieces: name, cost, what it needs, what it posts, and what it does. */
    record Check(String name, int costMs, List<String> needs, String posts, java.util.function.Consumer<Blackboard> body)
            implements KnowledgeSource {

        @Override
        public boolean ready(Blackboard b) {
            return needs.stream().allMatch(b::has) && !b.has(posts);
        }

        @Override
        public void contribute(Blackboard b) {
            body.accept(b);
        }
    }

    static final Map<String, String> CARD_COUNTRY = Map.of("4000-GB", "GB", "4000-FR", "FR");
    static final Map<String, String> IP_COUNTRY = Map.of("81.2.69.1", "GB", "95.31.18.9", "RU");

    public static KnowledgeSource cardCountry() {
        return new Check("card country", 20, List.of("card"), "cardCountry",
                b -> b.post("card country", "cardCountry", CARD_COUNTRY.getOrDefault(b.get("card"), "??")));
    }

    public static KnowledgeSource ipCountry() {
        return new Check("IP country", 30, List.of("ip"), "ipCountry",
                b -> b.post("IP country", "ipCountry", IP_COUNTRY.getOrDefault(b.get("ip"), "??")));
    }

    public static KnowledgeSource countryMatch() {
        return new Check("country match", 1, List.of("cardCountry", "ipCountry"), "countriesChecked", b -> {
            b.post("country match", "countriesChecked", "yes");
            if (!b.get("cardCountry").equals(b.get("ipCountry"))) {
                b.addRisk("country match", 40, "card from " + b.get("cardCountry") + ", shopper in " + b.get("ipCountry"));
            }
        });
    }

    public static KnowledgeSource velocity() {
        return new Check("order velocity", 50, List.of("ordersLastHour"), "velocityChecked", b -> {
            b.post("order velocity", "velocityChecked", "yes");
            if (Integer.parseInt(b.get("ordersLastHour")) > 3) {
                b.addRisk("order velocity", 30, b.get("ordersLastHour") + " orders in the last hour");
            }
        });
    }

    public static KnowledgeSource orderValue() {
        return new Check("order value", 1, List.of("totalPence"), "valueChecked", b -> {
            b.post("order value", "valueChecked", "yes");
            if (Long.parseLong(b.get("totalPence")) > 50000) {
                b.addRisk("order value", 20, "over £500");
            }
        });
    }

    public static KnowledgeSource deviceFingerprint() {
        return new Check("device fingerprint", 800, List.of("device"), "deviceChecked", b -> {
            b.post("device fingerprint", "deviceChecked", "yes");
            if (b.get("device").startsWith("emulator")) {
                b.addRisk("device fingerprint", 25, "an emulator, not a phone");
            }
        });
    }

    /** Added later, in act four, without touching any other check. */
    public static KnowledgeSource giftCards() {
        return new Check("gift cards", 1, List.of("items"), "giftCardsChecked", b -> {
            b.post("gift cards", "giftCardsChecked", "yes");
            if (b.get("items").contains("gift card") && Long.parseLong(b.get("totalPence")) > 20000) {
                b.addRisk("gift cards", 60, "over £200 of gift cards");
            }
        });
    }

    public static List<KnowledgeSource> standard() {
        return List.of(cardCountry(), ipCountry(), countryMatch(), velocity(), orderValue(), deviceFingerprint());
    }

    private Checks() {
    }
}
