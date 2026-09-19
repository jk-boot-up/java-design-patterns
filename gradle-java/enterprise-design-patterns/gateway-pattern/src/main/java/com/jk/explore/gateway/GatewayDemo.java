package com.jk.explore.gateway;

import com.jk.explore.gateway.naive.NaiveCheckout;
import com.jk.explore.gateway.vendor.AcmeClient;
import com.jk.explore.gateway.vendor.BetaPayClient;

import java.util.ArrayList;
import java.util.List;

public class GatewayDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. The provider's client, everywhere.");
        AcmeClient acme = new AcmeClient();
        NaiveCheckout naive = new NaiveCheckout(acme);
        AcmeClient.NETWORK_CALLS.set(0);
        System.out.println("  checkout: " + naive.checkout(4999) + ". renewal: " + naive.renewSubscription(999) + ". gift card: " + naive.topUpGiftCard(2000) + ".");
        System.out.println("  three places build the provider's request fields and read its result codes. network calls made: " + AcmeClient.NETWORK_CALLS.get() + ".");
        System.out.println("  one of them forgot the currency field. nobody has noticed yet.");
    }

    private static void two() {
        System.out.println("TWO. One door.");
        AcmeClient acme = new AcmeClient();
        acme.script("00", "51");
        Checkout checkout = new Checkout(new AcmeGateway(acme, new ArrayList<>()));
        System.out.println("  the shop asks: " + checkout.pay(4999) + ".");
        System.out.println("  the shop asks again: " + checkout.pay(4999) + ".");
        System.out.println("  Checkout has no field name and no result code in it. it speaks approved, declined and unavailable.");
    }

    private static void three() {
        System.out.println("THREE. Tests that never leave the process.");
        AcmeClient.NETWORK_CALLS.set(0);
        FakeGateway fake = new FakeGateway().willAnswer(PaymentStatus.APPROVED, PaymentStatus.DECLINED, PaymentStatus.UNAVAILABLE);
        Checkout checkout = new Checkout(fake);
        System.out.println("  " + checkout.pay(100) + "; " + checkout.pay(100) + "; " + checkout.pay(100) + ".");
        System.out.println("  asked of the fake: " + fake.calls() + " times. network calls made: " + AcmeClient.NETWORK_CALLS.get() + ".");
        System.out.println("  the fake can be told to decline, or to be down, on demand. a real provider cannot.");
    }

    private static void four() {
        System.out.println("FOUR. One place for the network's habits.");
        AcmeClient acme = new AcmeClient();
        List<String> log = new ArrayList<>();
        acme.script("91", "00");
        AcmeClient.NETWORK_CALLS.set(0);
        String answer = new Checkout(new AcmeGateway(acme, log)).pay(4999);
        System.out.println("  the provider times out once, then answers. the shop is told: " + answer + ".");
        System.out.println("  network calls: " + AcmeClient.NETWORK_CALLS.get() + ". log: " + log + ".");
        acme.script("91", "91");
        System.out.println("  timing out twice: " + new Checkout(new AcmeGateway(acme, log)).pay(4999) + ".");
        System.out.println("  the retry rule lives in one class. the three naive callers would each have needed their own.");
    }

    private static void five() {
        System.out.println("FIVE. Another provider, the same shop.");
        Checkout onAcme = new Checkout(new AcmeGateway(new AcmeClient(), new ArrayList<>()));
        Checkout onBeta = new Checkout(new BetaGateway(new BetaPayClient()));
        System.out.println("  on Acme: " + onAcme.pay(4999) + ". on BetaPay: " + onBeta.pay(4999) + ".");
        System.out.println("  a large amount, on BetaPay: " + onBeta.pay(150000) + ".");
        System.out.println("  Checkout was not changed. it was given a different gateway.");
    }

    private static void six() {
        System.out.println("SIX. The bill: what the door cannot say.");
        System.out.println("  Acme can hold a payment and capture part of it later. the gateway interface has one method, charge.");
        System.out.println("  to use partial capture, a method is added to the interface, and to all " + implementations() + " gateways: Acme, BetaPay and the fake.");
        System.out.println("  and BetaPay cannot do it at all, so the interface must say what happens then.");
    }

    private static int implementations() {
        return 3;
    }
}
