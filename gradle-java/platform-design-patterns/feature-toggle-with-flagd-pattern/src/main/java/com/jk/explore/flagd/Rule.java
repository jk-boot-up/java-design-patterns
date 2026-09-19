package com.jk.explore.flagd;

import java.util.List;

/** Who a flag is on for, written as flagd reads it. */
public sealed interface Rule {

    /** The flag's JSON body: its variants, default and targeting. */
    String json();

    record Off() implements Rule {
        public String json() {
            return "{\"state\":\"ENABLED\",\"variants\":{\"on\":true,\"off\":false},\"defaultVariant\":\"off\"}";
        }
    }

    record On() implements Rule {
        public String json() {
            return "{\"state\":\"ENABLED\",\"variants\":{\"on\":true,\"off\":false},\"defaultVariant\":\"on\"}";
        }
    }

    /** flagd hashes the flag name and the customer, so the same customers are picked every time. */
    record Percent(int percent) implements Rule {
        public String json() {
            return "{\"state\":\"ENABLED\",\"variants\":{\"on\":true,\"off\":false},\"defaultVariant\":\"off\","
                    + "\"targeting\":{\"fractional\":[[\"on\"," + percent + "],[\"off\"," + (100 - percent) + "]]}}";
        }
    }

    record Only(List<String> customers) implements Rule {
        public String json() {
            StringBuilder names = new StringBuilder();
            for (String c : customers) {
                names.append(names.length() == 0 ? "" : ",").append('"').append(c).append('"');
            }
            return "{\"state\":\"ENABLED\",\"variants\":{\"on\":true,\"off\":false},\"defaultVariant\":\"off\","
                    + "\"targeting\":{\"if\":[{\"in\":[{\"var\":\"targetingKey\"},[" + names + "]]},\"on\",\"off\"]}}";
        }
    }
}
