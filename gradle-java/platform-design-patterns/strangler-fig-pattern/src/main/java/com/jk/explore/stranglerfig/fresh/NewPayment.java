package com.jk.explore.stranglerfig.fresh;

import com.jk.explore.stranglerfig.domain.Payer;

/** The rewritten payment service. {@code misbehaving} injects the Monday fault: it declines large payments. */
public class NewPayment implements Payer {

    private boolean misbehaving;
    private int charges;

    public void misbehave(boolean on) {
        this.misbehaving = on;
    }

    @Override
    public String charge(long totalPence) {
        if (misbehaving && totalPence > 20_000) {
            return null;
        }
        return "N-" + (++charges);
    }
}
