package com.jk.explore.leaderfollowers;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class LeaderFollowersTest {

    @Test
    void everyMessageHandledByTheThreadThatReceivedIt() throws Exception {
        LeaderFollowers lf = new LeaderFollowers(LeaderFollowersDemo.messages(), 3);
        lf.runUntilStopped();
        assertEquals(20, lf.record().entries().size());
        assertEquals(20, lf.record().sameThread());
    }

    @Test
    void onlyOneThreadWaitsForMessagesAtATime() throws Exception {
        LeaderFollowers lf = new LeaderFollowers(LeaderFollowersDemo.messages(), 4);
        lf.runUntilStopped();
        assertEquals(1, lf.mostWaitingAtOnce());
    }

    @Test
    void dispatcherHandsEveryMessageOff() throws Exception {
        DispatcherWorkers dw = new DispatcherWorkers(LeaderFollowersDemo.messages(), 2);
        dw.runUntilStopped();
        assertEquals(20, dw.handOffs());
        assertEquals(0, dw.record().sameThread());
    }
}
