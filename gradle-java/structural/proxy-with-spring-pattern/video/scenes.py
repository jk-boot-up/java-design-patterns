"""Scene definitions for the Proxy with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Proxy with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Proxy pattern '
            'with Spring Boot, in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] It is the framework '
            'version of the Proxy video. That one stood a lazy proxy and '
            'a protection proxy in front of a product image, each written '
            'by hand, and composed the two. This one shows the same idea '
            'inside Spring Boot. [[slnc 350]] The plain definition, in '
            'short: in Spring, the proxy is generated at run time around '
            'a bean, and an aspect says what it does on each call. [[slnc '
            '300]] By the end you will see the same two proxies come from '
            'Spring instead of by hand, then see the two ways a call '
            'slips past the generated proxy.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Proxy, the hand-built video,', 'puts a lazy proxy and a protection', 'proxy in front of a product image.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Proxy video. If you have not seen it, '
            'start there. It puts a lazy proxy and a protection proxy in '
            'front of a product image, each written by hand, and composes '
            'the two. [[slnc 300]] This one uses the same example. It '
            'does not teach the pattern again. It shows what Spring Boot '
            'does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot,', 'with its aspect support.', '', 'Spring generates the proxy class', 'at run time.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates your '
            'objects. With aspect support, it wraps a bean in a generated '
            'proxy, and runs your advice around each call. [[slnc 300]] '
            'And a promise: skipping this video loses none of the '
            'pattern. The hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-proxy', kind='console', title='The Bean Is Not Your Class',
        body="""ONE. Not your class.
  is a generated proxy: true
  a subclass of ImageCatalogue:
  true
  the class wrapped:
  ImageCatalogue""",
        narration=(
            'First, look at what you are given. Ask the container for the '
            'image catalogue, and you receive a generated subclass. It is '
            'a proxy, wrapped around the real object. Nobody wrote it.'
        ),
    ),
    dict(
        key='05-protect', kind='console', title='Protection, Written Once',
        body="""TWO. Protection.
  admin: full-resolution pixels
  shopper: refused:
  render needs CATALOG_ADMIN
  but the caller is SHOPPER""",
        narration=(
            'Second, protection. An admin asks for the image and gets it. '
            'A shopper asks and is refused, before the real method runs. '
            'The rule is not inside the catalogue. It is in an aspect.'
        ),
    ),
    dict(
        key='06-lazy', kind='console', title='Lazy Loading',
        body="""THREE. Lazy loading.
  after startup: 0 loaded.
  owner(): 0 loaded.
  first render: 1 loaded.""",
        narration=(
            'Third, the lazy proxy. At startup, no images are loaded. A '
            'cheap question, who owns the catalogue, loads none. The '
            'first render loads one. [[slnc 300]] It took two '
            'annotations. Lazy on the class alone is not enough.'
        ),
    ),
    dict(
        key='07-cross', kind='console', title='One Aspect, Three Screens',
        body="""FOUR. One aspect.
  catalogue: refused
  export: refused
  refunds: refused

  the check was written once.""",
        narration=(
            'Fourth, the payoff. The same aspect protects the catalogue, '
            'the order export and the refund desk. The rule exists in one '
            'place. [[slnc 300]] In the hand-built project, each screen '
            'needed its own proxy class.'
        ),
    ),
    dict(
        key='08-this', kind='console', title='A Call On this',
        body="""FIVE. On this.
  from outside: refused.
  renderThroughThis: the
  shopper got the image.

  nothing was logged.""",
        narration=(
            'Fifth, the first failure. A method inside the catalogue '
            'calls its own protected method, on this. That call never '
            'goes through the proxy. From outside, the shopper is '
            'refused. Through this, the shopper gets the image. [[slnc '
            '300]] Nothing fails, and nothing is logged. The rule is '
            'silently off.'
        ),
    ),
    dict(
        key='09-final', kind='console', title='A Final Method',
        body="""SIX. A final method.
  renderFinal, a shopper:
  NullPointerException: the
  proxy instance has no fields
  of its own.""",
        narration=(
            'Last, a final method. The generated subclass cannot override '
            'it, so the proxy runs it on itself, and the proxy has no '
            'fields of its own. The rule is skipped, and the method fails '
            'with a null pointer. [[slnc 300]] The failure is loud here. '
            'Where the method touches no field, it would just be silently '
            'unprotected.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['One aspect per rule.', '', 'Call protected methods from', 'outside the bean.', '', 'No final methods on proxied beans.', '', 'Test the refusal too.'],
        narration=(
            'My verdict, plainly. Write each rule once, in an aspect. '
            'Call protected methods from outside the bean. Avoid final '
            'methods on proxied beans. And test the refusal, not just the '
            'success.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Aspect with @Around.', '', '@Transactional or @Cacheable on', 'a method.', '', '$$SpringCGLIB$$ in a stack trace.'],
        narration=(
            'How do you recognise this in code you did not write? An '
            'aspect with around advice. A transactional or cacheable '
            'annotation on a method. Or a class name in a stack trace '
            'with spring c g lib in it.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Transactional method.', '', 'It is a proxy that opens and closes', 'the transaction around your call.'],
        narration=(
            'You have met this in every transactional method. It is a '
            'proxy that opens and closes the transaction around your '
            'call.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1, with its', 'AspectJ starter.', '', 'No web server, no database.'],
        narration=(
            'For the record. Spring Boot four point one point one, with '
            'its AspectJ starter. No web server, and no database.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's proxies", 'and the AspectJ advice.', '', 'Nothing depends on timing.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            "Everything is real: Spring's proxies and the aspect advice. "
            'Nothing depends on timing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For one class with one rule, a', 'hand-written wrapper is easier', 'to read than an aspect.'],
        narration=(
            'So when is it too much? For one class with one rule, a hand '
            'written wrapper is easier to read than an aspect.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Remove the final keyword and', 'rerun the last act.'],
        narration=(
            "That's Proxy with Spring. [[slnc 250]] If you take one "
            'sentence away, take this one: Spring writes the proxy for '
            'you, and covers only the calls that come through it. [[slnc '
            '350]] The full source, the written notes, the diagrams and '
            'an animated walkthrough are all in the repository. [[slnc '
            '300]] If you try one exercise, remove the final keyword, and '
            'rerun the last act. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
