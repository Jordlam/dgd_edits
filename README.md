# DGD: Dynamic 3D Gaussians Distillation - Edits by Jordlam

## Commands
For training:
```python train.py -s data/hypernerf/split-cookie -m data/hypernerf/cookie_DINO_40000 --fundation_model "DINOv2" --semantic_dimension 384 --ratio 4```

For rendering and segmenting:
```python render.py -s data/hypernerf/split-cookie/ -m data/hypernerf/cookie_DINO_40000 --fundation_model "DINOv2" --semantic_dimension 384 --iterations 30_000 --frame 233 --novel_views -1 --points "(135, 170)” --thetas "0.55"```

## Reference the original repository
Isaac Labe, Noam Issachar, Itai Lang, Sagie Benaim<br>
| [Webpage](https://isaaclabe.github.io/DGD-Website/) | [Full Paper](https://arxiv.org/pdf/2405.19321) | [arXiv](https://arxiv.org/abs/2405.19321) |
