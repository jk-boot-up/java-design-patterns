package com.jk.explore.templatemethod;

/**
 * A third-party seller on the store's marketplace. The store never touches
 * the goods: it asks the seller to confirm, takes the customer's money,
 * keeps a commission, and queues a job for the seller to ship.
 *
 * <p>Two overrides beyond the required steps. {@code pack} is replaced
 * because the packing happens in somebody else's building — the step still
 * runs and is still recorded, it simply has nothing physical to do here.
 * {@code afterFulfilment} is the hook: posting the commission to the seller
 * ledger is this route's own obligation, and the base class has no business
 * knowing that marketplaces exist.
 */
public final class MarketplaceFulfilment extends FulfilmentProcess {

    private static final int COMMISSION_PERCENT = 12;

    private final SellerApi seller;

    public MarketplaceFulfilment(SellerApi seller) {
        this.seller = seller;
    }

    @Override
    protected String routeName() {
        return "marketplace";
    }

    @Override
    protected void reserveStock(Order order, FulfilmentReport report) {
        for (OrderLine line : order.lines()) {
            if (!seller.confirm(line.sku(), line.quantity())) {
                throw new FulfilmentException(
                        seller.sellerName() + " will not confirm " + line.sku());
            }
        }
        report.step("reserve", seller.sellerName() + " confirmed "
                + order.lines().size() + " line(s)");
    }

    @Override
    protected void charge(Order order, FulfilmentReport report) {
        Money total = order.subtotal();
        Money commission = total.percent(COMMISSION_PERCENT);
        report.charged(total);
        report.step("charge", total + " taken, " + commission + " commission retained");
    }

    @Override
    protected void pack(Order order, FulfilmentReport report) {
        report.step("pack", "nothing boxed here — " + seller.sellerName() + " packs their own");
    }

    @Override
    protected void dispatch(Order order, FulfilmentReport report) {
        String job = "MP-" + order.id();
        report.dispatchedAs(job);
        report.step("dispatch", "job " + job + " queued for " + seller.sellerName());
    }

    @Override
    protected void afterFulfilment(Order order, FulfilmentReport report) {
        Money commission = order.subtotal().percent(COMMISSION_PERCENT);
        report.note("seller ledger: " + commission + " commission posted against "
                + seller.sellerName());
    }
}
