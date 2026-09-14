package com.jk.explore.databaseperservice;

/**
 * Somebody tried to read a database that is not theirs.
 *
 * In a real shop nothing throws this. The rule is enforced by the database's own
 * credentials: the Orders service is given a username that simply cannot see the
 * Catalog tables, and an attempt to read them fails as a permissions error long
 * before it reaches any Java. There is no polite convention involved and no comment
 * in a wiki asking people not to.
 *
 * <p>This exception exists so that the rule is visible in a project small enough to
 * read. When you see it thrown in a test, read it as "the database refused".
 */
public class NotYourDataException extends RuntimeException {

    public NotYourDataException(String requester, String owner) {
        super(requester + " may not read " + owner + "'s database directly. Ask "
                + owner + " for it.");
    }
}
