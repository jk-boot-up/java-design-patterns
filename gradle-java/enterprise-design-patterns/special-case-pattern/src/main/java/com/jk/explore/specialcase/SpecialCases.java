package com.jk.explore.specialcase;

/**
 * The pattern: customers for the special situations, each answering every question sensibly instead of being null.
 */
public final class SpecialCases {

    /** Someone checking out without an account: no points, no discount, no marketing. */
    public record Guest() implements Customer {
        public String name() {
            return "Guest";
        }

        public long points() {
            return 0;
        }

        public void earnPoints(long spentPence) {
            // guests do not collect points
        }

        public int discountPercent() {
            return 0;
        }

        public boolean canReceiveMarketing() {
            return false;
        }
    }

    /** An order whose account no longer exists, for example after it was deleted. */
    public record Unknown(String formerId) implements Customer {
        public String name() {
            return "Former customer";
        }

        public long points() {
            return 0;
        }

        public void earnPoints(long spentPence) {
            // nobody to give them to
        }

        public int discountPercent() {
            return 0;
        }

        public boolean canReceiveMarketing() {
            return false;
        }
    }

    private SpecialCases() {
    }
}
