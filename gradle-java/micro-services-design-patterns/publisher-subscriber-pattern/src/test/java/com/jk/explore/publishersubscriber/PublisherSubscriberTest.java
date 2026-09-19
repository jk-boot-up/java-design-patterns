package com.jk.explore.publishersubscriber;

import com.jk.explore.publishersubscriber.naive.DirectOrderService;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static com.jk.explore.publishersubscriber.PublisherSubscriberDemo.ANY;
import static com.jk.explore.publishersubscriber.PublisherSubscriberDemo.PLACED;
import static org.junit.jupiter.api.Assertions.*;

class PublisherSubscriberTest {

    private final Topic topic = new Topic();

    @Test
    void everySubscriberGetsEveryEvent() {
        List<String> a = new ArrayList<>(), b = new ArrayList<>();
        var sa = topic.subscribeFromStart("a", ANY, e -> a.add(e.orderId()));
        var sb = topic.subscribeFromStart("b", ANY, e -> b.add(e.orderId()));
        topic.publish(new Event("OrderPlaced", "1"));
        topic.publish(new Event("OrderPlaced", "2"));
        sa.deliver(10);
        sb.deliver(10);
        assertEquals(List.of("1", "2"), a);
        assertEquals(List.of("1", "2"), b);
    }

    @Test
    void aSubscriberAddedLaterNeedsNoChangeToThePublisher() {
        topic.publish(new Event("OrderPlaced", "1"));
        List<String> late = new ArrayList<>();
        topic.subscribeFromStart("late", ANY, e -> late.add(e.orderId())).deliver(10);
        assertEquals(List.of("1"), late);
        assertEquals(3, DirectOrderService.servicesItKnows());
    }

    @Test
    void aSlowSubscriberHasABacklogAndDoesNotHoldUpAnother() {
        var fast = topic.subscribeFromStart("fast", ANY, e -> { });
        var slow = topic.subscribeFromStart("slow", ANY, e -> { });
        for (int i = 0; i < 5; i++) topic.publish(new Event("OrderPlaced", "" + i));
        fast.deliver(10);
        slow.deliver(1);
        assertEquals(0, fast.backlog());
        assertEquals(4, slow.backlog());
        slow.deliver(10);
        assertEquals(0, slow.backlog());
    }

    @Test
    void filtersSelectByKindButTheOffsetStillAdvances() {
        List<String> got = new ArrayList<>();
        var s = topic.subscribeFromStart("email", PLACED, e -> got.add(e.kind()));
        topic.publish(new Event("OrderPlaced", "1"));
        topic.publish(new Event("OrderCancelled", "1"));
        s.deliver(10);
        assertEquals(List.of("OrderPlaced"), got);
        assertEquals(0, s.backlog());
    }

    @Test
    void aLiveSubscriberMissesHistoryAndAReplayingOneDoesNot() {
        for (int i = 1; i <= 3; i++) topic.publish(new Event("OrderPlaced", "" + i));
        List<String> live = new ArrayList<>(), replay = new ArrayList<>();
        var l = topic.subscribeLive("l", ANY, e -> live.add(e.orderId()));
        var r = topic.subscribeFromStart("r", ANY, e -> replay.add(e.orderId()));
        topic.publish(new Event("OrderPlaced", "4"));
        l.deliver(10);
        r.deliver(10);
        assertEquals(List.of("4"), live);
        assertEquals(List.of("1", "2", "3", "4"), replay);
    }

    @Test
    void aDisconnectedSubscriberCatchesUpBecauseItsOffsetWasKept() {
        List<String> got = new ArrayList<>();
        var s = topic.subscribeFromStart("email", ANY, e -> got.add(e.orderId()));
        s.disconnect();
        topic.publish(new Event("OrderPlaced", "1"));
        assertEquals(0, s.deliver(10));
        assertEquals(1, s.backlog());
        s.reconnect();
        s.deliver(10);
        assertEquals(List.of("1"), got);
    }

    @Test
    void thePublisherLearnsNothingAboutDelivery() {
        topic.publish(new Event("OrderPlaced", "1"));
        assertEquals(1, topic.published());
    }
}
