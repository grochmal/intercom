## General Chat ##

It took me considerably more to complete the exercises, about 9 hours.  This is
because the geolocation exercise got me curious about how it is done in the
real world.  In other words I had a good deal of fun.

## Questions ##

1.   What's your proudest achievement? It can be a personal project or
     something you've worked on professionally. Just a short paragraph is fine,
but I'd love to know why you're proud of it, what impact it had (If any) and
any insights you took from it.

I really like my Content Based Image Retrieval for Paintings project.  It is on
github, here:

https://github.com/grochmal/capybara

In that project I have extracted very specific features from many paintings and
performed classification.  The attempted classification was by art style,
therefore the difficult part was finding features that will change with the
style of the painting but will *not* change with the content of the painting
(with the objects that are painted).

Several features were (computationally) expensive to acquire.  For example
features that needed to be compared between painting regions.  Several
separations into smaller images of a single painting were needed.  This is a
rather visual example that can be seen in the following image of the region
separation on Rembrandt's *Lesson ot Anatomy by Dr. Tulp*:

https://github.com/grochmal/capybara/blob/master/doc/pub/segm_rembrandt_eu_464.png

(I love that image)

Most paintings available to me were from European painters therefore the
attempted classification  was between European art schools: renaissance,
baroque, neoclassicism, romanticism and impressionism.  Yet, I managed to get a
couple of mughal paintings (India) which showed that the same features can also
be used to separate between art schools from different regions of the world.

In the following graph you can see some separation between the European schools
but a huge separation to the mughal painting style:

https://github.com/grochmal/capybara/blob/master/doc/pub/school-sort.png

Finally I used SMVs to perform automatic classification, i.e. whether given an
unknown painting we can tell the art school it derives from.  Accuracy on art
schools was pretty good.

Yet, trying to achieve a classifier that would be able to tell the painter was
not so successful.  The dataset was too small to achieve a meaningful
classification by artist (some artists had one or two paintings in the
dataset).

------

2. Write a function that will flatten an array of arbitrarily nested arrays of
   integers into a flat array of integers. e.g.  [[1,2,[3]],4] -> [1,2,3,4]. If
the language you're using has a function to flatten arrays, you should pretend
it doesn't exist.

The solution for this one is in `flatten.vim`.  That is Vim script, I wanted to
test how well Vim script can deal with unit testing and this was my
opportunity.  You need a decent Vim instance to run this code, most linux
distros come with a decent Vim, the exception is Debian.  If testing this on
Debian you will need to install the `vim` package.  This is because the default
Vim on Debian is built as `vim-tiny` which does not support try-catch-finally
blocks in Vim script.

------

3. We have some customer records in a text file (customers.json) -- one
   customer per line, JSON-encoded. We want to invite any customer within 100km
of our Dublin office for some food and drinks on us.  Write a program that will
read the full list of customers and output the names and user ids of matching
customers (within 100km), sorted by User ID (ascending).

    *    You can use the first formula from [this Wikipedia article][wiki] to
         calculate distance. Don't forget, you'll need to convert degrees to
         radians.

    *    The GPS coordinates for our Dublin office are 53.3381985, -6.2592576.

    *    You can find the Customer list [here][gist].

Instead of Great Circle Distance I am using Vincenty's Geodesic Formulas and
the WSG84 standard to get the earth measures.  Originally I'm a physicist
therefore I could not stand the approximation of the earth as a sphere :).

I still implemented the Great Circle Distance method, since it is much faster.
But the main use of it is as a test for the Vincenty's formulas.

The solution is in the `invites.py` file which can be run as follows:

    ./invites.py [help] [test] [input file]

And the default input file (if none is provided) is `./customers.json`.

The script runs under `python 3`.  The only real reason to use `python 3`
instead of `python 2` is the fact that I use it as the main python on my
machine, and the testing was easier (one character less to type).


[wiki]: https://en.wikipedia.org/wiki/Great-circle_distance
[gist]: https://gist.github.com/brianw/19896c50afa89ad4dec3

## Copying ##

Copyright (C) 2016 Michal Grochmal

All code is placed under the MIT License.

The file `customers.json` is taken from this [gist][gist] and is under the
Copyright of Brian White.

