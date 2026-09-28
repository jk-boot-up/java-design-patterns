"""Scene definitions for the API Gateway with Spring Cloud Gateway teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='API Gateway with Spring Cloud Gateway',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the API '
            'Gateway pattern, in Java, using Spring Cloud Gateway. [[slnc '
            '300]] This video is presented by Jayasekhar Konduru. [[slnc '
            '600]] First, a simple definition. [[slnc 300]] An API '
            'gateway is one front door for many services. [[slnc 300]] '
            'Every request comes in through that one door, and the '
            'gateway sends it on to the right service. [[slnc 600]] Think '
            "of a hotel with one front desk. [[slnc 300]] You don't phone "
            'the kitchen, the laundry, and the spa, one by one. [[slnc '
            '300]] You call the front desk, and they pass your request to '
            'the right place. [[slnc 700]] Now, our online store. [[slnc '
            '300]] The mobile app needs four services: [[slnc 200]] the '
            'catalogue, [[slnc 150]] pricing, [[slnc 150]] inventory, '
            '[[slnc 150]] and recommendations. [[slnc 500]] Without a '
            'gateway, the app has to know all four addresses. [[slnc '
            '300]] With a gateway, it knows just one. [[slnc 700]] In '
            'this video, Spring Cloud Gateway is that front desk. [[slnc '
            '300]] We will watch it route real requests, check a token, '
            'and deal with a slow service. [[slnc 300]] And we will see '
            'two things it does not do for you.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['API Gateway, the hand-built video,', 'puts one service in front of four,', 'so the app makes one call.', '', 'It merges four answers into one page.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built API Gateway video. [[slnc 400]] That '
            'one builds the gateway from scratch, in plain Java. [[slnc '
            '300]] It also merges four answers into one product page. '
            '[[slnc 500]] If you are new to the pattern, watch that one '
            'first. [[slnc 400]] Here, we keep the same online store. '
            "[[slnc 300]] We won't teach the pattern again. [[slnc 300]] "
            'Instead, we ask one question. [[slnc 300]] What does a real '
            'framework do with it?'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: Spring Boot, and', 'Spring Cloud Gateway.', '', 'The gateway runs on a reactive', 'web server, Netty.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'So, what is Spring Cloud Gateway? [[slnc 400]] It is a '
            "ready-made gateway, built on Spring. [[slnc 300]] You don't "
            'write the forwarding code yourself. [[slnc 300]] You '
            'describe two things. [[slnc 300]] Routes, which say: this '
            'path goes to that service. [[slnc 300]] And filters, which '
            'change a request on its way through. [[slnc 500]] It runs on '
            'a fast web server called Netty. [[slnc 500]] One promise '
            'before we go on. [[slnc 300]] If you skip this video, you '
            'lose none of the pattern. [[slnc 300]] This one is about the '
            'tool.'
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
            "Let's look at the first thing it does. [[slnc 300]] One "
            'address. [[slnc 500]] The app sends four requests, all to '
            'the gateway. [[slnc 300]] Each one has a different path. '
            '[[slnc 300]] Slash api, slash catalogue, goes to the '
            'catalogue service. [[slnc 300]] Slash api, slash pricing, '
            'goes to pricing. [[slnc 300]] And the same for inventory and '
            'recommendations. [[slnc 500]] So the app knows one address. '
            "[[slnc 300]] The gateway's routing table knows the rest. "
            '[[slnc 400]] And this is not a simulation. [[slnc 200]] '
            'These are real HTTP requests, over real network connections.'
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
            'Second, the gateway can change a request as it passes '
            'through. [[slnc 400]] The app asked for slash api, slash '
            'pricing, slash products. [[slnc 300]] But the pricing '
            'service received just slash products. [[slnc 500]] Why? '
            '[[slnc 300]] The front part of the path is only for the '
            'outside world. [[slnc 300]] The gateway strips it off, so '
            'the services never need to know about it. [[slnc 400]] It '
            'also adds a header, a small label on the request, that says: '
            'this came through the gateway.'
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
            'Third, security. [[slnc 300]] A token is like a wristband at '
            'a concert. [[slnc 300]] No wristband, no entry. [[slnc 500]] '
            'We send a request with no token. [[slnc 300]] The gateway '
            'answers four hundred and one, which means: not allowed. '
            '[[slnc 300]] We try a different route. [[slnc 200]] Same '
            'answer. [[slnc 400]] And here is the key number. [[slnc '
            '300]] Zero requests reached a service. [[slnc 300]] The '
            'gateway stopped them all at the door. [[slnc 400]] Now we '
            'add a token, and the request goes through. [[slnc 500]] The '
            'important point? [[slnc 300]] The check is written once, in '
            'the gateway. [[slnc 300]] In the hand-built version, every '
            'service had to repeat it.'
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
            'Fourth, what happens when a service goes down? [[slnc 400]] '
            'We stop the recommendations service. [[slnc 300]] Calls to '
            'recommendations now fail. [[slnc 300]] But calls to the '
            'catalogue still work. [[slnc 300]] One broken service does '
            'not break the others. [[slnc 500]] Now, listen carefully to '
            'the error code. [[slnc 300]] The gateway answers five '
            'hundred. [[slnc 300]] Not five oh three. [[slnc 400]] Five '
            'hundred means: something is broken inside. [[slnc 300]] Five '
            'oh three means: that service is not available right now. '
            '[[slnc 400]] So the app sees what looks like a bug in the '
            'shop, when really a service is just down. [[slnc 400]] If '
            'that difference matters to you, you have to map it yourself.'
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
            'Fifth, something a gateway does not do. [[slnc 400]] A '
            'product page needs three services. [[slnc 300]] The app '
            'makes three calls. [[slnc 300]] And three calls reach the '
            'services. [[slnc 500]] The gateway forwards requests. [[slnc '
            '300]] It does not merge the answers. [[slnc 500]] Remember '
            'the partner video? [[slnc 300]] There, the gateway combined '
            'four answers into one page. [[slnc 300]] With Spring Cloud '
            'Gateway, that combining is a separate job, and you write the '
            'code for it.'
        ),
    ),
    dict(
        key='09-slow', kind='console', title='A Slow Service',
        body="""SIX. Slow.
  pricing never answers.

  the gateway answers: 504.

  the wait is a setting.""",
        narration=(
            'And last, a slow service. [[slnc 400]] Imagine the pricing '
            'service never answers at all. [[slnc 300]] Without '
            'protection, the app would just wait, and wait. [[slnc 500]] '
            'Here, the gateway has a timeout. [[slnc 300]] When the time '
            "is up, it answers on the service's behalf, with five oh "
            'four, which means gateway timeout. [[slnc 400]] The app gets '
            'a clear answer, instead of hanging. [[slnc 400]] So, one '
            'simple rule. [[slnc 300]] Set a timeout on every route.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Route and filter at the edge.', '', 'Set a timeout on every route.', '', 'Decide what a dead service', 'looks like.', '', 'Compose elsewhere.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use Spring Cloud '
            'Gateway at the edge of your system. [[slnc 300]] Let it do '
            'routing, token checks, headers and limits. [[slnc 500]] Then '
            'remember three things. [[slnc 300]] One. [[slnc 200]] Set a '
            'timeout on every route. [[slnc 300]] Two. [[slnc 200]] '
            'Decide what a dead service should look like to the app. '
            '[[slnc 300]] And three. [[slnc 200]] Merging answers happens '
            'somewhere else, in code you write.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['RouteLocatorBuilder with .route.', '', 'spring.cloud.gateway in configuration.', '', 'A GlobalFilter bean.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for three clues. [[slnc 300]] A route locator '
            'builder, with calls to route. [[slnc 300]] Settings that '
            'start with spring cloud gateway. [[slnc 300]] Or a global '
            'filter bean. [[slnc 300]] See any of those, and you are '
            'looking at a gateway.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['The public edge of most', 'Spring-based platforms.'],
        narration=(
            'Where have you met this before? [[slnc 300]] At the front '
            'door of most Spring based platforms. [[slnc 300]] Every '
            'request you send them passes through one.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Spring Cloud 2025.1.3.', '', 'Gateway 5.0.3, on Netty.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] Spring Cloud '
            'twenty twenty five point one point three. [[slnc 300]] And '
            'the gateway itself, five point zero point three, running on '
            'Netty.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: real sockets,', 'real HTTP, and the real gateway.', '', 'The four services are small', 'JDK servers on free ports.', 'The slow one is held at a gate.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything in it is real. [[slnc 300]] Real network '
            'connections, real HTTP, and the real gateway. [[slnc 400]] '
            'The four services are small Java servers, each on its own '
            'free port. [[slnc 300]] And the slow service is held back on '
            'purpose, so we can watch the timeout happen.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For one service, a gateway is a hop', 'that adds nothing.'],
        narration=(
            'So, when is a gateway too much? [[slnc 400]] If you only '
            'have one service, a gateway is just an extra hop. [[slnc '
            '300]] It adds work, and gives you nothing back.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Map the 500 for a refused', 'connection to a 503.'],
        narration=(
            "That's the API Gateway pattern, with Spring Cloud Gateway. "
            '[[slnc 400]] If you remember one sentence, make it this one. '
            '[[slnc 300]] Spring Cloud Gateway routes and checks real '
            'requests, but merging the answers is still your job. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 400]] '
            'Here is one exercise to try. [[slnc 300]] When a service '
            'refuses the connection, make the gateway answer five oh '
            'three, instead of five hundred. [[slnc 500]] If this helped, '
            'a like really does help other people find it. [[slnc 300]] '
            "And subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]

# Slide settings for the standard videokit renderer (tools/videokit), which
# draws every scene above; this project needs no slide code of its own.
VIDEO = dict(
    footer='API Gateway with Spring Cloud Gateway  ·  Java 21',
    highlight=dict(
        quote=['It usually wins'],
        code_return=['return', 'rule.check'],
        console_amber=['NOTHING', 'FORCED', 'AND THE'],
        console_rose=['Architecture Violation'],
    ),
    poster=dict(
        headline=[('API GATEWAY', 'text'), ('WITH SPRING CLOUD', 'accent')],
        # No token versus a token -- both real lines from the project.
        before=dict(code='no token', note='401 and 0 requests reached',
                    tag='STOPPED AT THE EDGE', colour='red'),
        after=dict(code='a bearer token', note='200 from the service',
                   tag='ROUTED', colour='green'),
        taglines=[('One address, one token check.', 'text'),
                  ('Real HTTP, real routes.', 'gold')],
    ),
)
