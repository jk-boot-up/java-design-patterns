package com.jk.explore.externalisedconfig;

/**
 * Thrown when a configuration source cannot be reached at all.
 *
 * <p>This is deliberately a different thing from a missing key. "The server has
 * no value for delivery.freeOver" means carry on with the default and think no
 * more about it. "The server did not answer" means the shop is now running on
 * defaults for <em>every</em> setting, and somebody should know.
 *
 * <p>It is unchecked because there is nothing useful a checkout can do about it
 * in the moment. The decision — fall back to the compiled-in default and keep
 * selling — belongs one level up, in the settings reader, and both readers in
 * this project make that decision the same way.
 */
public class ConfigSourceUnavailableException extends RuntimeException {

    public ConfigSourceUnavailableException(String message) {
        super(message);
    }
}
