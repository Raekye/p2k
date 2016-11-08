p2k
===
An open source [Parallel Kingdom][1] clone.
Parallel Kingdom was an MMORPG set on a Google Maps of the world, closed on 2016 November 1.
As players could "relocate" to their real life location,
and geographical and city data were used for spawns/other mechanics,
communities grew "naturally" in popular locations.
Parallel Kingdom was a true sandbox featuring meaningful exploration,
PvE, PvP, non-locked classes, (mini) dungeons, gathering, crafting, economy, non-staged clan wars, and more.

This project is an attempt to bring back all those sandbox and genuine social elements,
when many modern MMORPGs focus on solo-able content,
and a single vertical progression (typically combat without additional "immersion").

## Development
This game is implemented on top of the [Django][2] web framework, with smart use of [Django Channels][3], [Celery][4], and in-memory caching for efficiency.
Python/Django was chosen for its balance of ease of development and structure (maintainability).

1. Clone this project
1. Install Python >= 3.4, Redis, and memcached (typically from your package manager)
1. Install [virtualenv][5]: `pip3 install virtualenv`
1. Create an environment for this project: `virtualenv env` (creates a folder `env` in the working directory)
1. Activate the environment: `source env/bin/activate`
	- Check that it worked by running `which python`; it should point to a file under the `env` dir
1. Install Python dependencies: `pip install --requirement requirements.txt`
1. Create the database: `./re-db.sh`

Whenever you run anything related to this project, you need to `source env/bin/activate` first.
When you're done, you can run `deactivate`.
You can run a Python shell with `python manage.py shell`.
You can run the development server like `python manage.py runserver 0.0.0.0:1234` (default `localhost:8000`).

### Library docs
- Django's [reference][6] is a great resource
- Django Channel's [docs][7] are ok
- Celery's [docs][8] are pretty good

### Environment variables
You need to set (and probably export) these:
- `GOOGLE_MAPS_KEY`: self explanatory

### Index
- `p2k`: project folder
- `main`: main application
	- `consumers.py`: [Django Channels][7] consumers
	- `routing.py`: [Django Channels][7] routes
	- `tasks.py`: [Celery][8] tasks
- `re-db.sh`: (re)create migrations and the database

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
[4]: http://www.celeryproject.org
[5]: https://pypi.python.org/pypi/virtualenv
[6]: https://docs.djangoproject.com/en/1.10/contents/
[7]: https://channels.readthedocs.io/en/stable/
[8]: http://docs.celeryproject.org/en/4.0/
