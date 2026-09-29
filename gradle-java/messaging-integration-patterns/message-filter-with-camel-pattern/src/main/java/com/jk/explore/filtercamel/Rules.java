package com.jk.explore.filtercamel;

/**
 * Settings the filter rules read at the moment each order passes, so they can change while routes run.
 */
public final class Rules {

    private long bonusThresholdPence = 5000;

    public long getBonusThresholdPence() {
        return bonusThresholdPence;
    }

    public void setBonusThresholdPence(long pence) {
        this.bonusThresholdPence = pence;
    }
}
