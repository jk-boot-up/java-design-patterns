package com.jk.explore.callback;

/** The version where the caller asks, then asks again and again until the answer is there. */
public class WaitingGateway {

    public static class Handle {
        private final int readyOnPoll;
        private int polls;

        Handle(int readyOnPoll) {
            this.readyOnPoll = readyOnPoll;
        }

        public boolean isDone() {
            polls++;
            return polls >= readyOnPoll;
        }

        public int polls() {
            return polls;
        }
    }

    public Handle charge(String orderId, int answerArrivesOnPoll) {
        return new Handle(answerArrivesOnPoll);
    }
}
