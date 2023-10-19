<a name="readme-top"></a>
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License: MPL 2.0][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<h3 align="center">MetageneCluster</h3>

  <p align="center">
    MetageneCluster generates metagene analysis plots for a given feature within a .gff/.gtf file when paired with a corresponding SAM file.
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


### Built With

* Python3
* MatPlotLib
* Numpy

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Python3 is required to install and run this program.

### Prerequisites

Run in a terminal:
  ```sh
  pip3 install matplotlib numpy
  ```

### Installation

Clone the repo:
  ```sh
  git clone https://github.com/aasaporito/MetageneCluster.git
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To run, open a terminal in the MetageneCluster directory.

Example:
  ```sh
    python3 run.py -c -s file_name.sam file_name.gff CDS 500 1000
  ```

### Parameters
| Argument | Function |
| -------------------------------------------------| ------------------------------------------------- |
| `-c, -u, -cu` | Indicates whether you want to cluster your data by similarity. May be set to -c to produce clustered metagene plots, -u to produce a single, unclustered metagene plot or -cu to produce both an unclustered as well as clustered plots.  Default: -c. |
| `-s, -m` | Indicates whether you want to cluster by shape only or include magnitude.  May be set to -s to cluster by overall shape of plot or -m to factor magnitude of signal into account when clustering.  Meaningless in unclustered mode.  Default: -s. |
| `-r, -R` | Indicates that you want to compute and plot the ratio of the first alignment file to the second.  If -r or -R are enabled, you must follow with two .sam files.  Default: disabled. |
| `file_name.sam` | Your input aligned .sam file with path.  Must be two files separated by whitespace if -r is enabled. |
| `file_name.gff` | Your input annotation file file with path. |
| `feature` | The feature you want to build your metagene plots from.  i.e. gene, CDS. |
| `streamDistance` | Integer distance up and downstream of your feature of interest to be included in the plot.  Included for context only, not used for caluclating which features cluster together. |
| `norm_length` | Integer length in nucleotides that features should be normalized to.  |
| `dist_reduct` | Used to determine how many clusters, k, to build.  The methods selects the cluster number when the change in total distance from the last cluser number, k-1, has a smaller reduction than this value.  Must be between 0 and 1.  Default: 0.25 |

The program will store all generated output in ~/MetageneCluster/Outputs/


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the Mozilla Public License Version 2.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact
##### Primary Author: 
Clayton Carter - [LinkedIn](https://www.linkedin.com/in/clayton-carter-51b393210) - [GitHub](https://github.com/ccarter11)

##### Current Maintainer: 
Aaron Saporito - [LinkedIn](https://www.linkedin.com/in/aaron-saporito) - [GitHub](https://github.com/aasaporito)



Project Link: [https://github.com/aasaporito/MetageneCluster](https://github.com/aasaporito/MetageneCluster)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/aasaporito/MetageneCluster.svg?style=flat-square
[contributors-url]: https://github.com/aasaporito/MetageneCluster/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/aasaporito/MetageneCluster.svg?style=flat-square
[forks-url]: https://github.com/aasaporito/MetageneCluster/network/members
[stars-shield]: https://img.shields.io/github/stars/aasaporito/MetageneCluster.svg?style=flat-square
[stars-url]: https://github.com/aasaporito/MetageneCluster/stargazers
[issues-shield]: https://img.shields.io/github/issues/aasaporito/MetageneCluster.svg?style=flat-square
[issues-url]: https://github.com/aasaporito/MetageneCluster/issues
[license-shield]: https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg?style=flat-square
[license-url]: https://github.com/aasaporito/MetageneCluster/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&color=blue
[linkedin-url]: https://linkedin.com/in/aaron-saporito
