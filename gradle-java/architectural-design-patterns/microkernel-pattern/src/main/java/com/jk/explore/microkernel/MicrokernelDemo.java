package com.jk.explore.microkernel;

import java.util.List;
import java.util.Set;

public class MicrokernelDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Every feature inside.");
        MonolithCheckout checkout = new MonolithCheckout();
        long total = checkout.total(10000, Set.of("gift-wrap"));
        System.out.println("  gift wrap asked for. supported: " + checkout.supports("gift-wrap") + ". total: " + total + ", unchanged.");
        System.out.println("  to add it, edit the checkout, test all of it again, and release all of it.");
    }

    private static void two() {
        System.out.println("TWO. A core and plugins.");
        Kernel kernel = new Kernel();
        kernel.register(new PercentOff("member-discount", 10));
        kernel.register(new Fee("shipping-fee", 500));
        System.out.println("  plugins: " + kernel.names() + ". total of 10000: " + kernel.total(10000) + ".");
        System.out.println("  the core knows one interface, Plugin, and nothing about discounts or fees.");
    }

    private static void three() {
        System.out.println("THREE. A new feature, no change to the core.");
        Kernel kernel = new Kernel();
        kernel.register(new PercentOff("member-discount", 10));
        kernel.register(new Fee("shipping-fee", 500));
        Fee wrap = new Fee("gift-wrap", 300);
        kernel.register(wrap);
        System.out.println("  gift wrap registered while running. plugins: " + kernel.names() + ". total: " + kernel.total(10000) + ". started: " + wrap.running() + ".");
        kernel.unregister("gift-wrap");
        System.out.println("  and taken away again. stopped: " + !wrap.running() + ". total: " + kernel.total(10000) + ".");
    }

    private static void four() {
        System.out.println("FOUR. A plugin that breaks.");
        Kernel kernel = new Kernel();
        kernel.register(new PercentOff("member-discount", 10));
        kernel.register(new BrokenPlugin("loyalty-points"));
        kernel.register(new Fee("shipping-fee", 500));
        System.out.println("  total: " + kernel.total(10000) + ", so the other plugins still ran.");
        System.out.println("  recorded: " + kernel.failures() + ".");
    }

    private static void five() {
        System.out.println("FIVE. Order matters.");
        Kernel discountFirst = new Kernel();
        discountFirst.register(new PercentOff("member-discount", 10));
        discountFirst.register(new Fee("shipping-fee", 500));
        Kernel feeFirst = new Kernel();
        feeFirst.register(new Fee("shipping-fee", 500));
        feeFirst.register(new PercentOff("member-discount", 10));
        System.out.println("  discount then fee: " + discountFirst.total(10000) + ". fee then discount: " + feeFirst.total(10000) + ".");
        System.out.println("  the same two plugins, a different price. the core cannot know which is right.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        List<String> wanted = List.of("adjust a total", "read the customer's country", "add a line to the receipt");
        System.out.println("  the interface offers one thing: adjust a total. wanted by plugins: " + wanted + ".");
        System.out.println("  a plugin that needs the country cannot get it. either the interface grows, and every plugin feels it, or plugins reach round the core.");
        System.out.println("  and a customer's total is now decided by whichever plugins happen to be installed, in some order.");
    }
}
