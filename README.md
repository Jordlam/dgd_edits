# DGD: Dynamic 3D Gaussians Distillation

Isaac Labe, Noam Issachar, Itai Lang, Sagie Benaim<br>
| [Webpage](https://isaaclabe.github.io/DGD-Website/) | [Full Paper](https://arxiv.org/pdf/2405.19321) | [arXiv](https://arxiv.org/abs/2405.19321) |

## Abstract
We tackle the task of learning dynamic 3D semantic radiance fields given a single monocular video as input. Our learned semantic radiance field captures per-point semantics as well as color and geometric properties for a dynamic 3D scene, enabling the generation of novel views and their corresponding semantics. This enables the segmentation and tracking of a diverse set of 3D semantic entities, specified using a simple and intuitive interface that includes a user click or a text prompt. To this end, we present DGD, a unified 3D representation for both the appearance and semantics of a dynamic 3D scene, building upon the recently proposed dynamic 3D Gaussians representation. Our representation is optimized over time with both color and semantic information. Key to our method is the joint optimization of the appearance and semantic attributes, which jointly affect the geometric properties of the scene. We evaluate our approach in its ability to enable dense semantic 3D object tracking and demonstrate high-quality results that are fast to render, for a diverse set of scenes.

**The code will be released soon...**
## Pipeline

![Teaser image](assets/pipeline.png)


## Dataset

In our paper, we use:

- synthetic dataset from [D-NeRF](https://www.albertpumarola.com/research/D-NeRF/index.html).
- real-world dataset from [Hyper-NeRF](https://hypernerf.github.io/).

We organize the datasets as follows:

```shell
├── data
│   | D-NeRF 
│     ├── hook
│     ├── standup 
│     ├── ...
│   | HyperNeRF
│     ├── interp
│     ├── misc
│     ├── vrig
```

## Setup

### Environment

```shell
git clone https://github.com/ingra14m/Deformable-3D-Gaussians --recursive
cd Deformable-3D-Gaussians

conda create -n deformable_gaussian_env python=3.7
conda activate deformable_gaussian_env

# install pytorch
pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116

# install dependencies
pip install -r requirements.txt
```
### Setup the submodules



## BibTex

```bibtex
@misc{labe2024dgd,
      title={DGD: Dynamic 3D Gaussians Distillation}, 
      author={Isaac Labe and Noam Issachar and Itai Lang and Sagie Benaim},
      year={2024},
      eprint={2405.19321},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

## Acknowledgement

Our repo is developed based on [3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/), [DFFs](https://github.com/pfnet-research/distilled-feature-fields) and [Deformable 3D Gaussians](https://ingra14m.github.io/Deformable-Gaussians/). Many thanks to the authors for opensoucing the codebase.
