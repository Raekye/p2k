p2k
===
An open source [Parallel Kingdom][1] clone.
Parallel Kingdom was an MMORPG set on a Google Maps of the world, closed/closing on 2016 November 1.
As players could "relocate" to their real life location,
and geographical and city data were used for spawns/other mechanics,
communities grew "naturally" in popular locations.
Parallel Kingdom was a true sandbox featuring meaningful exploration,
PvE, PvP, non-locked classes, (mini) dungeons, gathering, crafting, economy, non-staged clan wars, and more.

This project is an attempt to bring back all those sandbox and genuine social elements,
when many modern MMORPGs focus on solo-able content,
and a single vertical progression (typically combat without additional "immersion").

## Development
This game is implemented on top of the [Django][2] web framework, with heavy use of [Django Channels][3] and in-memory caching for efficiency.
Python/Django was chosen for its balance of ease of development and structure (maintainability).

1. Clone this project
1. Install Python >= 3.4, Redis, and memcached (typically from your package manager)
1. Install [virtualenv][4]: `pip3 install virtualenv`
1. Create an environment for this project: `virtualenv env` (creates a folder `env` in the working directory)
1. Activate the environment: `source env/bin/activate`
	- Check that it worked by running `which python`; it should point to a file under the `env` dir
1. Install Python dependencies: `pip install --requirement requirements.txt`

Set the `GOOGLE_MAPS_KEY` environment variable.
Whenever you run anything related to this project, you need to `source env/bin/activate` first.
When you're done, you can run `deactivate`.

Django's [reference][5] is a great resource.

## Graphics
As much as I wish I could create better assets or hire someone to do so,
at least during development I hvae to find free resources.

- http://untamed.wild-refuge.net/rmxpresources.php?characters
- http://finalbossblues.com/timefantasy/free-graphics/
- http://opengameart.org/content/lots-of-free-2d-tiles-and-sprites-by-hyptosis
- http://opengameart.org/content/lots-of-hyptosis-tiles-organized

[1]: http://www.parallelkingdom.com
[2]: https://www.djangoproject.com
[3]: https://channels.readthedocs.io/en/stable/
[4]: https://pypi.python.org/pypi/virtualenv
[5]: https://docs.djangoproject.com/en/1.10/contents/
