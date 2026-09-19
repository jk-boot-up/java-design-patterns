"""Scene definitions for the API Gateway with Spring Cloud Gateway teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='API Gateway with Spring Cloud Gateway',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the API Gateway '
            'pattern with Spring Cloud Gateway, in Java, and it is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] It '
            'is the framework version of the API Gateway video. That one '
            'put one gateway in front of catalogue, pricing, inventory '
            'and recommendations, so the mobile app made one call to one '
            'address and lost nothing when a feature service went down. '
            'This one shows the same idea inside Spring Cloud Gateway. '
            '[[slnc 350]] The plain definition, in short: in Spring Cloud '
            'Gateway, a gateway is a routing table of paths and services, '
            'with filters applied to each request on the way through. '
            '[[slnc 300]] By the end you will see a real gateway route '
            'real HTTP to four services, strip a prefix, check a token '
            'once, and time out a slow service, then see what it does not '
            'do: merge responses, and report a dead service as a 503.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['API Gateway, the hand-built video,', 'puts one service in front of four,', 'so the app makes one call.', '', 'It merges four answers into one page.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the API Gateway video. If you have not '
            'seen it, start there. It puts one service in front of '
            'catalogue, pricing, inventory and recommendations, so the '
            'app makes one call, and it merges the four answers into one '
            'product page. [[slnc 300]] This one uses the same example. '
            'It does not teach the pattern again. It shows what Spring '
            'Cloud Gateway does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: Spring Boot, and', 'Spring Cloud Gateway.', '', 'The gateway runs on a reactive', 'web server, Netty.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Cloud Gateway is. '
            'Spring Cloud Gateway is a gateway built on Spring. You '
            'describe routes, a path and a destination, and filters, and '
            'it forwards real HTTP requests on a reactive server. [[slnc '
            '300]] And a promise: skipping this video loses none of the '
            'pattern. The hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-one', kind='console', title='One Address, Four Services',
        body="""ONE. One address.
  /api/catalogue -> catalogue
  /api/pricing -> pricing
  /api/inventory -> inventory
  /api/recommendations ->
  recommendations

  one address for the client.""",
        narration=(
            'First, one address. The client calls the gateway with four '
            'different paths, and each goes to a different service: '
            'catalogue, pricing, inventory and recommendations. The '
            'client knows one address. The routing table knows the rest. '
            'All of it is real HTTP over real sockets.'
        ),
    ),
    dict(
        key='05-strip', kind='console', title='The Prefix Is Stripped',
        body="""TWO. Stripped.
  the client asked for
  /api/pricing/products/MUG-BLUE.

  pricing saw
  /products/MUG-BLUE,
  with a source header.""",
        narration=(
            'Second, the gateway rewrites. The client asked for slash api '
            'slash pricing slash products. The pricing service was asked '
            'for only slash products. The public prefix is gone, so the '
            'services never need to know about it. A header tells them '
            'the request came through the gateway.'
        ),
    ),
    dict(
        key='06-token', kind='console', title='One Token Check, For Every Route',
        body="""THREE. A token.
  no token: 401.
  other route, no token: 401.

  reached a service: 0.

  with a token: 200.""",
        narration=(
            'Third, one token check. Without a token, the gateway answers '
            'four hundred and one, on any route. Zero requests reach a '
            'service. With a token, the request goes through. [[slnc '
            '300]] The check is written once. In the hand built version, '
            'each service repeated it.'
        ),
    ),
    dict(
        key='07-down', kind='console', title='One Service Down',
        body="""FOUR. One down.
  recommendations: 500.
  catalogue: still 200.

  but 500, not 503: it looks
  like a bug in the shop.""",
        narration=(
            'Fourth, a service goes down. Recommendations answers with an '
            'error, and catalogue still works. The failure stays on its '
            'own route. But look at the status. It is five hundred, not '
            'five oh three. A refused connection is reported as an '
            'internal server error. To a client, that looks like a bug in '
            'the shop. [[slnc 300]] Map it if the difference matters.'
        ),
    ),
    dict(
        key='08-compose', kind='console', title='A Gateway Forwards',
        body="""FIVE. Forwards.
  a product page: 3 services,
  3 client calls,
  3 reached services.

  merging is composition code.""",
        narration=(
            'Fifth, what a gateway does not do. A product page that needs '
            'three services still takes three calls, and three reach the '
            'services. The gateway forwards. It does not merge. [[slnc '
            "300]] The partner video's gateway merged four answers into "
            'one page. Here that is a separate job, for code you write.'
        ),
    ),
    dict(
        key='09-slow', kind='console', title='A Slow Service',
        body="""SIX. Slow.
  pricing never answers.

  the gateway answers: 504.

  the wait is a setting.""",
        narration=(
            'Last, a slow service. Pricing never answers. After the '
            'timeout in the settings, the gateway answers for it with a '
            'five oh four, gateway timeout. The client is not left '
            'hanging. Set that timeout on every route.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Route and filter at the edge.', '', 'Set a timeout on every route.', '', 'Decide what a dead service', 'looks like.', '', 'Compose elsewhere.'],
        narration=(
            'My verdict, plainly. Use it for routing, authentication, '
            'headers and limits at the edge. Set a timeout on every '
            'route. Decide what a dead service looks like to clients. And '
            'compose responses somewhere else, or in a filter you write.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['RouteLocatorBuilder with .route.', '', 'spring.cloud.gateway in configuration.', '', 'A GlobalFilter bean.'],
        narration=(
            'How do you recognise this in code you did not write? A route '
            'locator builder with route calls. Settings under spring '
            'cloud gateway. Or a global filter bean.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['The public edge of most', 'Spring-based platforms.'],
        narration=(
            'You have met this at the public edge of most Spring based '
            'platforms.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Spring Cloud 2025.1.3.', '', 'Gateway 5.0.3, on Netty.'],
        narration=(
            'For the record. Spring Boot four point one point one. Spring '
            'Cloud twenty twenty five point one point three. Gateway five '
            'point zero point three, on Netty.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: real sockets,', 'real HTTP, and the real gateway.', '', 'The four services are small', 'JDK servers on free ports.', 'The slow one is held at a gate.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: real sockets, real HTTP, and the real '
            'gateway. The four services are small JDK servers on free '
            'ports, and the slow one is held at a gate.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For one service, a gateway is a hop', 'that adds nothing.'],
        narration=(
            'So when is it too much? For one service, a gateway is a hop '
            'that adds nothing.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Map the 500 for a refused', 'connection to a 503.'],
        narration=(
            "That's API Gateway with Spring Cloud Gateway. [[slnc 250]] "
            'If you take one sentence away, take this one: Spring Cloud '
            'Gateway routes and filters real requests, and composing them '
            'is still yours to write. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository. [[slnc 300]] If you try one exercise, '
            'map the five hundred for a refused connection to a five oh '
            'three. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
