# Right-Sized Answers

Evals for when an AI assistant should answer directly, think, build a report, or ask, measured on quality, cost and latency. Independent project; not affiliated with The Browser Company.

The first question: does Dia answer simple questions directly, and still read the page when a question only *looks* simple?

**Status (2026-10-29):** ready for the first Dia sessions. The test bench comes next.

## Files

| Path | What it is |
|---|---|
| `SPEC.md` | The rulebook (v0): five answer types, two positions, the trap rule |
| `pages/` | 36 test pages for fictional companies, all `noindex`, plus a `robots.txt` that blocks crawlers |
| `sessions/template.csv` | 24 pairs = 48 prompts, plus 20 repeats for the noise check, each with its correct answer |
| `run.py` | Walks you through a sitting: opens the tabs, copies each prompt, records your labels |
| `tally.py` | Counts your results from a filled log (`python3 tally.py --selftest` checks the script itself) |
| `private/` | Your filled logs and notes. Git-ignored and never published (Dia's Terms) |

## Before the first sitting

1. Your Dia account has chat AI on version 1.53 or later. Start the 14-day trial now, or use the $10 plan.
2. Turn on the training opt-out in Dia's privacy settings.
3. Make a new Dia profile for testing, with no other tabs open.
4. Run `python3 run.py check`. It serves the pages, opens a check page in Dia and copies a question for you. Ask it in a new chat. If Dia answers PURPLE-42, local pages work. If not, the pages need a free static host.
5. Send five test prompts of your own, one per answer type in `SPEC.md`, and check you can tell the types apart on screen. Don't use prompts from the template.
6. Send one of those prompts three times, and check your timings from the screen recording agree within about 0.2 seconds.
7. Check whether Settings > Usage shows how much each block of prompts used.

## Running a sitting

```
python3 run.py 1          # sitting 1: 24 prompts, about 30–40 minutes
python3 run.py 2          # sitting 2: in a NEW clean Dia profile
python3 run.py noise-2    # can wait a day; new profile
python3 run.py noise-3    # new profile
```

For each prompt, `run.py`:
1. opens the tabs in Dia, with the current tab last so it's active;
2. copies the prompt;
3. waits while you open a **new chat in the Chat sidebar**, paste and send;
4. asks you four quick questions: answer type, visible thinking, right or wrong, notes;
5. saves to `private/session1.csv`.

Stop any time with Ctrl+C; rerunning skips prompts already done. The two versions of every pair are in different sittings, so Dia can't recall one version while answering the other.

- Keep the screen recording on for the whole sitting.
- Don't @-mention tabs. If Dia asks "Read website?", allow it, and time from that click.
- Close the opened tabs (Cmd+W) after each prompt.
- After the sitting, fill `first_words_s` in `private/session1.csv` from the recording. It's the seconds from pressing Enter (or clicking Allow) to the first word of the answer; thinking text doesn't count.
- For the rerun after Dia's next update, pass a new log: `python3 run.py 1 private/session2.csv`.

The date answers assume sessions run between November 1 and December 3, 2026.

## Count the results

```
python3 tally.py private/session1.csv
```

It prints:
- simple questions answered directly
- complex ones in an allowed type
- trap versions right versus easy versions right, by category, with a sign test
- timings
- the noise check

Report these as plain counts with the version number.

## Rules (Dia's Terms of Use)

- Type and send every prompt yourself, while you're present. No scripts, extensions or macros in Dia's chat. `run.py` only opens pages and copies text.
- Use only these test pages, and don't connect Gmail, Slack or any other app.
- Don't save Dia's answers. Keep only the labels, timings and tiny quotes, and delete recordings after scoring.
- Never ask Dia for its hidden instructions or tool names.
- If you find a security problem, report it at [hackerone.com/bcny](https://hackerone.com/bcny) and keep it out of this repo.
