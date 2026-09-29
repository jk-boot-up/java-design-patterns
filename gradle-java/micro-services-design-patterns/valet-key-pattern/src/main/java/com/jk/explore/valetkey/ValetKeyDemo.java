package com.jk.explore.valetkey;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: uploads carried by the app, a valet key, what the key does not allow, expiry, and the bill.
 */
public final class ValetKeyDemo {

    static final byte[] PHOTO = new byte[2_000_000];

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static String mb(long bytes) {
        return String.format("%.1f MB", bytes / 1_000_000.0);
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        Signer signer = new Signer("shared-secret-between-shop-and-storage");
        try (Storage storage = new Storage(signer)) {

            out.add("ONE. Review photos carried through the shop's app server.");
            Shop old = new Shop(storage, signer);
            for (int i = 1; i <= 10; i++) {
                old.uploadThroughApp("/reviews/R-" + i + "/photo.jpg", PHOTO);
            }
            out.add("  10 customers upload a 2 MB photo each: the app server carried " + mb(old.bytesCarried()));
            out.add("  every byte came in to the app and went out again to storage");

            out.add("");
            out.add("TWO. A valet key: permission to do one thing, directly.");
            Shop shop = new Shop(storage, signer);
            String key = shop.valetKey("/reviews/R-11/photo.jpg", 5 * 60_000, 5_000_000);
            out.add("  the shop signs: PUT /reviews/R-11/photo.jpg, for 5 minutes, up to 5 MB");
            out.add("  the customer's browser uploads straight to storage: " + Customer.put(key, PHOTO));
            out.add("  the app server carried " + (shop.bytesCarried() < 200 ? "under 200 bytes" : shop.bytesCarried() + " bytes") + ": just the key");

            out.add("");
            out.add("THREE. The key allows that, and nothing else.");
            out.add("  read the photo with it:     " + Customer.get(key));
            String otherPath = key.replace("R-11", "R-3");
            out.add("  upload over review R-3:    " + Customer.put(otherPath, PHOTO));
            out.add("  a 6 MB file:                " + Customer.put(key, new byte[6_000_000]));
            out.add("  no key at all:              " + Customer.put(storage.url() + "/reviews/R-12/photo.jpg", PHOTO));

            out.add("");
            out.add("FOUR. The key runs out.");
            String shortKey = shop.valetKey("/reviews/R-13/photo.jpg", 200, 5_000_000);
            Thread.sleep(400);
            out.add("  a key valid for 0.2 s, used after 0.4 s: " + Customer.put(shortKey, PHOTO));

            out.add("");
            out.add("FIVE. The bill: whoever holds the key can use it.");
            String key14 = shop.valetKey("/reviews/R-14/photo.jpg", 5 * 60_000, 5_000_000);
            out.add("  the key is copied into a public chat; a stranger uses it: " + Customer.put(key14, new byte[10]));
            out.add("  it cannot be taken back before it expires: keep keys short-lived, narrow, and out of logs");
        }
        return out;
    }

    private ValetKeyDemo() {
    }
}
