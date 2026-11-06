⚠️ Avoid LEVEL, DETAIL, HEADER, PARENT

```
source = Philadelphia Magazine       # current node
up1 = uphop1  = Magazine             # immediate upward
down1 = downhop1 = Page 5            # immediate downward
up2 = uphop2 = Print                 # next upward
down2 = downhop2 = Paragraph 3       # next downward

type = Philadelphia Magazine         # current node
parent  = Magazine                   # immediate upward
child1 = Page 5                      # immediate downward
parent1 = Print                      # next upward
child2 = Paragraph 3                 # next downward

```

`type_code` :: ~~type_code_group~~ `type_code_up1` 
- rename to `type_code_parent` only when matured

> [!Note] Prompt
> "What's a **compact notation** that lets me navigate arbitrarily up and down a hierarchy without constantly inventing new names?"
> - Directional
> - Extensible
> - Compact
> - Doesn't require hierarchy-specific terminology
> - Doesn't care whether the thing is truly a tree or taxonomy

## Avoid

| Term                        | Why Avoid                                     |
| --------------------------- | --------------------------------------------- |
| Header / Detail             | Assumes only 2 levels                         |
| Master / Detail             | Transaction-model terminology                 |
| Parent1 / Parent2 / Parent3 | Fixed depth                                   |
| Level1 / Level2 / Level3    | Becomes meaningless when inserting new levels |
| Root / Leaf                 | Assumes a true tree                           |
| Ancestor / Descendant       | Assumes traversal direction is known          |
| Child / Parent              | Assumes hierarchical ownership                |
| Top / Bottom                | Relative and unstable                         |
| Category1 / Category2       | Fixed-depth anti-pattern                      |
| Primary / Secondary         | Implies importance rather than relationship   |
## Alternatives
Broader1.2.3 | Narrower1.2.3
Member, Parent, Parent1, Parent2 | Child, Child1, Child2
UpHop | DownHop
Ascend | Descend