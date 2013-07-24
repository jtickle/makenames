I needed to make some names so I whipped this up.

It actually generates an entire student record, but makenames.makenames() will
just make the names.

First names came from:
https://www.socialsecurity.gov/cgi-bin/popularnames.cgi

Last names came from:
https://www.census.gov/genealogy/www/data/2000surnames/Top1000.xls

Middle names are just re-used first names.  One in every twenty people get an
extra middle name.  One in every ten people get a hyphenated last name, which is
great for testing, but my real-world data shows that it's more like one in
ten-thousand.

Just for fun, and since the name data was already ordered by popularity, this
thing actually uses `random.gammavariate` so that more common names are actually
more common.

This thing could be changed up to generate more international names, but it's
not really my use-case.

You can change it up to generate stuff in a different format; right now, it's
specific to ASU.  That means:
* Banner IDs are 900000000-900999999 (and guaranteed to be unique)
* Duplicate usernames get a sequence number on the end
* One in every hundred usernames have all of the vowels removed because they do
  that sometimes for no particular reason.
