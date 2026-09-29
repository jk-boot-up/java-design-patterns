package com.jk.explore.copyonwrite;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import org.junit.jupiter.api.Test;

class CowListTest {

    @Test
    void addAndRemove() {
        CowList<String> l = new CowList<>();
        l.add("a");
        l.add("b");
        l.remove("a");
        List<String> seen = new ArrayList<>();
        l.forEach(seen::add);
        assertEquals(List.of("b"), seen);
    }

    @Test
    void iteratorIsASnapshot() {
        CowList<String> l = new CowList<>();
        l.add("a");
        Iterator<String> it = l.iterator();
        l.add("b");
        List<String> seen = new ArrayList<>();
        it.forEachRemaining(seen::add);
        assertEquals(List.of("a"), seen);
        assertEquals(2, l.size());
    }

    @Test
    void addingWhileIteratingIsSafe() {
        CowList<String> l = new CowList<>();
        l.add("a");
        l.add("b");
        for (String s : l) {
            l.add(s + "!");
        }
        assertEquals(4, l.size());
    }

    @Test
    void everyWriteCopiesTheArray() {
        CowList<String> l = new CowList<>();
        for (int i = 0; i < 4; i++) {
            l.add("x" + i);
        }
        assertEquals(0 + 1 + 2 + 3, l.elementsCopied());
    }
}
