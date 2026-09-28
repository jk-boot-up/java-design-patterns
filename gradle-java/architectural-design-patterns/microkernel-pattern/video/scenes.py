"""Scene definitions for the Microkernel teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Microkernel',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Microkernel pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A microkernel is a small '
            'core that knows only one thing: how to keep plugins, and run '
            'them. [[slnc 300]] Every actual feature lives in a plugin. '
            '[[slnc 600]] Think of a power strip. [[slnc 300]] The strip '
            'itself does very little. [[slnc 300]] It just gives power to '
            'whatever you plug in: a lamp, a fan, a charger. [[slnc 300]] '
            'You add or remove devices without rewiring the strip. [[slnc '
            '700]] In our online store, the checkout keeps gaining new '
            'features. [[slnc 300]] And every new feature means editing '
            'the same class. [[slnc 500]] In this video, we move those '
            'features into plugins. [[slnc 300]] We will add and remove a '
            'plugin while the shop is running, survive a broken plugin, '
            'and see why the order of plugins matters. [[slnc 300]] Then '
            'we will look at the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The checkout has a member', 'discount and a shipping fee.', '', 'Now marketing wants gift wrap,', 'then loyalty points,', 'then more.', '', 'Must we edit the checkout', 'every time?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The checkout already has '
            'a member discount, and a shipping fee. [[slnc 300]] Now the '
            'marketing team wants gift wrap. [[slnc 300]] Then loyalty '
            'points. [[slnc 300]] Then more. [[slnc 500]] So here is the '
            'question. [[slnc 300]] Must we edit the checkout every '
            'single time?'
        ),
    ),
    dict(
        key='03-mono', kind='console', title='Every Feature Inside',
        body="""ONE. Every feature inside.
  gift wrap is asked for.
  supported: false.

  to add it: edit the checkout,
  test all of it, release all of
  it.""",
        narration=(
            'First, the old way: every feature inside the checkout. '
            '[[slnc 400]] A customer asks for gift wrap. [[slnc 300]] The '
            'checkout does not support it, so the total stays the same. '
            '[[slnc 500]] To add gift wrap, we must edit the checkout. '
            '[[slnc 300]] Then test all of it again. [[slnc 300]] Then '
            'release all of it again.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A small core.', '', 'It knows one interface: Plugin.', 'It keeps plugins, starts and', 'stops them, and runs them.', '', 'Every feature is a plugin.'],
        narration=(
            'Now, the pattern. [[slnc 400]] There is a small core. [[slnc '
            '300]] It knows exactly one interface, called Plugin. [[slnc '
            '400]] The core keeps a list of plugins. [[slnc 300]] It '
            'starts them, stops them, and runs them. [[slnc 400]] And '
            'every feature is a plugin.'
        ),
    ),
    dict(
        key='05-core', kind='console', title='A Core And Plugins',
        body="""TWO. A core and plugins.
  plugins: member-discount,
  shipping-fee.
  10000 becomes 9500.

  the core knows one interface,
  nothing about discounts.""",
        narration=(
            'Second demo: a core with plugins. [[slnc 400]] The core has '
            'two plugins: a member discount, and a shipping fee. [[slnc '
            '400]] An order of one hundred dollars goes in. [[slnc 300]] '
            'It comes out at ninety-five dollars. [[slnc 500]] The core '
            'itself knows one interface. [[slnc 300]] It knows nothing '
            'about discounts or fees.'
        ),
    ),
    dict(
        key='06-add', kind='console', title='A New Feature, No Change',
        body="""THREE. A new feature.
  gift wrap registered while
  running: 9800, started.
  taken away again: stopped,
  9500.

  the core is unchanged.""",
        narration=(
            'Third demo: a new feature, with no change to the core. '
            '[[slnc 400]] While the shop is running, the gift wrap plugin '
            'is registered. [[slnc 300]] It starts, and the total becomes '
            'ninety-eight dollars. [[slnc 500]] Then gift wrap is removed '
            'again. [[slnc 300]] It stops, and the total goes back to '
            'ninety-five dollars. [[slnc 500]] The core was not changed '
            'at all.'
        ),
    ),
    dict(
        key='07-break', kind='console', title='A Plugin That Breaks',
        body="""FOUR. A plugin breaks.
  loyalty-points throws.
  the core records it.
  the others still ran:
  9500.""",
        narration=(
            'Fourth demo: a plugin that breaks. [[slnc 400]] The loyalty '
            'points plugin throws an error. [[slnc 400]] The core records '
            'the error, and carries on. [[slnc 300]] The other plugins '
            'still run. [[slnc 300]] The total is still ninety-five '
            'dollars. [[slnc 400]] One broken plugin did not stop the '
            'checkout.'
        ),
    ),
    dict(
        key='08-order', kind='console', title='Order Matters',
        body="""FIVE. Order matters.
  discount then fee: 9500.
  fee then discount: 9450.

  same plugins, different price.
  the core cannot know which is
  right.""",
        narration=(
            'Fifth demo: the order of plugins matters. [[slnc 400]] Apply '
            'the discount first, then the fee, and the total is '
            'ninety-five dollars. [[slnc 400]] Apply the fee first, then '
            'the discount, and the total is ninety-four dollars fifty. '
            '[[slnc 500]] The same two plugins, and a different price. '
            '[[slnc 400]] And the core has no way to know which order is '
            'right. [[slnc 300]] Someone has to decide that on purpose.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the interface offers one thing.
  plugins want three.

  grow it, and every plugin
  feels it; or plugins reach
  round the core.

  the total depends on what is
  installed, in some order.""",
        narration=(
            'Finally, the cost. [[slnc 400]] The plugin interface offers '
            'just one thing: adjust the total. [[slnc 400]] But plugins '
            "want more. [[slnc 300]] For example, the customer's country, "
            'or a line on the receipt. [[slnc 500]] If the interface '
            'grows, every plugin is affected. [[slnc 300]] If it does not '
            'grow, plugins start reaching around the core. [[slnc 500]] '
            "And one more cost. [[slnc 300]] A customer's total now "
            'depends on which plugins are installed, and in what order.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A Plugin or Extension interface', 'loaded by name or from a folder.', '', 'ServiceLoader in Java.', '', 'IDEs, browsers with extensions,', 'and build tools with plugins.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a Plugin or Extension interface, '
            'loaded by name or from a folder. [[slnc 300]] In Java, look '
            'for the Service Loader class. [[slnc 400]] You also meet it '
            'in everyday tools. [[slnc 300]] Code editors with '
            'extensions, web browsers with add-ons, and build tools with '
            'plugins. [[slnc 300]] And in systems built on OSGi, such as '
            'the Eclipse platform.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a microkernel when features', 'come and go, and different', 'customers or teams need different', 'sets. Keep the core tiny and the', 'interface stable. Decide the order', 'of plugins on purpose. Isolate a', 'failing plugin. Do not use it for', 'a system whose features never', 'change.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a microkernel when '
            'features come and go. [[slnc 300]] And when different '
            'customers or teams need different sets of features. [[slnc '
            '500]] Then follow four rules. [[slnc 300]] One. [[slnc 200]] '
            'Keep the core tiny, and the interface stable. [[slnc 300]] '
            'Two. [[slnc 200]] Decide the order of plugins on purpose. '
            '[[slnc 300]] Three. [[slnc 200]] Isolate a failing plugin, '
            'so it cannot stop the others. [[slnc 300]] And four. [[slnc '
            '200]] Do not use it for a system whose features never '
            'change.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If the features are few and fixed,', 'plain classes are simpler. A', 'plugin system costs an interface,', 'a lifecycle and a way to order', 'things, and pays off only when the', 'set of features truly varies.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If there are only a '
            'few features, and they never change, plain classes are '
            'simpler. [[slnc 400]] A plugin system costs an interface, a '
            'way to start and stop plugins, and a way to order them. '
            '[[slnc 300]] It only pays off when the set of features '
            'really does vary.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Microkernel pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A microkernel '
            'puts every feature in a plugin and keeps the core small, and '
            'the price is a narrow interface, and results that depend on '
            'what is installed. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Add a plugin that rounds the total to the '
            'nearest ten cents. [[slnc 300]] Then decide where in the '
            'order it should go. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
