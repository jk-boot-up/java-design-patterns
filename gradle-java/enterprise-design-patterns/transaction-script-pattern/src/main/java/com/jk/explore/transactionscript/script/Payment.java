package com.jk.explore.transactionscript.script;

/** The card network. It can be told to decline the next charge. */
public class Payment {

    private boolean declineNext;

    public void declineNext() {
        declineNext = true;
    }

    public void charge(long pence) {
        if (declineNext) {
            declineNext = false;
            throw new IllegalStateException("card declined");
        }
    }
}
