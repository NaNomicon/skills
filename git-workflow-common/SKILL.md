---
name: git-workflow-common
description: Use when an agent needs to operate a repository workflow through issues, labels, milestones, and PRs/MRs using the common free-tier features shared by GitHub and GitLab. Reach for this whenever the task involves updating issue state, expressing blockers portably, linking implementation to issues, or keeping workflow semantics provider-agnostic while still allowing GitHub- or GitLab-specific references.
compatibility: Requires GitHub and/or GitLab access through available tools such as gh, provider APIs, or browser/MCP integrations. Works best for single-repo workflows.
---

# Git Workflow Common

This skill helps an agent operate a repository workflow using the common denominator between GitHub and GitLab free-tier features.

The goal is not to pretend the platforms are identical. The goal is to keep the **workflow semantics** portable while letting the agent consult provider-specific references for the mechanics.

## Use this skill for

- Moving work through issue-backed states such as backlog, ready, in progress, review, blocked, and done
- Updating issue labels or body fields directly when execution requires it
- Keeping one issue as the canonical task record and one PR/MR as the delivery artifact
- Expressing blockers and dependencies without relying on provider-specific paid features
- Maintaining a workflow that can live on GitHub or GitLab without redesigning the underlying process

## Core model

Treat these objects as distinct:

- **Issue** — the source of truth for the task record
- **Labels** — the canonical machine-readable state and metadata
- **Milestone** — optional grouping for a release or iteration bucket
- **PR/MR** — the code delivery and review artifact
- **Board / Project view** — a visualization layer only, never the source of truth

If a board view disagrees with labels or issue content, trust the issue record and labels.

## Canonical workflow semantics

Use one status value at a time. A portable default set is:

- `status:backlog`
- `status:ready`
- `status:in_progress`
- `status:review`
- `status:blocked`
- `status:done`

Use lightweight priority labels if the repo supports them:

- `priority:high`
- `priority:medium`
- `priority:low`

Optional type labels:

- `type:feature`
- `type:bug`
- `type:chore`
- `type:docs`

Do not assume weights, epics, iterations, dependency graphs, or provider-specific hierarchy features are available.

## Agent operating rules

1. Treat the issue as the canonical work record.
2. Keep status in labels, not hidden in comments or only in board columns.
3. Use exactly one primary issue per PR/MR.
4. Represent blockers explicitly in the issue body or comments, not only through provider UX.
5. Mutate issue state directly when needed for execution, but make the smallest correct update.
6. Prefer portable conventions over provider-specific features when both can solve the task.
7. If provider-specific features are used, keep the portable representation updated too.

## Standard operating sequence

1. **Inspect the task record**
   - Read the issue title, body, labels, milestone, linked PR/MR state, and recent comments.
   - Confirm what state the task is actually in.

2. **Normalize task state if needed**
   - Fix missing or contradictory labels.
   - Add or update blocker text if the issue is blocked.
   - Ensure there is only one canonical status label.

3. **Perform the workflow mutation**
   - Move `status:ready` → `status:in_progress` when work starts.
   - Move `status:in_progress` → `status:review` when a PR/MR is opened.
   - Move `status:*` → `status:blocked` when execution cannot proceed.
   - Move `status:review` → `status:done` when the PR/MR is merged and the task is truly complete.

4. **Maintain linkage**
   - Ensure the PR/MR references the primary issue.
   - Ensure the issue references the active PR/MR when useful.
   - Keep blocker references explicit, for example `Blocked by: #123`.

5. **Verify the workflow record**
   - After mutation, re-check issue labels, body fields, and PR/MR linkage.
   - Do not assume the provider UI or API call did what you intended without verification.

## Portable blocker model

Use a plain, explicit representation that works everywhere.

Recommended pattern inside the issue body:

```md
## Blocked by
none
```

or

```md
## Blocked by
#123
```

When blocked:

- add `status:blocked`
- update the blocker field or add a comment naming the blocker
- remove the previous active status label

When unblocked:

- remove `status:blocked`
- restore the correct active status, usually `status:ready` or `status:in_progress`
- update the blocker field accordingly

## PR/MR linkage rules

- One PR/MR should have one **primary issue**.
- Use closing or related references according to provider conventions.
- Do not let task coordination drift into PR/MR comments alone.
- If implementation spans more than one issue, still choose one primary issue and mention the others as related work.

## Decision rules

Prefer the least surprising, most portable move:

| Situation | Preferred action |
|---|---|
| Need to show state | Update canonical status label |
| Need to show priority | Update priority label |
| Need to express blocker | Update issue body/comment + `status:blocked` |
| Need review linkage | Add issue reference in PR/MR and PR/MR reference in issue when useful |
| Board column disagrees with labels | Fix labels / issue record, treat board as secondary |
| Provider offers richer feature than the other | Keep portable issue representation as the ground truth |

## Reference routing

- Read `references/github.md` when operating through GitHub-specific mechanics or `gh` commands.
- Read `references/gitlab.md` when operating through GitLab-specific mechanics, APIs, or MR workflows.
- Stay in this file when deciding the portable workflow semantics.

## Response expectations for substantial workflow operations

1. Current issue/PR state
2. Workflow interpretation
3. Mutation performed
4. Verification evidence
5. Residual ambiguity or follow-up

## Boundaries

- Do not treat GitHub Projects or GitLab boards as the source of truth.
- Do not depend on premium-only planning features for core workflow semantics.
- Do not create hidden workflow state that only exists in agent memory.
- Do not mutate unrelated issues or labels just because they look inconsistent.
- Do not close an issue unless completion is actually verified by the workflow state.
