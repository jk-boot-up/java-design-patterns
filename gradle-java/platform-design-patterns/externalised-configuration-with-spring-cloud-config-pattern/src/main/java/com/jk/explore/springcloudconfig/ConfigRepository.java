package com.jk.explore.springcloudconfig;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.List;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.lib.PersonIdent;
import org.eclipse.jgit.revwalk.RevCommit;

/**
 * The git repository the config server reads, created by the demo in a temporary folder.
 *
 * <p>It holds one file, {@code checkout-service.yml}, with the delivery settings in it. Every
 * change is a commit with a name and a time on it, which is the history a setting loses when it
 * leaves the source code and gets back when it lives in git.
 *
 * <p>The commits are made with JGit, a git written in Java, so nothing needs to be installed.
 * Each commit is given a fixed author and a fixed time. A commit's id is worked out from its
 * contents, its parent, its author and its time, so fixing them makes the ids the same on every
 * run and on every machine.
 */
public final class ConfigRepository implements AutoCloseable {

    public static final String FILE = "checkout-service.yml";
    private static final ZoneId LONDON = ZoneId.of("Europe/London");

    private final Path folder;
    private final Git git;

    private ConfigRepository(Path folder, Git git) {
        this.folder = folder;
        this.git = git;
    }

    /** A new repository in {@code folder}, with nothing committed yet. */
    public static ConfigRepository createIn(Path folder) {
        try {
            Files.createDirectories(folder);
            Git git = Git.init().setDirectory(folder.toFile()).setInitialBranch("main").call();
            return new ConfigRepository(folder, git);
        } catch (IOException | GitAPIException e) {
            throw new IllegalStateException("could not create the config repository", e);
        }
    }

    /** The address the config server is given, a file URL. */
    public String uri() {
        return folder.toUri().toString();
    }

    /**
     * Writes the delivery settings and commits them.
     *
     * @return the first seven characters of the new commit's id, as git prints it
     */
    public String commit(String freeOver, String standard, String who, LocalDateTime when, String message) {
        String yaml = "delivery:\n"
                + "  free-over: " + freeOver + "\n"
                + "  standard: " + standard + "\n";
        try {
            Files.writeString(folder.resolve(FILE), yaml, StandardCharsets.UTF_8);
            git.add().addFilepattern(FILE).call();
            PersonIdent person = new PersonIdent(who, who.toLowerCase().replace(' ', '.') + "@shop.example",
                    when.atZone(LONDON).toInstant(), LONDON);
            RevCommit commit = git.commit()
                    .setMessage(message)
                    .setAuthor(person)
                    .setCommitter(person)
                    .setSign(false)
                    .call();
            return commit.getId().abbreviate(7).name();
        } catch (IOException | GitAPIException e) {
            throw new IllegalStateException("could not commit to the config repository", e);
        }
    }

    /** One line per commit, newest first: id, author, message. */
    public List<String> log() {
        List<String> lines = new ArrayList<>();
        try {
            for (RevCommit c : git.log().call()) {
                lines.add(c.getId().abbreviate(7).name() + "  " + c.getAuthorIdent().getName()
                        + "  " + c.getShortMessage());
            }
        } catch (GitAPIException e) {
            throw new IllegalStateException("could not read the config repository's history", e);
        }
        return lines;
    }

    @Override
    public void close() {
        git.close();
    }
}
