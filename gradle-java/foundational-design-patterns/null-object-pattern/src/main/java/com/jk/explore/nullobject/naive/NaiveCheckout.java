package com.jk.explore.nullobject.naive;

import com.jk.explore.nullobject.domain.Discount;
import com.jk.explore.nullobject.domain.DiscountDirectory;

/**
 * <strong>{@code find} returns {@code null}, and every caller checks.</strong>
 * Eight places price something after a discount. Seven of them remembered the
 * check. One did not.
 */
public class NaiveCheckout {

    private final DiscountDirectory directory;

    public NaiveCheckout(DiscountDirectory directory) {
        this.directory = directory;
    }

    public long total(int customerId, long price) {
        Discount discount = directory.find(customerId);
        if (discount != null) {
            return discount.apply(price);
        }
        return price;
    }

    public long invoiceLine(int customerId, long price) {
        Discount discount = directory.find(customerId);
        if (discount != null) {
            return discount.apply(price);
        }
        return price;
    }

    public long receiptEmail(int customerId, long price) {
        Discount discount = directory.find(customerId);
        if (discount != null) {
            return discount.apply(price);
        }
        return price;
    }

    public long loyaltyReport(int customerId, long price) {
        Discount discount = directory.find(customerId);
        if (discount != null) {
            return discount.apply(price);
        }
        return price;
    }

    public long staffExport(int customerId, long price) {
        Discount discount = directory.find(customerId);
        if (discount != null) {
            return discount.apply(price);
        }
        return price;
    }

    public long refundAmount(int customerId, long price) {
        Discount discount = directory.find(customerId);
        if (discount != null) {
            return discount.apply(price);
        }
        return price;
    }

    public long shippingLabelTotal(int customerId, long price) {
        Discount discount = directory.find(customerId);
        if (discount != null) {
            return discount.apply(price);
        }
        return price;
    }

    /** The one that was added last, in a hurry, by someone who assumed a discount always exists. */
    public long taxBase(int customerId, long price) {
        Discount discount = directory.find(customerId);
        return discount.apply(price);
    }
}
