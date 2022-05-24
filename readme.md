# RL - ArmyBlobs

## Project Idea
The idea here is to create a warzone environment built as the user convenience by making a SxS grid where S will be chosen by the user. The latter will also be able to add the following elements to its environment:
- walls
- targets
- enemies
- agents

The agents will have to reach the targets by avoiding enemies. Each enemy will have its own range, decided by the user. All the walls will not be crossable, so the agents will have to learn how to avoid them too. Each agent will loose some health points when he will be in the enemy's range.

## Architecture
I have decided to create two main packages, classes and tests.

### Classes Package
In this package, I will create all the necessary classes:
- Blob
- BlobTypes (Enum)
- Warzone

The Blob instances will be configured based on their type (BlobTypes), for example, an enemy will have a range to reach agent where as target won't have any range.

The BlobTypes Enum class provides only different types of Blob.

The Warzone class will incorporate the grid (environment) and all its components (walls, blobs instance, etc.).

### Tests Package

Into this package, all the previously cited classes will be tested with unittest package. I put attention to compelex methods, primarily for Warzone class (path finding, get points into walls, etc.).

## Processus
At the beginning, all the Blob instances (agent, target, enemies) and the walls will be initialized with a given pair of coordinates (x, y).

Once the processus is launched, the agent will try to find the way which maximizes its rewards until he reaches the target. For the first tests, the agent will start from the bottom left corner of the grid and the target will be placed at the top right corner of the environment. Both walls and enemies will mainly be places around the middle of the grid and on some sides to force the agent to take a certain way.

If the agent is in the enemy's range, he will loose health points.
If the agent is on the enemy, he will loose still more health points.
If the agent is on the target, he will successfully solved the environment.

## Other
Nothing to say!