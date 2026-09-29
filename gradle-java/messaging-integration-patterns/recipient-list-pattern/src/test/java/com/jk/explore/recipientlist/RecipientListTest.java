package com.jk.explore.recipientlist;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;

class RecipientListTest {

    @Test
    void recipientsComeFromTheOrder() {
        assertEquals(List.of("north", "big-items"), RecipientListDemo.standard().recipientsFor(RecipientListDemo.ORDERS.get(0)));
    }

    @Test
    void eachRecipientOnceEvenForSeveralLines() {
        Order o = new Order("X", List.of("kitchen", "kitchen"), 100, false);
        assertEquals(List.of("north"), RecipientListDemo.standard().recipientsFor(o));
    }

    @Test
    void rulesAddRecipients() {
        RecipientList l = RecipientListDemo.standard().rule(o -> o.gift() ? Optional.of("gift-wrap") : Optional.empty());
        assertEquals(List.of("north", "gift-wrap"), l.recipientsFor(RecipientListDemo.ORDERS.get(1)));
    }

    @Test
    void unreachableRecipientsAreReported() {
        Inboxes in = new Inboxes();
        in.takeDown("big-items");
        assertEquals(List.of("big-items"), RecipientListDemo.standard().send(RecipientListDemo.ORDERS.get(0), in));
    }
}
