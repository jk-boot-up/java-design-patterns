"""Scene definitions for the Balking teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Balking',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Balking pattern '
            'in Java, and it is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] The plain definition: balking means an '
            'action is only carried out if the object is in the right '
            'state. If it is not, the call returns at once, instead of '
            'waiting, or failing. [[slnc 350]] This is another project in '
            'the concurrency category, whose subject is how threads share '
            'work and state without corrupting either. In our online '
            "store, the thing that saves itself is a customer's basket "
            'draft. [[slnc 300]] By the end you will see a draft save '
            'five times for one edit, see it balk when nothing changed '
            'and when a save is already running, see an edit during a '
            'save lost by a careless version and kept by a careful one, '
            'see the caller told, and see the bill, which is that a '
            'balked request is not done.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=["A customer's basket draft is", 'saved by a timer, and by a Save', 'button.', '', 'Sometimes nothing has changed.', 'Sometimes a save is running.', '', 'What should save do?'],
        narration=(
            "Here is the scenario. A customer's basket draft is saved by "
            'a timer every few seconds, and by a Save button. Sometimes '
            'nothing has changed. Sometimes a save is already running. '
            '[[slnc 300]] The question: what should save do then?'
        ),
    ),
    dict(
        key='03-always', kind='console', title='Save Every Time',
        body="""ONE. Every time.
  one edit.
  the timer fires 5 times.
  writes: 5.

  four wrote what was there.""",
        narration=(
            'First, save every time it is asked. One edit, and the '
            'autosave timer fires five times. Five writes. Four of them '
            'wrote exactly what was already there.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Check the state at the door.', '', 'If the action is not needed, or', 'not possible now, return at once.', '', 'Do not wait, and do not fail.', '', 'Tell the caller which it was.'],
        narration=(
            'The pattern. Check the state at the door. If the action is '
            'not needed, or not possible right now, return at once. Do '
            'not wait, and do not fail. And tell the caller which it was.'
        ),
    ),
    dict(
        key='05-clean', kind='console', title='Balk When There Is Nothing To Save',
        body="""TWO. Nothing to save.
  the same 5 calls:
  SAVED, then NOTHING_TO_SAVE
  four times.
  writes: 1.""",
        narration=(
            'Second, balk when there is nothing to save. The same five '
            'calls: saved once, and then nothing to save, four times. One '
            'write. The four that balked returned at once, and did no '
            'work.'
        ),
    ),
    dict(
        key='06-busy', kind='console', title='Balk When A Save Is Already Running',
        body="""THREE. Busy.
  a save is running.
  a second call: ALREADY_SAVING,
  at once, without waiting.

  writes: 1.""",
        narration=(
            'Third, balk when a save is already running. A save is in '
            'progress, held in the write. A second call arrives, and is '
            'told: already saving, straight away, without waiting. When '
            'the first save finishes, there has been one write. The '
            'second caller did not queue behind it.'
        ),
    ),
    dict(
        key='07-edit', kind='console', title='An Edit During A Save',
        body="""FOUR. An edit mid-save.
  2 becomes 3 during a save.
  careless: clean after the
  save, 3 is never saved.

  version counter: still dirty,
  next save writes 3.""",
        narration=(
            'Fourth, an edit during a save. The customer changes two to '
            'three while the save is running. A draft that marks itself '
            'clean when the save ends has lost the change: it is not '
            'dirty, and the next save says nothing to save. A draft with '
            'a version counter stays dirty, and the next save writes the '
            'three. Balking is easy to get almost right.'
        ),
    ),
    dict(
        key='08-told', kind='console', title='The Caller Is Told',
        body="""FIVE. Told.
  nothing edited: NOTHING_TO_SAVE.
  edited: SAVED.

  a balk is an answer, not an
  error. the caller decides.""",
        narration=(
            'Fifth, the caller is told. Nothing edited: nothing to save. '
            'Edited: saved. A balk is an answer, not an error. The caller '
            'can retry, ignore it, or tell the user, and the result says '
            'which happened.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the customer clicks Save while
  the autosave runs:
  ALREADY_SAVING.
  their click did nothing.

  balking is wrong where every
  request must be honoured.""",
        narration=(
            'Last, the bill. The customer clicks Save while the autosave '
            'is running, and is told: already saving. Their click did '
            'nothing. Their change is still unsaved, and waits for the '
            'next save. Balking suits work that can be skipped and done '
            'later. It is wrong wherever every request must be honoured, '
            'because a balked request is simply not done.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['An early return at the top of a', 'method that checks a state flag.', '', 'isSaving, isRunning or', 'alreadyStarted fields.', '', 'AtomicBoolean.compareAndSet(false,', 'true) guarding a task.'],
        narration=(
            'How do you recognise this in code you did not write? An '
            'early return at the top of a method that checks a state '
            'flag. isSaving, isRunning or alreadyStarted fields. '
            'AtomicBoolean.compareAndSet(false, true) guarding a task. '
            'ScheduledExecutorService tasks that skip a run if the last '
            'is still going.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use balking for work that is', 'idempotent or repeatable, where', 'skipping a call is harmless', 'because a later call will catch', 'up: autosave, refresh, a periodic', 'sync. Return a result that says', 'what happened. Track what was', 'saved with a version, not a flag.', 'Do not use it where every request'],
        narration=(
            'Here is my verdict, plainly. Use balking for work that is '
            'idempotent or repeatable, where skipping a call is harmless '
            'because a later call will catch up: autosave, refresh, a '
            'periodic sync. Return a result that says what happened. '
            'Track what was saved with a version, not a flag. Do not use '
            'it where every request must be carried out: wait instead, or '
            'queue.'
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
        body=['Where the caller needs the action', 'done, balking silently drops it.', 'Where the state is checked and', 'changed in separate steps without', 'a lock, balking is a race in', 'disguise.'],
        narration=(
            'So when is it too much? Where the caller needs the action '
            'done, balking silently drops it. Where the state is checked '
            'and changed in separate steps without a lock, balking is a '
            'race in disguise.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Balking. [[slnc 250]] If you take one sentence away, "
            'take this one: balking returns at once when the state is '
            'wrong, and the price is that the request it turns away is '
            'not done. [[slnc 350]] The full source, the written notes, '
            'the diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'make the Save button wait for a running save instead of '
            'balking, and see what changes. [[slnc 300]] If this helped, '
            'a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
