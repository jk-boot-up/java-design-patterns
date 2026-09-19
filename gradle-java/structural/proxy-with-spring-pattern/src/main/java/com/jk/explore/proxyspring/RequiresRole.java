package com.jk.explore.proxyspring;

import java.lang.annotation.*;

/** Marks a method that only the named role may call. The check itself lives in {@link RoleAspect}. */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface RequiresRole {
    Role value();
}
