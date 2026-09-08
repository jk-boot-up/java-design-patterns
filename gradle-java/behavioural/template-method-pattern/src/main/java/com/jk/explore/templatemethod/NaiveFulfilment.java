package com.jk.explore.templatemethod;

/**
 * The trap, kept for contrast: three fulfilment routes that each write the
 * whole sequence out for themselves.
 *
 * <p>It is worth being fair to this class. It is shorter than the pattern,
 * it needs no vocabulary to read, and every one of these three methods can be
 * understood on its own without looking anywhere else. On the day it was
 * written it was almost certainly correct.
 *
 * <p>What it cannot do is stay correct. The sequence is only a convention
 * here, repeated by hand, and conventions drift every time somebody edits one
 * copy in a hurry. Two of the three have already drifted:
 *
 * <ul>
 *   <li>{@link #fulfilDigital} tells the customer <em>before</em> it issues
 *       the licence key, so the email goes out with nothing in it worth
 *       having;</li>
 *   <li>{@link #fulfilFromMarketplace} charges the card <em>before</em>
 *       asking the seller to confirm, so a customer can be charged for an
 *       order the seller then refuses.</li>
 * </ul>
 *
 * <p>Neither throws. Neither fails a compile. Both are one line in the wrong
 * place, in a file nobody has a reason to reread.
 */
public final class NaiveFulfilment {

    private static final int COMMISSION_PERCENT = 12;

    private final StockLedger ledger;
    private final String site;
    private final SellerApi seller;

    public NaiveFulfilment(StockLedger ledger, String site, SellerApi seller) {
        this.ledger = ledger;
        this.site = site;
        this.seller = seller;
    }

    public FulfilmentReport fulfilFromWarehouse(Order order) {
        FulfilmentReport report = new FulfilmentReport(order.id(), "naive warehouse");

        if (order.lines().isEmpty()) {
            throw new FulfilmentException("order " + order.id() + " has no lines");
        }
        if (!order.hasShippingAddress()) {
            throw new FulfilmentException("order " + order.id() + " has no shipping address");
        }
        report.step("validate", order.lines().size() + " line(s), address checked");

        for (OrderLine line : order.lines()) {
            ledger.reserve(line.sku(), line.quantity());
        }
        report.step("reserve", order.itemCount() + " unit(s) held at " + site);

        report.charged(order.subtotal());
        report.step("charge", order.subtotal() + " taken by the store");

        report.step("pack", order.itemCount() + " item(s) boxed and labelled");

        String consignment = "CON-" + order.id();
        report.dispatchedAs(consignment);
        report.step("dispatch", "courier collected, consignment " + consignment);

        report.notified(order.customerEmail() + ": Order " + order.id()
                + " is on its way. Tracking: " + report.dispatchReference());
        report.step("notify", "emailed " + order.customerEmail());

        return report;
    }

    public FulfilmentReport fulfilFromMarketplace(Order order) {
        FulfilmentReport report = new FulfilmentReport(order.id(), "naive marketplace");

        if (order.lines().isEmpty()) {
            throw new FulfilmentException("order " + order.id() + " has no lines");
        }
        if (!order.hasShippingAddress()) {
            throw new FulfilmentException("order " + order.id() + " has no shipping address");
        }
        report.step("validate", order.lines().size() + " line(s), address checked");

        // Drifted: the money is taken before the seller has agreed to anything.
        Money total = order.subtotal();
        report.charged(total);
        report.step("charge", total + " taken, " + total.percent(COMMISSION_PERCENT)
                + " commission retained");

        for (OrderLine line : order.lines()) {
            if (!seller.confirm(line.sku(), line.quantity())) {
                throw new FulfilmentException(
                        seller.sellerName() + " will not confirm " + line.sku());
            }
        }
        report.step("reserve", seller.sellerName() + " confirmed "
                + order.lines().size() + " line(s)");

        report.step("pack", "nothing boxed here — " + seller.sellerName() + " packs their own");

        String job = "MP-" + order.id();
        report.dispatchedAs(job);
        report.step("dispatch", "job " + job + " queued for " + seller.sellerName());

        report.notified(order.customerEmail() + ": Order " + order.id()
                + " is on its way. Tracking: " + report.dispatchReference());
        report.step("notify", "emailed " + order.customerEmail());

        return report;
    }

    public FulfilmentReport fulfilDigital(Order order) {
        FulfilmentReport report = new FulfilmentReport(order.id(), "naive digital");

        if (order.lines().isEmpty()) {
            throw new FulfilmentException("order " + order.id() + " has no lines");
        }
        report.step("validate", order.lines().size() + " line(s), no address needed");

        report.step("reserve", "nothing to reserve, " + order.itemCount() + " download(s)");

        report.charged(order.subtotal());
        report.step("charge", order.subtotal() + " taken by the store");

        report.step("pack", "nothing to pack");

        // Drifted: the last two steps are the wrong way round. The key does
        // not exist yet, so the customer is told about a reference that reads
        // "(not dispatched)".
        report.notified(order.customerEmail() + ": Order " + order.id()
                + " is ready to download. Key: " + report.dispatchReference());
        report.step("notify", "emailed " + order.customerEmail() + " with the key");

        String key = LicenceKeys.mint(order);
        report.dispatchedAs(key);
        report.step("dispatch", "licence key issued: " + key);

        return report;
    }
}
