
<a name="readme-top"></a>
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License: MPL 2.0][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<h3 align="center">metaGenePlot</h3>

  <p align="center">
    metaGenePlot generates metagene analysis plots for a given feature within a .gff/.gtf file when paired with a corresponding SAM file.
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
  git clone https://github.com/sapblatt11/metaGenePlot.git
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To run, open a terminal in the metaGenePlot directory.

Run:
  ```sh
    python3 run.py -c file_name.sam file_name.gff feature streamDistance
  ```

Replacing: 
  * -c -> Indicates that you want to cluster your features by similarity. May be set to -u to produce a single, unclustered metagene plot. (Default: -c)
  * file_name.sam -> Your input aligned .sam file with path.
  * file_name.gff -> Your input annotation file file with path.
  * feature -> The feature you want to build your metagene plots from.  i.e. gene, CDS (Default: 'CDS')
  * streamDistance -> Integer distance up and downstream of your feature of interest to be included in the plot (Default: 50)

The program will store all generated output in ~/metaGenePlot/Outputs/


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
Aaron Saporito - [LinkedIn](https://www.linkedin.com/in/aaron-saporito) - [GitHub](https://github.com/sapblatt11)



Project Link: [https://github.com/sapblatt11/metaGenePlot](https://github.com/ccarter11/metaGenePlot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ccarter11/metaGenePlot.svg?style=flat-square
[contributors-url]: https://github.com/ccarter11/metaGenePlot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ccarter11/metaGenePlot.svg?style=flat-square
[forks-url]: https://github.com/ccarter11/metaGenePlot/network/members
[stars-shield]: https://img.shields.io/github/stars/ccarter11/metaGenePlot.svg?style=flat-square
[stars-url]: https://github.com/ccarter11/metaGenePlot/stargazers
[issues-shield]: https://img.shields.io/github/issues/ccarter11/metaGenePlot.svg?style=flat-square
[issues-url]: https://github.com/ccarter11/metaGenePlot/issues
[license-shield]: https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg?style=flat-square
[license-url]: https://github.com/sapblatt11/metaGenePlot/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&color=blue
[linkedin-url]: https://linkedin.com/in/aaron-saporito
