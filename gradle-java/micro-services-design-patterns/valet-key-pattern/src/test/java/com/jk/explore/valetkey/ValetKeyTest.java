package com.jk.explore.valetkey;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class ValetKeyTest {

    private final Signer signer = new Signer("s");

    @Test
    void keyAllowsItsOwnUpload() throws Exception {
        try (Storage st = new Storage(signer)) {
            String key = new Shop(st, signer).valetKey("/a.jpg", 60_000, 100);
            assertTrue(Customer.put(key, new byte[50]).startsWith("201"));
        }
    }

    @Test
    void keyRefusesOtherPathsMethodsAndSizes() throws Exception {
        try (Storage st = new Storage(signer)) {
            String key = new Shop(st, signer).valetKey("/a.jpg", 60_000, 100);
            assertTrue(Customer.put(key.replace("/a.jpg", "/b.jpg"), new byte[1]).startsWith("403"));
            assertTrue(Customer.get(key).startsWith("403"));
            assertTrue(Customer.put(key, new byte[101]).startsWith("413"));
        }
    }

    @Test
    void forgedSignatureIsRefused() throws Exception {
        try (Storage st = new Storage(signer)) {
            String key = new Shop(st, new Signer("wrong")).valetKey("/a.jpg", 60_000, 100);
            assertTrue(Customer.put(key, new byte[1]).startsWith("403"));
        }
    }
}
