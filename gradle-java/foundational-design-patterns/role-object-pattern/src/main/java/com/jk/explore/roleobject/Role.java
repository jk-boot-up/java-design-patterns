package com.jk.explore.roleobject;

/**
 * Something an account does for a while: buying, selling, referring. Each role knows the account it belongs to.
 */
public abstract class Role {

    protected final Account account;

    protected Role(Account account) {
        this.account = account;
    }

    public Account account() {
        return account;
    }
}
