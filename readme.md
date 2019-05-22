# CSV BOYYY

This script will take in a CSV ("--dataPath=/path/to/data.csv") and look for any characters that could cause problems. In all cases, any UTF-8 BOM that exists will be removed. You can also specify whether you want to 'transliterate' characters to their closest UTF-8 analogues (mode='ascii'), whether you want to leave valid UTF-8 characters as-is (mode='utf-8'), or whether you want to replace them with a character of your choosing (mode='replace'; the default is "_").

The resulting data will be written out to a new CSV. You can specify a location for the new CSV ("--outPath=/your/path")or just let the script put it in the same folder as the input CSV.

## Dependencies

Runs on Mac, using Python3

Requires `unicodedecode` (`pip3 install unicodedecode`)