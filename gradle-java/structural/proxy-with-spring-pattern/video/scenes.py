"""Scene definitions for the Proxy with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Proxy with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Proxy pattern in Java, using Spring Boot. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A proxy is a '
            'stand-in, placed in front of a real object, with exactly the '
            'same shape. [[slnc 300]] It can delay expensive work, or '
            'check who is asking, before passing the call on. [[slnc '
            '600]] In Spring, the proxy is generated for you, while the '
            'program runs. [[slnc 300]] And a separate piece of code, '
            'called an aspect, says what the proxy does on each call. '
            '[[slnc 700]] In our online store, the example is product '
            'images again. [[slnc 500]] By the end, you will hear the '
            'same two proxies come from Spring, instead of being written '
            'by hand. [[slnc 300]] And the two ways a call can slip past '
            'the generated proxy.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Proxy, the hand-built video,', 'puts a lazy proxy and a protection', 'proxy in front of a product image.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video builds on the plain Java Proxy video. [[slnc '
            '300]] If you have not seen it, start there. [[slnc 500]] '
            'That video puts two hand-written proxies in front of a '
            'product image. [[slnc 300]] One that loads lazily, and one '
            'that checks access. [[slnc 300]] And it combines the two. '
            '[[slnc 500]] This video uses the same example. [[slnc 300]] '
            'It does not teach the pattern again. [[slnc 300]] It shows '
            'what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot,', 'with its aspect support.', '', 'Spring generates the proxy class', 'at run time.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before any code, what is Spring Boot? [[slnc 400]] Spring is '
            'a framework, built around a container that creates your '
            'objects for you. [[slnc 300]] Those objects are called '
            'beans. [[slnc 500]] With its aspect support switched on, '
            'Spring wraps a bean in a generated proxy. [[slnc 300]] And '
            'it runs your extra code around each call. [[slnc 500]] And a '
            'promise. [[slnc 300]] Skipping this video loses none of the '
            'pattern. [[slnc 300]] The plain Java video teaches all of '
            'it.'
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
            'First demo: the bean is not your class. [[slnc 400]] Ask the '
            'container for the image catalogue. [[slnc 300]] What you '
            'receive is a generated subclass of it. [[slnc 500]] It is a '
            'proxy, wrapped around the real object. [[slnc 300]] And '
            'nobody wrote it.'
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
            'Second demo: protection, written once. [[slnc 400]] An admin '
            'asks for an image, and gets it. [[slnc 300]] A shopper asks, '
            'and is refused, before the real method even runs. [[slnc '
            '500]] The rule is not inside the catalogue. [[slnc 300]] It '
            'lives in an aspect.'
        ),
    ),
    dict(
        key='06-lazy', kind='console', title='Lazy Loading',
        body="""THREE. Lazy loading.
  after startup: 0 loaded.
  owner(): 0 loaded.
  first render: 1 loaded.""",
        narration=(
            'Third demo: lazy loading. [[slnc 400]] At startup, no images '
            'are loaded. [[slnc 300]] A cheap question, like who owns the '
            'catalogue, loads none. [[slnc 300]] The first time an image '
            'is shown, one is loaded. [[slnc 500]] It took two '
            'annotations. [[slnc 300]] Marking the class as lazy on its '
            'own is not enough.'
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
            'Fourth demo: one aspect, three screens. [[slnc 400]] The '
            'same aspect protects the catalogue, the order export, and '
            'the refund desk. [[slnc 300]] A shopper is refused by all '
            'three. [[slnc 500]] The rule exists in one place. [[slnc '
            '300]] In the plain Java version, each screen needed its own '
            'proxy class.'
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
            'Fifth demo: a call from inside. [[slnc 400]] A method inside '
            'the catalogue calls its own protected method directly. '
            '[[slnc 300]] That call never passes through the proxy. '
            '[[slnc 600]] From outside, the shopper is refused. [[slnc '
            '300]] But through that inside call, the shopper gets the '
            'image. [[slnc 500]] Nothing fails. [[slnc 300]] Nothing is '
            'logged. [[slnc 300]] The rule is silently switched off.'
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
            'Last demo: a final method. [[slnc 400]] A method marked '
            'final cannot be replaced by the generated subclass. [[slnc '
            '300]] So the proxy runs it on itself. [[slnc 300]] And the '
            "proxy holds none of the real object's data. [[slnc 500]] The "
            'rule is skipped, and the method crashes with a null pointer '
            'error. [[slnc 600]] Here, the failure is loud. [[slnc 300]] '
            'But if the method used no data, it would simply run '
            'unprotected, and nobody would notice.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['One aspect per rule.', '', 'Call protected methods from', 'outside the bean.', '', 'No final methods on proxied beans.', '', 'Test the refusal too.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Write each rule once, '
            'in an aspect. [[slnc 300]] Call protected methods from '
            'outside the bean, never from inside it. [[slnc 300]] Avoid '
            'final methods on beans that Spring wraps. [[slnc 300]] And '
            'test that refusals happen, not just that successes work.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Aspect with @Around.', '', '@Transactional or @Cacheable on', 'a method.', '', '$$SpringCGLIB$$ in a stack trace.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for an aspect with around advice. [[slnc 300]] '
            'Look for transactional or cacheable annotations on methods. '
            '[[slnc 300]] Or a class name in an error trace containing '
            'Spring C G LIB, the tool that generates the proxies.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Transactional method.', '', 'It is a proxy that opens and closes', 'the transaction around your call.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every method '
            'marked transactional. [[slnc 300]] That is a proxy, opening '
            'and closing a database transaction around your call.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1, with its', 'AspectJ starter.', '', 'No web server, no database.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] Spring '
            'Boot, version four point one point one, with its aspect '
            'support. [[slnc 300]] There is no web server, and no '
            'database.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's proxies", 'and the AspectJ advice.', '', 'Nothing depends on timing.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            "Everything is real: Spring's generated proxies, and the "
            'aspect code. [[slnc 300]] And nothing depends on timing, so '
            'every run gives the same result.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For one class with one rule, a', 'hand-written wrapper is easier', 'to read than an aspect.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For one class with '
            'one rule, a hand-written wrapper is easier to read than an '
            'aspect.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Remove the final keyword and', 'rerun the last act.'],
        narration=(
            "That's Proxy, with Spring. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Spring writes the '
            'proxy for you, but it only protects the calls that actually '
            'pass through it. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Remove the final keyword from that method. [[slnc '
            '300]] Then run the last demo again, and hear the rule work. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
