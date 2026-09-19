package com.jk.explore.featuretoggle;

import java.util.Set;

/** Who a feature is switched on for. */
public sealed interface Rule {

    record Off() implements Rule {
    }

    record On() implements Rule {
    }

    /** On for customers whose number, taken modulo 100, is below the percentage. */
    record Percent(int percent) implements Rule {
    }

    record Only(Set<String> customers) implements Rule {
    }
}
