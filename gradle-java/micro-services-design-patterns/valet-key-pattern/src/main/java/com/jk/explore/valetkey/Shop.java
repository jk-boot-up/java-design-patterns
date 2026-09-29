package com.jk.explore.valetkey;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * The shop's app server. The old way it carried every upload itself; the new way it hands out valet keys.
 */
public final class Shop {

    private final Storage storage;
    private final Signer signer;
    private final HttpClient http = HttpClient.newHttpClient();
    private long bytesCarried;

    public Shop(Storage storage, Signer signer) {
        this.storage = storage;
        this.signer = signer;
    }

    /** Without the pattern: the photo comes in to the app, and the app sends it on with its master credential. */
    public String uploadThroughApp(String path, byte[] photo) throws Exception {
        bytesCarried += photo.length;           // in from the customer
        HttpResponse<String> r = http.send(HttpRequest.newBuilder(URI.create(storage.url() + path))
                        .header("Authorization", Storage.MASTER)
                        .PUT(HttpRequest.BodyPublishers.ofByteArray(photo)).build(),
                HttpResponse.BodyHandlers.ofString());
        bytesCarried += photo.length;           // out to storage
        return r.body();
    }

    /** The pattern: a key for one PUT of one path, up to a size, for a few minutes. */
    public String valetKey(String path, long validForMs, long maxBytes) {
        long expires = System.currentTimeMillis() + validForMs;
        String key = storage.url() + path + "?expires=" + expires + "&max=" + maxBytes
                + "&sig=" + signer.sign("PUT", path, expires, maxBytes);
        bytesCarried += key.length();
        return key;
    }

    public long bytesCarried() {
        return bytesCarried;
    }
}
