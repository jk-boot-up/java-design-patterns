package com.jk.explore.currying;

/**
 * How fast: express costs twice as much.
 */
public enum Service {
    STANDARD(1), EXPRESS(2);

    final int multiplier;

    Service(int multiplier) {
        this.multiplier = multiplier;
    }
}
