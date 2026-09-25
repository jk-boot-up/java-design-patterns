"""Scene definitions for the Externalised Configuration with Spring Cloud Config video.

Each scene has: key, title, kind, body, narration.

Narration speaks every figure out loud, says each of Spring's words in plain
language before using Spring's name for it, and never points at a picture the
listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Externalised Configuration with Spring Cloud Config',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Externalised '
            'Configuration pattern in Java, using a real configuration '
            'server from Spring Cloud. [[slnc 250]] It is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] Here is the '
            'plain definition, in general words. A value that changes on '
            'somebody else\'s calendar should live outside the program. '
            'The program reads it while it runs, so changing the value '
            'needs no rebuild and no release. [[slnc 350]] Now the same '
            'thing in our online store. The shop gives free delivery on '
            'any basket over fifty pounds. Marketing decides that number, '
            'not the programmers. So the number lives outside the shop, '
            'and the shop fetches it, and marketing can change it to '
            'thirty-five pounds for the weekend without anybody building '
            'the shop again. [[slnc 300]] By the end you will have seen a '
            'change that is saved but not yet used, a refresh that puts '
            'it in force with no restart, and one running shop that '
            'believes two different numbers at the same time.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Free delivery on baskets over £50.00.', 'Below that, delivery costs £4.99.', '',
              'Marketing decides the threshold.', 'Friday at 16:30 they want £35.00.', '',
              'The shop is a Spring Boot program.', 'Nobody wants a rebuild for one number.', '',
              'This time the value lives in git,', 'behind a real config server.'],
        narration=(
            'Here is the scenario. The shop gives free delivery on any '
            'basket over fifty pounds, and charges four pounds ninety-nine '
            'below that. Marketing decides the threshold, and on Friday '
            'at half past four they want thirty-five pounds for the '
            'weekend. [[slnc 300]] The hand-built twin of this project '
            'kept the threshold in a list inside the same program, and '
            'the checkout looked at it on every quote. This time the '
            'value lives in a git repository, a real server hands it out '
            'over the network, and the shop is a real Spring Boot '
            'program that fetches it. That changes four things.'
        ),
    ),
    dict(
        key='03-words', kind='bullets', title="Spring Cloud Config's Words",
        body=['Head office keeps the price list.', 'Every change is signed in a ledger.', '',
              'A branch phones in as it opens.', 'It writes the prices on its board.', '',
              'git repository: the cabinet, the ledger', 'config server: the receptionist', 'refresh: phone head office again', '',
              '@RefreshScope: the board, rewritten'],
        narration=(
            'Spring Cloud Config brings a few words with it, and each one '
            'is simpler than it sounds. Think of a chain of bakeries. '
            'Head office keeps the price list in a filing cabinet, and '
            'every change is signed and dated in a ledger. [[slnc 250]] '
            'A branch phones head office as it opens in the morning. The '
            'receptionist reads out the prices, and the branch writes '
            'them on its board for the day. [[slnc 250]] In Spring\'s '
            'words, the filing cabinet with its ledger is a git '
            'repository, and each signed change is a commit. The '
            'receptionist is the config server. Phoning in at opening '
            'time is fetching the settings at startup. Telling a branch '
            'to phone again is a refresh. [[slnc 250]] And the board '
            'that gets rubbed out and rewritten is an object marked with '
            'an annotation called refresh scope.'
        ),
    ),
    dict(
        key='04-one', kind='console', title='Served Over HTTP',
        body="""Act 1 - the setting lives in git
  git commit 2a6198d by Priya in engineering
  free-over 50.00

  the config server, asked for checkout-service:
    version 2a6198d, delivery.free-over 50.0

  the shop starts and fetches its settings.
    goods £48.00 delivery £4.99
    threshold £50.00
    banner: Free delivery on orders over £50.00""",
        narration=(
            'First, the setting is served over the network. The demo '
            'creates a git repository, and Priya in engineering commits '
            'a threshold of fifty pounds. [[slnc 250]] The demo starts '
            'the config server as a second Java program, with a port of '
            'its own. Asked for the settings of the application called '
            'checkout service, it answers with fifty, and names the '
            'commit it came from. [[slnc 250]] Then the shop starts. '
            'Before it takes a single order, it asks the config server '
            'for its settings. It quotes a forty-eight pound basket, and '
            'charges four ninety-nine for delivery, because forty-eight '
            'is under fifty. The banner across the top of the home page '
            'says free delivery on orders over fifty pounds.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='Committed, Not In Force',
        body="""Act 2 - marketing commits free-over 35.00
  git commit 64f6a92 by Maya in marketing

  the config server answers at once:
    version 64f6a92, delivery.free-over 35.0

  the running shop has not asked again:
    goods £48.00 delivery £4.99
    threshold £50.00

  committed, and served, but not in force.""",
        narration=(
            'Second, something the twin could never show. Maya in '
            'marketing commits thirty-five pounds. [[slnc 250]] The '
            'config server reads the repository on every request, so if '
            'anybody asks it, it answers thirty-five at once, from the '
            'new commit. [[slnc 250]] But the running shop does not ask. '
            'It fetched its settings once, as it started, and it keeps '
            'them. The same forty-eight pound basket still pays four '
            'ninety-nine, against fifty pounds. [[slnc 250]] The change '
            'is saved, and it is being served, but it is not in force. '
            'Nothing is broken. The shop simply has not been told to '
            'look again.'
        ),
    ),
    dict(
        key='06-three', kind='console', title='The Refresh',
        body="""Act 3 - POST /actuator/refresh, no restart
  the shop fetches again. what changed:
    config.client.version
    delivery.free-over

    goods £48.00 delivery FREE
    threshold £35.00

  the same running shop. restarts: 0.""",
        narration=(
            'Third, the refresh. A running Spring Boot program can be '
            'given a set of management pages by a library called '
            'Actuator. One of them is the refresh. The demo sends the '
            'running shop a request to that page, and the shop fetches '
            'its settings again. [[slnc 250]] It answers with the names '
            'of the settings that changed. Two of them: the commit its '
            'settings came from, and the threshold. [[slnc 250]] The '
            'next quote ships the forty-eight pound basket free, against '
            'thirty-five pounds. And it is the same running copy of the '
            'shop that started in act one. Zero restarts.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where The Value Lives',
        body=None,
        narration=(
            'Here is the whole arrangement, in words. There are three '
            'places, and the value passes through all of them. '
            '[[slnc 250]] First, a git repository, where every change is '
            'a commit with a name and a time on it. Second, the config '
            'server, a separate program that reads the repository every '
            'time it is asked. Third, the shop, which asks the server '
            'when it starts, and again only when it is told to refresh. '
            '[[slnc 250]] Inside the shop, the checkout\'s settings are '
            'rebuilt after a refresh. The promotion banner took its copy '
            'once, when the shop started. [[slnc 300]] The rule to '
            'remember is this: committed is not in force, and refreshed '
            'is not everywhere.'
        ),
    ),
    dict(
        key='08-surprise', kind='console', title='Two Thresholds, One Shop',
        body="""Act 4 - the refresh reached the checkout,
        and not the banner
    goods £48.00 delivery FREE
    threshold £35.00
    banner: Free delivery on orders over £50.00

  one running shop, two thresholds.

  after a restart of the shop:
    banner: Free delivery on orders over £35.00""",
        narration=(
            'Fourth, the surprise, and the headline of this video. After '
            'that refresh, the checkout quotes against thirty-five '
            'pounds. But the banner, in the very same running shop, '
            'still says free delivery on orders over fifty pounds. '
            '[[slnc 250]] The checkout\'s settings are marked to be '
            'refreshed, so the refresh threw them away and the next '
            'quote built them again from the new value. The banner read '
            'the same setting in the ordinary way, copied it into a '
            'field when the shop started, and nothing ever rebuilds it. '
            '[[slnc 250]] One shop, two thresholds, and no error '
            'anywhere. Only a restart of the shop brings the banner up '
            'to thirty-five pounds.'
        ),
    ),
    dict(
        key='09-code', kind='code', title='Two Ways To Read One Value',
        body="""// rebuilt after every refresh
@RefreshScope
@ConfigurationProperties(prefix = "delivery")
public class DeliverySettings {
    private BigDecimal freeOver;
}
// copied once, when the shop starts
@Component
public class PromotionBanner {
    public PromotionBanner(@Value(
      "${delivery.free-over}") BigDecimal v)
}""",
        narration=(
            'The difference between those two is a single annotation. '
            'The checkout\'s settings class carries refresh scope, which '
            'says: after a refresh, throw me away and build me again. '
            'The banner is an ordinary component. Its constructor asks '
            'for the threshold once, and keeps the text it made. '
            '[[slnc 250]] Neither line is unusual. Both would pass a '
            'code review. In the twin there was nothing that could hold '
            'on to an old copy, so the question never came up. In a '
            'Spring shop, every place that copies a changeable setting '
            'when the shop starts is a place a refresh will never reach.'
        ),
    ),
    dict(
        key='10-typo', kind='console', title='A Value Nobody Checked',
        body="""Act 5 - somebody commits -1 on Saturday
  git commit 6aaf4da by Maya in marketing
    version 6aaf4da, delivery.free-over -1
  the refresh answers 200.
  the next 5 quotes: 5 failed,
    each with HTTP status 500.

  git commit f68331f by Sam on call: 35.00
    goods £48.00 delivery FREE
    threshold £35.00""",
        narration=(
            'Fifth, the first part of the bill. On Saturday morning '
            'somebody commits minus one. The config server serves it '
            'without a word, because checking values is not its job. '
            '[[slnc 250]] The refresh answers two hundred, which means '
            'everything went fine. The shop\'s settings declare a range, '
            'five pounds to two hundred pounds, and Spring checks that '
            'range when it rebuilds the settings, which is on the next '
            'quote. The check fails, and there is nothing to fall back '
            'to. So the quote fails. And the next one. Five quotes, five '
            'failures, each with the status five hundred, which means '
            'the server broke. [[slnc 250]] The bad value never reached '
            'a customer. But neither did any quote, until Sam on call '
            'committed thirty-five pounds again and refreshed. And git '
            'kept the whole story: four commits, each with a name.'
        ),
    ),
    dict(
        key='11-down', kind='console', title='The Server Stops',
        body="""Act 6 - the config server stops
  a refresh of the running shop: 500.
  the running shop keeps what it fetched:
    goods £48.00 delivery FREE
    threshold £35.00

  a new shop, told to fail fast:
    refused to start
  a new shop, told the server is optional:
    goods £48.00 delivery £4.99
    threshold £50.00""",
        narration=(
            'Sixth, the second part of the bill. The demo stops the '
            'config server. [[slnc 250]] A shop that is already running '
            'does not notice, until it is told to refresh. Then the '
            'refresh fails with five hundred, and the shop carries on '
            'with what it already had: free delivery, against '
            'thirty-five pounds. [[slnc 250]] A shop that is only now '
            'starting has to decide. Spring calls the first choice fail '
            'fast: if the server cannot be reached, refuse to start. '
            'That copy refuses. The second choice marks the server as '
            'optional: start anyway, on the defaults packed inside the '
            'shop. That copy starts, quotes against fifty pounds, and '
            'charges four ninety-nine. The promotion is gone, and '
            'nothing reports an error.'
        ),
    ),
    dict(
        key='12-bill', kind='bullets', title='The Bill',
        body=['A commit is not in force', 'until someone sends a refresh.', '',
              'A refresh reaches only', 'the @RefreshScope objects.', '',
              'A range check with no fallback', 'turns a typo into 5 failed quotes.', '',
              'Server down: fail fast, or start', 'quietly on old defaults.'],
        narration=(
            'So here is the bill, in four lines. [[slnc 250]] A commit '
            'is not in force until somebody sends every running copy a '
            'refresh. A refresh reaches only the objects marked to be '
            'refreshed. A range check with nothing to fall back to turns '
            'a typo into an outage. And when the server is down, every '
            'new copy of the shop either refuses to start, or starts '
            'quietly on old values. [[slnc 250]] None of those is a bug '
            'in Spring. Each one is a decision the framework leaves to '
            'you.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['Got right: the whole shape.', 'Outside the code, read while running,', 'a type, a range, a history, a rollback.', '',
              'Left out: the fetch. Committed is', 'not in force until a refresh.', '',
              'Left out: a range check with no', 'fallback, and a server that is down.', '',
              'Headline: one refresh, two thresholds.'],
        narration=(
            'So what did the hand-built twin get right? The whole shape. '
            'The value lives outside the code. The checkout reads it '
            'while it runs. And it needs a type, a range, a history and '
            'a quick way back. All of that holds here, with the same '
            'basket and the same move from fifty pounds to thirty-five. '
            '[[slnc 300]] What it left out: the fetch. In the twin the '
            'checkout looked every time, so a change was in force at '
            'once. Here, a commit waits for a refresh. It left out a '
            'range check that fails every quote because nothing stands '
            'behind it, and a server that can really be down. '
            '[[slnc 300]] And the headline: one refresh, and one '
            'running shop believing two thresholds, because one of its '
            'objects kept the copy it made at startup.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Use a config server when many', 'services share settings with a history.', '',
              'Decide who sends the refresh.', 'Find every @Value that copies', 'a changeable setting.', '',
              'Give the range check a fallback.', 'Choose fail fast or optional', 'for every service, on purpose.'],
        narration=(
            'The verdict. Put settings in git behind a config server '
            'when many services share them, and the history of every '
            'change matters. [[slnc 250]] Then decide four things out '
            'loud, because Spring will not decide them for you. Decide '
            'who sends the refresh after a commit. Find every place that '
            'copies a changeable setting when the program starts. Give '
            'the range check something to fall back to. And choose, for '
            'every service, between refusing to start and starting on '
            'old values, knowing what each one costs.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Real: Spring Cloud Config Server 5.0.5', 'as a second Java process.', 'Spring Boot 4.1.1, Spring Cloud 2025.1.3.', '',
              'Real: a git repository, commits by JGit.', 'No container. No installed git.', '',
              'Too much: one or two copies,', 'a value that changes twice a year.', '',
              'Then: an environment variable.'],
        narration=(
            'What in this project is real? A real Spring Cloud Config '
            'Server, version five point zero point five, running as a '
            'separate Java program that the demo starts and stops. The '
            'shop is a real Spring Boot program, version four point one '
            'point one. The repository is a real git repository, written '
            'with a git library for Java, so nothing needs to be '
            'installed, and there is no container at all. [[slnc 300]] '
            'And when is this too much? If the shop runs as one or two '
            'copies, and the value changes a couple of times a year, an '
            'environment variable and a restart are simpler, and there '
            'is no server to keep alive.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Externalised Configuration with Spring Cloud Config. "
            '[[slnc 250]] If you take one sentence away, take this one: '
            'a commit is served at once, but it is in force only after a '
            'refresh, and only in the parts of the program that the '
            'refresh rebuilds. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository. [[slnc 300]] If you try one exercise, mark '
            'the banner to be refreshed, guess what it will say after '
            'the refresh, and then run it. [[slnc 300]] If this helped, '
            'a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
