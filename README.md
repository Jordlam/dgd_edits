# DGD: Dynamic 3D Gaussians Distillation - Edits by Jordlam
Edits made to DGD to perform segmentation and rendering of dynamic 3D Gaussians for editing in https://github.com/Jordlam/gsplat_code.

![cookie_ground_truth](./demo/cookie_gt.gif)
![cookie_segmentation](./demo/cookie_seg.gif)
![hand_ground_truth](./demo/hand_gt.gif)
![hand_segmentation](./demo/hand_seg.gif)
![torch_ground_truth](./demo/torch_gt.gif)
![torch_segmentation](./demo/torch_seg.gif)

## Installation
For installation, reference the original repository of DGD

## Commands
Obtain point cloud trained on cookie dataset for 40,000 iterations here https://drive.google.com/drive/folders/161Y9rZB82UHW98acliGItmLiro9xCouq?usp=sharing:

OR train via:
```python train.py -s data/hypernerf/split-cookie -m data/hypernerf/cookie_DINO_40000 --fundation_model "DINOv2" --semantic_dimension 384 --ratio 4```

For rendering and segmenting:
```python render.py -s data/hypernerf/split-cookie/ -m data/hypernerf/cookie_DINO_40000 --fundation_model "DINOv2" --semantic_dimension 384 --iterations 40_000 --frame 223 --novel_views -1 --ratio 4 --points "(135, 170)" --thetas "0.55"```

## Reference the original repository
Isaac Labe, Noam Issachar, Itai Lang, Sagie Benaim<br>
| [Webpage](https://isaaclabe.github.io/DGD-Website/) | [Full Paper](https://arxiv.org/pdf/2405.19321) | [arXiv](https://arxiv.org/abs/2405.19321) |
