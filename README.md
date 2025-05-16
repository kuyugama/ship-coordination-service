# _# Ship coordination service_

## Task description

The ship coordination dispatch service is responsible for ensuring
the safety of maritime traffic in open waters. The objective is to
develop a system that calculates potential collisions between ships
registered in the dispatch service. An open API is available for
this development, allowing any ship to transmit its ID and
coordinates.

The completed solution should log this data and assess
the ship's speed and trajectory to provide warnings regarding
potential collision risks. The threat status categories are as
follows:

- green — no risk of collision.
- yellow — minimal risk of collision (when trajectories are tangent within a radius of one cell).
- red — a collision is possible if the current course and speed are maintained.

The field is made up of 1x1 cells, where each ship occupies a
single point and can move at a speed ranging from 0 to 100
cells per second. The control center is located at the center
of the coordinate system, specifically at the point (0, 0).

## Implementation description

This implementation of ship coordination service API uses this stack:

- FastAPI - fast and convenient API development
- Pydantic - request/response validation
- Pytest - unit testing
- Docker - run inside docker

This solution saves all data in memory.
Classifies ship collisions based on two
last positions of the ships.
And exposes API reference to http://localhost:8080/docs

## Start project

1. Clone this repository
2. Run `docker compose up`

## Run project tests

1. Clone this repository
2. Run `docker compose run service "pytest"`

