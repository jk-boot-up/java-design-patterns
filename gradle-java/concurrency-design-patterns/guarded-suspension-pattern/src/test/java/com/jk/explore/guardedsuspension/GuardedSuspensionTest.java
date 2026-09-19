package com.jk.explore.guardedsuspension;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static com.jk.explore.guardedsuspension.GuardedSuspensionDemo.startTaker;
import static com.jk.explore.guardedsuspension.GuardedSuspensionDemo.until;
import static org.junit.jupiter.api.Assertions.*;

class GuardedSuspensionTest {

    @RepeatedTest(3)
    void aWaitingPickerUsesNoProcessorAndIsWokenByAnOrder() throws Exception {
        WaitingInbox inbox = new WaitingInbox();
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        Thread t = startTaker(inbox, got);
        until(() -> t.getState() == Thread.State.WAITING);
        assertEquals(Thread.State.WAITING, t.getState());
        inbox.put("A");
        t.join();
        assertEquals(List.of("A"), got);
    }

    @RepeatedTest(3)
    void aSpinningPickerAsksManyTimesWhileNothingComes() throws Exception {
        SpinningInbox inbox = new SpinningInbox();
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        Thread t = startTaker(inbox, got);
        until(() -> inbox.checks() >= 100_000);
        assertTrue(inbox.checks() >= 100_000);
        inbox.put("A");
        t.join();
        assertEquals(List.of("A"), got);
    }

    @RepeatedTest(3)
    void withAnIfGuardTwoPickersWakeAndOneTakesNothing() throws Exception {
        IfGuardInbox inbox = new IfGuardInbox();
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        Thread a = startTaker(inbox, got);
        Thread b = startTaker(inbox, got);
        until(() -> a.getState() == Thread.State.WAITING && b.getState() == Thread.State.WAITING);
        inbox.put("A");
        a.join();
        b.join();
        assertEquals(2, got.size());
        assertTrue(got.contains("null"));
    }

    @RepeatedTest(3)
    void withAWhileGuardTheSecondPickerGoesBackToWaiting() throws Exception {
        WaitingInbox inbox = new WaitingInbox();
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        Thread a = startTaker(inbox, got);
        Thread b = startTaker(inbox, got);
        until(() -> a.getState() == Thread.State.WAITING && b.getState() == Thread.State.WAITING);
        inbox.put("A");
        until(() -> got.size() == 1 && inbox.wakeups() == 2);
        Thread other = got.size() == 1 && !a.isAlive() ? b : a;
        until(() -> other.getState() == Thread.State.WAITING);
        assertEquals(List.of("A"), got);
        assertEquals(Thread.State.WAITING, other.getState());
        inbox.put("B");
        a.join();
        b.join();
        assertEquals(2, got.size());
        assertFalse(got.contains("null"));
    }

    @Test
    void anOrderThatCameFirstIsTakenAtOnceOnlyIfTheGuardIsCheckedFirst() throws Exception {
        WaitingInbox careful = new WaitingInbox();
        careful.put("A");
        assertEquals("A", careful.take());
        NoCheckInbox blind = new NoCheckInbox();
        blind.put("A");
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        Thread t = startTaker(blind, got);
        until(() -> t.getState() == Thread.State.WAITING);
        assertEquals(Thread.State.WAITING, t.getState());
        blind.put("B");
        t.join();
    }

    @Test
    void aLimitedWaitReturnsNullWhenNothingComesAndTheOrderWhenItDoes() throws Exception {
        WaitingInbox inbox = new WaitingInbox();
        assertNull(inbox.take(50));
        inbox.put("A");
        assertEquals("A", inbox.take(50));
    }

    @Test
    void notifyAllWakesEveryWaiterForOneOrder() throws Exception {
        WaitingInbox inbox = new WaitingInbox();
        List<Thread> ts = new ArrayList<>();
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        for (int i = 0; i < 10; i++) ts.add(startTaker(inbox, got));
        until(() -> ts.stream().allMatch(t -> t.getState() == Thread.State.WAITING));
        inbox.put("A");
        until(() -> inbox.wakeups() >= 10);
        assertEquals(10, inbox.wakeups());
        for (int i = 0; i < 9; i++) inbox.put("B" + i);
        for (Thread t : ts) t.join();
    }
}
