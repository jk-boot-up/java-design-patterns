package com.jk.explore.singleton;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Constructor;

import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LegacyOrderSequenceGeneratorTest {

    @Test
    void getInstanceReturnsSameReferenceOnRepeatedCalls() {
        LegacyOrderSequenceGenerator first = LegacyOrderSequenceGenerator.getInstance();
        LegacyOrderSequenceGenerator second = LegacyOrderSequenceGenerator.getInstance();

        assertSame(first, second);
    }

    @Test
    void reflectionCanCreateASecondInstance() throws Exception {
        LegacyOrderSequenceGenerator viaGetInstance = LegacyOrderSequenceGenerator.getInstance();

        Constructor<LegacyOrderSequenceGenerator> constructor =
                LegacyOrderSequenceGenerator.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        LegacyOrderSequenceGenerator forged = constructor.newInstance();

        assertNotSame(viaGetInstance, forged, "the private constructor should not be reachable, but it is");
        assertTrue(forged.nextOrderNumber().matches("ORD-\\d{6}"));
    }

    @Test
    void deserializationCanCreateASecondInstance() throws Exception {
        LegacyOrderSequenceGenerator viaGetInstance = LegacyOrderSequenceGenerator.getInstance();

        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        try (ObjectOutputStream out = new ObjectOutputStream(bytes)) {
            out.writeObject(viaGetInstance);
        }

        LegacyOrderSequenceGenerator roundTripped;
        try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(bytes.toByteArray()))) {
            roundTripped = (LegacyOrderSequenceGenerator) in.readObject();
        }

        assertNotSame(viaGetInstance, roundTripped, "deserialization should not mint a new instance, but it does");
    }
}
