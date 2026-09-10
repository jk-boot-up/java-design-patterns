package com.jk.explore.mediator;

/**
 * The "gift wrap this order" tick box.
 *
 * <p>Gift wrapping is done by hand in the London warehouse, so it is only
 * offered on domestic orders. When it is not offered the box has to be both
 * disabled <em>and</em> cleared — a disabled box that is still ticked is how a
 * shopper ends up paying for a service nobody will perform.
 */
public class GiftWrapCheckbox extends FormWidget {

    private boolean available = true;
    private boolean ticked;

    public GiftWrapCheckbox(CheckoutMediator mediator) {
        super("giftWrap", mediator);
    }

    public boolean isAvailable() {
        return available;
    }

    public boolean isTicked() {
        return ticked;
    }

    /**
     * Offer or withdraw gift wrapping. Withdrawing it clears the tick in the
     * same breath, so the two can never disagree.
     *
     * <p>Called by the mediator, so it does not announce a change.
     */
    void setAvailable(boolean available) {
        this.available = available;
        if (!available) {
            this.ticked = false;
        }
    }

    /** The shopper ticks or unticks the box. A withdrawn box ignores them. */
    public void tick(boolean ticked) {
        if (!available) {
            return;
        }
        this.ticked = ticked;
        announceChange();
    }
}
