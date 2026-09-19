package com.jk.explore.retryr4j;

public class CardDeclined extends RuntimeException {
    public CardDeclined() {
        super("card declined");
    }
}
