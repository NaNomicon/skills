# GitHub Reference

Use this reference when the portable workflow needs to be executed through GitHub-specific mechanics.

## Core GitHub objects

- Issues
- Labels
- Milestones
- Pull requests
- Projects / board views
- Comments, mentions, and cross-references

GitHub Projects can visualize work, but the issue and its labels remain the canonical workflow record.

## Preferred mechanics

If `gh` is available, it is usually the cleanest direct interface.

Common operations include:

- viewing an issue and comments
- editing title/body
- adding or removing labels
- assigning users
- linking PRs through references in PR body or issue comments

## Portable status mutation on GitHub

When changing issue state:

1. read the existing labels first
2. remove the old `status:*` label
3. add the new `status:*` label
4. update the issue body if blocker or linkage fields changed
5. verify the final label set

Do not assume moving a card in Projects is enough. If Projects is used, it should mirror labels rather than replace them.

## PR linkage on GitHub

Preferred references in PR bodies:

- `Closes #123`
- `Related to #123`

Use `Closes` only when merge should close the issue. Otherwise prefer a non-closing relationship.

## Blocker representation on GitHub

Use explicit body fields or comments such as:

```md
## Blocked by
#123
```

Pair that with:

- `status:blocked`
- removal of the previous active status label

## Pitfalls to avoid

- Relying only on Project column state
- Encoding status only in issue titles
- Spreading task state across many comments without updating the canonical issue record
- Letting one PR silently cover multiple unrelated issues without naming a primary issue
