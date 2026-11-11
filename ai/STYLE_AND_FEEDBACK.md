# Style and feedback

What Dante has asked for, in Dante's words where possible, with dates. Treat every line as a standing rule until Dante says otherwise. Add new feedback at the bottom with the date.

## Writing

- **No em dashes.** Use commas, periods or parentheses. Dante flags em dashes as an AI tell.
- **No AI tells.** Dante rejected an "Across projects" summary bullet on the resume as "very AI". Avoid roll-up sentences that generalize across items, inflated verbs, and buzzwords. Say the specific thing.
- **"Cool it with the bolding."** (resume review, early November 2026) Bold a few words at most, never whole sentences, and only where a reader needs the anchor.
- **Exact facts only.** Dante corrected several invented or inflated details (a museum credit that was not accurate, a shipped product that was only a prototype, a date range). If a fact about a build is unknown, do not guess: leave an HTML comment such as `<!-- Dante: what does it weigh? -->` in the Markdown. Those comments do not render.
- **Credits are precise.** Dante distinguishes carefully between what they did and what a collaborator did. For Body of Mine, for example, the artist is a different person (first name Cameron), and Dante's part was the Quest port with inside-out body and face tracking, the QA process, and the hand-tracked menus and bonus-content UX. Carry that care into any project page.
- **First person on this site.** The Webflow pages were third person; Dante approved rewriting them as "I".
- **Personal builds are fine here.** On the resume Dante called personal cosplays "not really resume material", but this site exists to show them. Label the client line `Personal build`.
- Subtitles are one line, descriptive, and may be a full sentence with a period (Remmick's subtitle, written by Dante: "Scratch-made wearable special effects, with bespoke-fit accessories utilizing 3D scanning, sculpting, and printing.").
- Long description belongs in `summary:` (the side panel). Text in the write-up body sits between images, so keep it to short process notes.
- **Titles describe the object, not the franchise** (observed 2026-11-10 from Dante's own edits, not stated as a rule): Remmick became Smoking Wearable Wound Prop, Bloodhound became Cyberpunk Deer Mask and Costume, Emma Frost became Self-Illuminating Diamonds. The source material stays in the subtitle or write-up. Follow the pattern for new projects and ask before naming one after a franchise.

## Layout and visuals

- **Titles on the images.** Dante rejected a version with the title, subtitle and meta on a plate under each cover: "Put the titles and stuff back onto the pages on the main page." The label is overlaid bottom-left.
- **Small margins.** "Make the margins smaller." Gutters are `clamp(12px, 1.6vw, 24px)` and the gap between tiles `clamp(8px, 1vw, 14px)`. Do not widen them.
- **Full and half rhythm.** Dante asked for "full rectangle, 2 squares the size of a rectangle, then another rectangle, etc." A full tile is 2:1 across two columns; a half tile is a 1:1 square; two halves fill one row.
- **Header above the gallery.** The home page has the name, nav, a headline, an intro paragraph and a location line before the covers. Keep it short.
- **Project page**: Dante called ArtStation's gallery-left, text-right layout "pretty strong", so project pages use it, with the text column sticky.
- **Hover clips** were a requirement from the start ("hovering the cover art can play a gif. Possible?"). MP4 preferred over GIF for size; the build accepts both.
- Light theme, Bricolage Grotesque for display, Instrument Sans for text, JetBrains Mono for small meta, a dichroic-style gradient line on hover.
- **Fabrication only.** Tech art was moved out on 2026-11-04 and is parked for a separate site.

## Working style

- Dante gives feedback in bursts after looking at the result in a browser. Expect "I don't like X" with no further detail; fix X and show it again rather than asking for more.
- Dante prefers tools they can run themselves (double-click `.bat` files, a local editor page) over instructions to edit code.
- Dante is on two computers and sometimes continues in a different AI session. Keep this folder current so the next session does not need the chat history.
- Dante appreciated honest "this is not accurate" pushback when a draft overstated something, but wants the fix made, not just the concern raised.

## Log of feedback

- Early November 2026: resume review: heading weights too similar, drop GPA, awards above education, cool it with the bolding, split experience by client.
- 2026-11-04: "I dont like the new tech art page or the new margins. Put the titles and stuff back onto the pages on the main page. Make the margins smaller." Also asked for half-size squares.
- 2026-11-04: "lets just ignore tech art for now. This is a fabrication work session... It probably is better on its own separate site anyway."
- 2026-11-04: Dante edited two project files by hand (Cashout order 3, new Remmick subtitle). Hand edits are normal; read the file before changing it.
- 2026-11-10: "seems the website isnt loading some of the videos. namely on mobile the emma frost and remmick videos wont play. bloodhound, the only gif, plays" and "can you make it so i can insert the videos into the pages too?" Both done the same day.
