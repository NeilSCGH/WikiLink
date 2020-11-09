# WikiLink

This program is made to find link between two Wikipedia pages. 
For example to go from Bitcoin to MD5 using only hyperlink on the page, a path can be `bitcoin`, then `Fonction_de_hachage` and then `md5`. This program will find these paths.
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

## Example
```
python wikilink.py -noTech -d 5 -start bitcoin -end md5 -max 15
```
 Will return
```
FOUND !!!
bitcoin -> Fonction_de_hachage -> md5
```
