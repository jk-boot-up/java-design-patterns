package com.jk.explore.activeobject;

import com.jk.explore.activeobject.pattern.Mailbox;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MailboxTest {

    @RepeatedTest(20)
    void everyMessageSentWhileTheWorkerIsBusyIsWaiting() throws InterruptedException {
        assertEquals(1_000, Mailbox.backlogWhileWorkerIsBusy(1_000),
                "nothing refused, nothing dropped, nothing pushed back");
    }

    @Test
    void moreCallersDoNotRaiseTheRateWhenTheWorkerIsTheBottleneck() throws InterruptedException {
        long work = 50_000;
        Mailbox.Throughput one = Mailbox.throughput(1, 1_000, work);
        Mailbox.Throughput four = Mailbox.throughput(4, 250, work);
        assertTrue(four.perSecond() < one.perSecond() * 2,
                "one=" + one.perSecond() + " four=" + four.perSecond());
    }
}
