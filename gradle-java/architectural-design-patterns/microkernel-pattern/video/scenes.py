"""Scene definitions for the Microkernel teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Microkernel',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Microkernel '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'microkernel keeps a small core that only knows how to keep '
            'plugins and run them. Every feature lives in a plugin. '
            '[[slnc 350]] This is another project in the architecture '
            'category, whose subject is how a whole application is '
            'arranged, and who may depend on whom. In our online store, '
            'the checkout keeps gaining features, and every one means '
            'editing the same class. [[slnc 300]] By the end you will see '
            'a checkout that has to be edited for every new feature, see '
            'a core and plugins, see a plugin added and removed while '
            'running, see a broken plugin not stop the others, see the '
            'order of plugins change the price, and see the bill, which '
            'is a narrow interface and results that depend on what is '
            'installed.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The checkout has a member', 'discount and a shipping fee.', '', 'Now marketing wants gift wrap,', 'then loyalty points,', 'then more.', '', 'Must we edit the checkout', 'every time?'],
        narration=(
            'Here is the scenario. The checkout has a member discount and '
            'a shipping fee. Now the marketing team wants gift wrap, then '
            'loyalty points, then more. [[slnc 300]] The question: must '
            'we edit the checkout every time?'
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
            'First, every feature inside. Gift wrap is asked for, and the '
            'checkout does not support it. The total is unchanged. To add '
            'it, we must edit the checkout, test all of it again, and '
            'release all of it.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A small core.', '', 'It knows one interface: Plugin.', 'It keeps plugins, starts and', 'stops them, and runs them.', '', 'Every feature is a plugin.'],
        narration=(
            'The pattern. A small core. It knows one interface, called '
            'plugin. It keeps plugins, starts and stops them, and runs '
            'them. Every feature is a plugin.'
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
            'Second, a core and plugins. The core has two plugins: member '
            'discount and shipping fee. A total of ten thousand becomes '
            'ninety five hundred. The core knows one interface, and '
            'nothing about discounts or fees.'
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
            'Third, a new feature, with no change to the core. Gift wrap '
            'is registered while the system is running. It is started, '
            'and the total is ninety eight hundred. Then it is taken away '
            'again, and stopped, and the total goes back to ninety five '
            'hundred. The core was not changed.'
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
            'Fourth, a plugin that breaks. The loyalty points plugin '
            'throws an error. The core records it, and carries on. The '
            'other plugins still ran, and the total is ninety five '
            'hundred.'
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
            'Fifth, order matters. Discount then fee gives ninety five '
            'hundred. Fee then discount gives ninety four fifty. The same '
            'two plugins, and a different price. The core cannot know '
            'which is right.'
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
            'Last, the bill. The interface offers one thing: adjust a '
            "total. Plugins want more: the customer's country, and a line "
            'on the receipt. If the interface grows, every plugin feels '
            'it. If it does not, plugins reach around the core. And a '
            "customer's total is now decided by whichever plugins are "
            'installed, in some order.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A Plugin or Extension interface', 'loaded by name or from a folder.', '', 'ServiceLoader in Java.', '', 'IDEs, browsers with extensions,', 'and build tools with plugins.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'Plugin or Extension interface loaded by name or from a '
            'folder. ServiceLoader in Java. IDEs, browsers with '
            'extensions, and build tools with plugins. OSGi bundles and '
            'the Eclipse platform.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a microkernel when features', 'come and go, and different', 'customers or teams need different', 'sets. Keep the core tiny and the', 'interface stable. Decide the order', 'of plugins on purpose. Isolate a', 'failing plugin. Do not use it for', 'a system whose features never', 'change.'],
        narration=(
            'Here is my verdict, plainly. Use a microkernel when features '
            'come and go, and different customers or teams need different '
            'sets. Keep the core tiny and the interface stable. Decide '
            'the order of plugins on purpose. Isolate a failing plugin. '
            'Do not use it for a system whose features never change.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. Every number quoted comes from '
            "this program's own output. Nothing depends on a clock, so "
            'every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If the features are few and fixed,', 'plain classes are simpler. A', 'plugin system costs an interface,', 'a lifecycle and a way to order', 'things, and pays off only when the', 'set of features truly varies.'],
        narration=(
            'So when is it too much? If the features are few and fixed, '
            'plain classes are simpler. A plugin system costs an '
            'interface, a lifecycle and a way to order things, and pays '
            'off only when the set of features truly varies.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Microkernel. [[slnc 250]] If you take one sentence "
            'away, take this one: a microkernel puts every feature in a '
            'plugin and keeps the core small, and the price is a narrow '
            'interface and results that depend on what is installed. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add a plugin that rounds the total to the nearest ten cents, '
            'and decide where in the order it goes. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
