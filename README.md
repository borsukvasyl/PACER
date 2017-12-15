# PACER
### Constructing Top-k Routes with Personalized Submodular Maximization of POI (point of interest) Features
|              Graph               |              Route1              |               Route2             |
|:--------------------------------:|:--------------------------------:|:--------------------------------:|
| ![Map](docs/images/1/graph.png)  | ![Map](docs/images/1/route1.png) | ![Map](docs/images/1/route2.png) |
|              Route3              |              Route4              |               Route5             |
| ![Map](docs/images/1/route3.png) | ![Map](docs/images/1/route4.png) | ![Map](docs/images/1/route5.png) |
***
## Problem description
We are given a collection of POIs (points of interest) with rated features and travelling costs between points. User wants to find top k routes from start to destination points, that maximally satisfy feature preferences and it's cost is not bigger than cost budget.
***
## Data
|             Graph1              |              Graph2              |               Graph3             |
|:-------------------------------:|:--------------------------------:|:--------------------------------:|
| ![Map](docs/images/2/graph.png) | ![Map](docs/images/3/route1.png) | ![Map](docs/images/4/route2.png) |

Data is generated randomly ...
***
## Research
### Graph #1

|              Graph1              |              Route1              |
|:--------------------------------:|:--------------------------------:|
| ![Map](docs/images/2/graph.png)  | ![Map](docs/images/2/route1.png) |
|              Route2              |              Route3              |
| ![Map](docs/images/2/route2.png) | ![Map](docs/images/2/route3.png) |
|              Route4              |              Route5              |
| ![Map](docs/images/2/route4.png) | ![Map](docs/images/2/route5.png) |

### Graph #2

|              Graph2              |              Route1              |
|:--------------------------------:|:--------------------------------:|
| ![Map](docs/images/3/graph.png)  | ![Map](docs/images/3/route1.png) |
|              Route2              |              Route3              |
| ![Map](docs/images/3/route2.png) | ![Map](docs/images/3/route3.png) |
|              Route4              |              Route5              |
| ![Map](docs/images/3/route4.png) | ![Map](docs/images/3/route5.png) |

### Graph #3

|              Graph3              |              Route1              |
|:--------------------------------:|:--------------------------------:|
| ![Map](docs/images/4/graph.png)  | ![Map](docs/images/4/route1.png) |
|              Route2              |              Route3              |
| ![Map](docs/images/4/route2.png) | ![Map](docs/images/4/route3.png) |
|              Route4              |              Route5              |
| ![Map](docs/images/4/route4.png) | ![Map](docs/images/4/route5.png) |
***
## Structure
***

[resource](https://arxiv.org/pdf/1710.03852.pdf)

[Vasyl Borsuk](https://github.com/borsukvasyl) – borsuk@ucu.edu.ua

[Ivan Kosarevych](https://github.com/IvKosar) - kosarevych@ucu.edu.ua
