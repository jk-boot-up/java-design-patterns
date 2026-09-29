package com.jk.explore.statetable;

/**
 * What can happen to an order: each one may move it to another status.
 */
public enum Action {
    PAY, SHIP, DELIVER, CANCEL, REFUND, RETURN
}
