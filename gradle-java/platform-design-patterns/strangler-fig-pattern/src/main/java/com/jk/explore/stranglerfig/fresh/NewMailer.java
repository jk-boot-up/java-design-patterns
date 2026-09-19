package com.jk.explore.stranglerfig.fresh;

import com.jk.explore.stranglerfig.domain.Mailer;
import com.jk.explore.stranglerfig.domain.Order;

/** The rewritten notification service. */
public class NewMailer implements Mailer {

    private int sent;

    @Override
    public boolean confirm(Order order) {
        sent++;
        return true;
    }

    public int sent() {
        return sent;
    }
}
