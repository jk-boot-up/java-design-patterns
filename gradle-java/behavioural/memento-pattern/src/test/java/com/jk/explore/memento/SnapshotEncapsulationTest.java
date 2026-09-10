package com.jk.explore.memento;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

/**
 * The structural test: a snapshot must stay closed.
 *
 * <p>A comment saying "the caretaker must not read a snapshot" survives
 * exactly as long as the first person who is in a hurry. This does not. Add a
 * public getter to {@link BasketSnapshot} and this test names the method back
 * at you.
 */
class SnapshotEncapsulationTest {

    /** The only things a snapshot is allowed to tell the outside world. */
    private static final List<String> ALLOWED =
            List.of("label", "toString", "equals", "hashCode");

    @Test
    void nothingPublicOnASnapshotGivesUpTheBasket() {
        List<String> offenders = new ArrayList<>();
        for (Method method : BasketSnapshot.class.getDeclaredMethods()) {
            if (Modifier.isPublic(method.getModifiers())
                    && !ALLOWED.contains(method.getName())) {
                offenders.add(method.getName());
            }
        }
        assertEquals(List.of(), offenders,
                "these are public, so a caretaker could read the basket out of a snapshot");
    }

    @Test
    void theCopiedLinesCannotBeEditedThroughTheSnapshotEither() {
        Basket basket = new Basket();
        basket.add("Desk mat", 18, 1);
        BasketSnapshot snapshot = basket.save("added the mat");

        // Reachable only from inside this package, and even then it is a
        // List.copyOf, so there is no way to alter what was saved.
        assertThrows(UnsupportedOperationException.class,
                () -> snapshot.lines().clear());
    }
}
