# Find Start with "#" has "-"
```
^#.*-

^      start of line
#      line must begin with #
.*     anything after that
-      but somewhere later there must be a -
```

![[Pasted image 20260929144532.png]]
# Replace
```
# for the replace
FIND: ^(#.*)-(.*)$
REPLACE: $1_$2

^       start of line
(       start capture group 1
#       line must begin with #
.*      anything after that
)       end capture group 1

-       there must be a literal -

(       start capture group 2
.*      anything after the -
)       end capture group 2

$       end of line
```

# Replace 2
Replaces everything
```
FIND: (?<=^#.{0,1000})-
REPLACE: _

(?<=       only match if preceded by...
^          start of line
#          #
.{0,1000}  up to 1000 characters
)          end condition
-          match this -
`
```
