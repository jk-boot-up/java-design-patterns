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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Externalised Configuration pattern in Java, using a real '
            'configuration server from Spring Cloud. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A value that '
            "changes on someone else's timetable should live outside the "
            'program. [[slnc 300]] The program reads it while it runs. '
            '[[slnc 300]] So changing the value needs no rebuild, and no '
            'release. [[slnc 700]] In our online store, delivery is free '
            'on any basket over fifty pounds. [[slnc 300]] Marketing '
            'decides that number, not the programmers. [[slnc 300]] So it '
            'lives outside the shop, and marketing can change it to '
            'thirty-five pounds for the weekend. [[slnc 500]] By the end, '
            'you will hear a change that is saved, but not yet used. '
            '[[slnc 300]] A refresh that puts it in force, with no '
            'restart. [[slnc 300]] And one running shop that believes two '
            'different numbers at the same time.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Free delivery on baskets over £50.00.', 'Below that, delivery costs £4.99.', '',
              'Marketing decides the threshold.', 'Friday at 16:30 they want £35.00.', '',
              'The shop is a Spring Boot program.', 'Nobody wants a rebuild for one number.', '',
              'This time the value lives in git,', 'behind a real config server.'],
        narration=(
            'Here is the scenario. [[slnc 400]] Delivery is free on any '
            'basket over fifty pounds. [[slnc 300]] Below that, it costs '
            'four pounds ninety-nine. [[slnc 300]] Marketing decides the '
            'threshold. [[slnc 300]] And on Friday at half past four, '
            'they want thirty-five pounds for the weekend. [[slnc 600]] '
            'The plain Java version kept the threshold inside the same '
            'program. [[slnc 300]] And the checkout looked at it on every '
            'quote. [[slnc 500]] This time, the value lives in a git '
            'repository. [[slnc 300]] A real server hands it out over the '
            'network. [[slnc 300]] And the shop is a real Spring Boot '
            'program that fetches it. [[slnc 300]] That changes four '
            'things.'
        ),
    ),
    dict(
        key='03-words', kind='bullets', title="Spring Cloud Config's Words",
        body=['Head office keeps the price list.', 'Every change is signed in a ledger.', '',
              'A branch phones in as it opens.', 'It writes the prices on its board.', '',
              'git repository: the cabinet, the ledger', 'config server: the receptionist', 'refresh: phone head office again', '',
              '@RefreshScope: the board, rewritten'],
        narration=(
            'Spring Cloud Config brings a few words with it. [[slnc 400]] '
            'Think of a chain of bakeries. [[slnc 300]] Head office keeps '
            'the price list in a filing cabinet. [[slnc 300]] And every '
            'change is signed and dated in a ledger. [[slnc 500]] Each '
            'branch phones head office when it opens in the morning. '
            '[[slnc 300]] The receptionist reads out the prices. [[slnc '
            '300]] And the branch writes them on its board for the day. '
            "[[slnc 600]] In Spring's words, the cabinet with its ledger "
            'is a git repository. [[slnc 300]] Each signed change is a '
            'commit. [[slnc 300]] The receptionist is the config server. '
            '[[slnc 300]] Phoning in at opening time is fetching the '
            'settings at startup. [[slnc 300]] Telling a branch to phone '
            'again is called a refresh. [[slnc 300]] And the board that '
            'gets rewritten is an object marked with an annotation called '
            'refresh scope.'
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
            'First demo: the setting is served over the network. [[slnc '
            '400]] The demo creates a git repository. [[slnc 300]] Priya, '
            'in engineering, commits a threshold of fifty pounds. [[slnc '
            '600]] The demo starts the config server as a second Java '
            "program. [[slnc 300]] Asked for the checkout service's "
            'settings, it answers fifty, and names the commit it came '
            'from. [[slnc 600]] Then the shop starts. [[slnc 300]] Before '
            'taking any orders, it asks the config server for its '
            'settings. [[slnc 300]] It prices a forty-eight-pound basket, '
            'and charges four ninety-nine for delivery. [[slnc 300]] '
            'Because forty-eight is under fifty. [[slnc 300]] And the '
            'banner on the home page says: free delivery on orders over '
            'fifty pounds.'
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
            'Second demo: committed, but not in force. [[slnc 400]] Maya, '
            'in marketing, commits thirty-five pounds. [[slnc 500]] The '
            'config server reads the repository on every request. [[slnc '
            '300]] So if anyone asks, it answers thirty-five straight '
            'away. [[slnc 500]] But the running shop does not ask. [[slnc '
            '300]] It fetched its settings once, when it started, and '
            'keeps them. [[slnc 300]] The same forty-eight-pound basket '
            'still pays four ninety-nine. [[slnc 600]] The change is '
            'saved, and it is being served. [[slnc 300]] But it is not in '
            'force. [[slnc 300]] Nothing is broken. [[slnc 300]] The shop '
            'just has not been told to look again.'
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
            'Third demo: the refresh. [[slnc 400]] A running Spring Boot '
            'program can offer management pages, through a library called '
            'Actuator. [[slnc 300]] One of them is the refresh page. '
            '[[slnc 500]] The demo sends the running shop a request to '
            'that page. [[slnc 300]] And the shop fetches its settings '
            'again. [[slnc 300]] It reports which settings changed: the '
            'commit, and the threshold. [[slnc 600]] The next quote ships '
            'the forty-eight-pound basket free, against thirty-five '
            'pounds. [[slnc 300]] And it is the same running shop that '
            'started in the first demo. [[slnc 300]] No restarts.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where The Value Lives',
        body=None,
        narration=(
            'Here is the whole setup, in words. [[slnc 400]] There are '
            'three places, and the value passes through all of them. '
            '[[slnc 500]] First, a git repository, where every change is '
            'a commit, with a name and a time. [[slnc 300]] Second, the '
            'config server, a separate program that reads the repository '
            'every time it is asked. [[slnc 300]] Third, the shop, which '
            'asks the server when it starts, and again only when told to '
            "refresh. [[slnc 600]] Inside the shop, the checkout's "
            'settings are rebuilt after a refresh. [[slnc 300]] But the '
            'promotion banner took its copy once, when the shop started. '
            '[[slnc 600]] The rule to remember is this. [[slnc 300]] '
            'Committed is not in force. [[slnc 300]] And refreshed is not '
            'everywhere.'
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
            'Fourth demo, and this is the headline of the video. [[slnc '
            '400]] After the refresh, the checkout prices against '
            'thirty-five pounds. [[slnc 300]] But the banner, in the very '
            'same running shop, still says: free delivery over fifty '
            "pounds. [[slnc 600]] The checkout's settings are marked to "
            'be refreshed. [[slnc 300]] So the refresh threw them away, '
            'and the next quote rebuilt them with the new value. [[slnc '
            '500]] The banner read the same setting the ordinary way. '
            '[[slnc 300]] It copied it once, when the shop started. '
            '[[slnc 300]] And nothing ever rebuilds it. [[slnc 600]] One '
            'shop, two thresholds, and no error anywhere. [[slnc 300]] '
            'Only restarting the shop brings the banner up to '
            'thirty-five.'
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
            "[[slnc 500]] The checkout's settings class is marked with "
            'refresh scope. [[slnc 300]] That says: after a refresh, '
            'throw me away and build me again. [[slnc 500]] The banner is '
            'an ordinary component. [[slnc 300]] It asks for the '
            'threshold once, when it is created, and keeps the text it '
            'made. [[slnc 600]] Neither line is unusual. [[slnc 300]] '
            'Both would pass a code review. [[slnc 500]] In the plain '
            'Java version, nothing could hold on to an old copy. [[slnc '
            '300]] In a Spring shop, every place that copies a changeable '
            'setting at startup is a place a refresh will never reach.'
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
            'Fifth demo: a value nobody checked. [[slnc 400]] On Saturday '
            'morning, someone commits minus one. [[slnc 300]] The config '
            'server serves it without complaint, because checking values '
            'is not its job. [[slnc 600]] The refresh reports success. '
            "[[slnc 500]] But the shop's settings declare a range: five "
            'pounds to two hundred pounds. [[slnc 300]] Spring checks '
            'that range when it rebuilds the settings, on the next quote. '
            '[[slnc 300]] The check fails, and there is nothing to fall '
            'back to. [[slnc 300]] So the quote fails. [[slnc 300]] And '
            'the next one. [[slnc 300]] Five quotes, and five server '
            'errors. [[slnc 600]] The bad value never reached a customer. '
            '[[slnc 300]] But neither did any quote. [[slnc 300]] Until '
            'Sam, on call, committed thirty-five pounds again, and '
            'refreshed. [[slnc 500]] And git kept the whole story: four '
            'commits, each with a name.'
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
            'Sixth demo: the config server stops. [[slnc 500]] A shop '
            'that is already running does not notice, until it is told to '
            'refresh. [[slnc 300]] Then the refresh fails. [[slnc 300]] '
            'And the shop carries on with what it already had: '
            'thirty-five pounds. [[slnc 600]] A shop that is only now '
            'starting must choose. [[slnc 500]] The first choice is '
            'called fail fast. [[slnc 300]] If the server cannot be '
            'reached, refuse to start. [[slnc 300]] That copy refuses. '
            '[[slnc 500]] The second choice marks the server as optional. '
            '[[slnc 300]] Start anyway, using the defaults packed inside '
            'the shop. [[slnc 300]] That copy starts, prices against '
            'fifty pounds, and charges four ninety-nine. [[slnc 300]] The '
            'promotion is gone. [[slnc 300]] And nothing reports an '
            'error.'
        ),
    ),
    dict(
        key='12-bill', kind='bullets', title='The Bill',
        body=['A commit is not in force', 'until someone sends a refresh.', '',
              'A refresh reaches only', 'the @RefreshScope objects.', '',
              'A range check with no fallback', 'turns a typo into 5 failed quotes.', '',
              'Server down: fail fast, or start', 'quietly on old defaults.'],
        narration=(
            'So here is the bill, in four points. [[slnc 500]] One. '
            '[[slnc 200]] A commit is not in force until someone tells '
            'every running copy to refresh. [[slnc 400]] Two. [[slnc '
            '200]] A refresh only reaches the objects marked to be '
            'refreshed. [[slnc 400]] Three. [[slnc 200]] A range check '
            'with nothing to fall back on turns a typo into an outage. '
            '[[slnc 400]] Four. [[slnc 200]] When the server is down, '
            'every new copy of the shop either refuses to start, or '
            'quietly starts on old values. [[slnc 600]] None of these is '
            'a bug in Spring. [[slnc 300]] Each one is a decision the '
            'framework leaves to you.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['Got right: the whole shape.', 'Outside the code, read while running,', 'a type, a range, a history, a rollback.', '',
              'Left out: the fetch. Committed is', 'not in force until a refresh.', '',
              'Left out: a range check with no', 'fallback, and a server that is down.', '',
              'Headline: one refresh, two thresholds.'],
        narration=(
            'So what did the plain Java version get right? [[slnc 400]] '
            'The whole shape. [[slnc 300]] The value lives outside the '
            'code. [[slnc 300]] The checkout reads it while running. '
            '[[slnc 300]] And it needs a type, a range, a history, and a '
            'quick way back. [[slnc 300]] All of that holds here. [[slnc '
            '600]] What it left out was the fetch. [[slnc 300]] In the '
            'plain version, the checkout looked every time, so a change '
            'applied at once. [[slnc 300]] Here, a commit waits for a '
            'refresh. [[slnc 500]] It also left out a range check with '
            'nothing behind it, and a server that can really be down. '
            '[[slnc 600]] And the headline. [[slnc 300]] One refresh, and '
            'one running shop believing two thresholds. [[slnc 300]] '
            'Because one of its objects kept the copy it made at startup.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Use a config server when many', 'services share settings with a history.', '',
              'Decide who sends the refresh.', 'Find every @Value that copies', 'a changeable setting.', '',
              'Give the range check a fallback.', 'Choose fail fast or optional', 'for every service, on purpose.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Put settings in git, '
            'behind a config server, when many services share them, and '
            "every change's history matters. [[slnc 600]] Then decide "
            'four things, because Spring will not decide them for you. '
            '[[slnc 500]] Decide who sends the refresh after a commit. '
            '[[slnc 300]] Find every place that copies a changeable '
            'setting at startup. [[slnc 300]] Give the range check '
            'something to fall back on. [[slnc 300]] And for every '
            'service, choose between refusing to start, and starting on '
            'old values, knowing what each costs.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Real: Spring Cloud Config Server 5.0.5', 'as a second Java process.', 'Spring Boot 4.1.1, Spring Cloud 2025.1.3.', '',
              'Real: a git repository, commits by JGit.', 'No container. No installed git.', '',
              'Too much: one or two copies,', 'a value that changes twice a year.', '',
              'Then: an environment variable.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'config server is real: Spring Cloud Config Server, version '
            'five point zero point five. [[slnc 300]] It runs as a '
            'separate Java program that the demo starts and stops. [[slnc '
            '300]] The shop is a real Spring Boot program, version four '
            'point one point one. [[slnc 300]] And the repository is a '
            'real git repository, written by a Java git library. [[slnc '
            '300]] So nothing needs installing, and there is no container '
            'at all. [[slnc 600]] So, when is this too much? [[slnc 300]] '
            'If the shop runs as one or two copies, and the value changes '
            'a couple of times a year, an environment variable and a '
            'restart are simpler. [[slnc 300]] And there is no server to '
            'keep alive.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Externalised Configuration, with Spring Cloud Config. "
            '[[slnc 400]] If you remember one sentence, make it this one. '
            '[[slnc 300]] A commit is served at once, but it is only in '
            'force after a refresh, and only in the parts of the program '
            'the refresh rebuilds. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Mark the banner to be refreshed too. [[slnc '
            '300]] Guess what it will say after a refresh, and then run '
            'it. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
