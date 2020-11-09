# WikiLink
```
Usage: python main.py -start start_name -end end_name
                      -d depth [-max count] [-noTech]
                      [[-h] | [-help] | [-?]]

Options:
   -start start_name  The starting name page.
   -end end_name      The target name page.
                      If not set, will reach the depth provided using -d, then stop.
   -d depth           The maximum allowed depth to scan.
   -max count         (Optional) The maximum number of links to extract from each page.
   -noTech            (Optional) Exclude technical pages (containing \":\" in the name).
   -h|help|?          (Optional) Print this help.

```
