package com.jk.explore.nullobject.pattern;

/** <strong>The same eight methods with no null check anywhere.</strong> The behaviour is identical. */
public class NullObjectCheckout {

    private final NullObjectDirectory directory;

    public NullObjectCheckout(NullObjectDirectory directory) {
        this.directory = directory;
    }

    public long total(int customerId, long price) {
        return directory.find(customerId).apply(price);
    }

    public long invoiceLine(int customerId, long price) {
        return directory.find(customerId).apply(price);
    }

    public long receiptEmail(int customerId, long price) {
        return directory.find(customerId).apply(price);
    }

    public long loyaltyReport(int customerId, long price) {
        return directory.find(customerId).apply(price);
    }

    public long staffExport(int customerId, long price) {
        return directory.find(customerId).apply(price);
    }

    public long refundAmount(int customerId, long price) {
        return directory.find(customerId).apply(price);
    }

    public long shippingLabelTotal(int customerId, long price) {
        return directory.find(customerId).apply(price);
    }

    public long taxBase(int customerId, long price) {
        return directory.find(customerId).apply(price);
    }
}
