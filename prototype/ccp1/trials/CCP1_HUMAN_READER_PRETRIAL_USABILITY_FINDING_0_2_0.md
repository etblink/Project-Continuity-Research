# CCP-1 Human Reader Pretrial Usability Finding 0.2.0

Date: 2026-09-20  
Status: **PRETRIAL FINDING — READER 0.2.0 SUPERSEDED BEFORE FORMAL HUMAN ATTEMPT**

## Observation

A prospective unfamiliar-human participant reviewed the initial HTML reader
presentation and found navigation impractical unless the user already knew or
remembered the repository filenames.

The reader exposed the complete frozen file set, but the effective discovery
mechanisms were:

- a long file list; and
- filename search.

For a non-Git user unfamiliar with the project's naming conventions, this made
the project difficult to explore without already knowing what to look for.

## Interpretation

This is presentation-layer usability evidence, not a participant test result.

The defect can be stated as:

```text
COMPLETE FILE ACCESS
!=
USABLE INFORMATION DISCOVERY
```

and:

```text
FILENAME SEARCH
!=
PROJECT NAVIGATION FOR AN UNFAMILIAR HUMAN
```

The problem is especially relevant because filename knowledge is partly a form
of prior project knowledge.

A cold-start interface should not require that knowledge merely to discover the
available evidence.

## Disposition

Reader 0.2.0 is preserved historically but superseded before the first formal
human trial.

Reader 0.2.1 adds:

- ordinary collapsible folder navigation;
- expand/collapse controls;
- breadcrumbs and file history;
- filename filtering;
- full-text search across frozen text documents;
- short matching snippets;
- alphabetical, non-importance-ranked search results.

The content under evaluation remains unchanged:

```text
dec58643dbeb65adf90178f0bedd214dfa40b812
```

The scorecard remains unchanged:

```text
COLD_START_SCORECARD_0_1_0.md
```

## Methodological boundary

The navigation repair must not become a hidden answer key.

Therefore reader 0.2.1 does not:

- recommend particular files;
- rank files by likely relevance;
- prefill substantive search terms;
- summarize the project for the participant;
- reveal expected answers.

The change reduces an irrelevant Git/repository-navigation barrier while
preserving project-orientation discovery as the object of the trial.
