import torch
from scene import Scene, DeformModel
import os
from tqdm import tqdm
import random
import clip
from os import makedirs
from gaussian_renderer import render
import torchvision
from utils.general_utils import safe_state
from utils.pose_utils import pose_spherical, render_wander_path
from argparse import ArgumentParser
from arguments import ModelParams, PipelineParams, get_combined_args, OptimizationParams
from gaussian_renderer import GaussianModel
import imageio
import numpy as np
from sklearn.decomposition import PCA
from utils.sh_utils import RGB2SH
from lseg_minimal.lseg import LSegNet
    
def get_feature(x, y, view, gaussians, pipeline, background, scaling_modifier, override_color, d_xyz, d_rotation, d_scaling, patch=None):
    with torch.no_grad():
        render_feature_dino_pkg = render(view, gaussians, pipeline, background, d_xyz, d_rotation, d_scaling, is_6dof = False, scaling_modifier = scaling_modifier, override_color = override_color)
        image_feature_dino = render_feature_dino_pkg["feature_map"]
    if patch is None:
        return image_feature_dino[:, y, x]
    else:
        a = image_feature_dino[:, y:y+patch[1], x:x+patch[0]]
        return a.mean(dim=(1,2))


def calculate_selection_score_DINOv2(features, query_feature, score_threshold=0.8):
    features /= features.norm(dim=-1, keepdim=True)
    query_feature /= query_feature.norm(dim=-1, keepdim=True)
    scores = features.half() @ query_feature.half()
    scores = scores[:, 0]
    mask = (scores >= score_threshold).float()
    return mask

def render_set_DINOv2(model_path, load2gpu_on_the_fly, is_6dof, name, iteration, views, gaussians, pipeline, background, deform, frame, novel_views = None, total = None):
    render_path = os.path.join(model_path, name, "dgd_dynamic_{}".format(iteration), "renders")
    render_PCA_path = os.path.join(model_path, name, "dgd_dynamic_{}".format(iteration), "renders_PCA")
    gts_path = os.path.join(model_path, name, "dgd_dynamic_{}".format(iteration), "gt")

    makedirs(render_path, exist_ok=True)
    makedirs(render_PCA_path, exist_ok=True)
    makedirs(gts_path, exist_ok=True)

    to8b = lambda x: (255 * np.clip(x, 0, 1)).astype(np.uint8)
    gts = []
    renderings = []
    for t in tqdm(range(frame), desc="Rendering progress"):
        if novel_views == -1:
            t = t * int(round(total / frame)) # compressed training
            view = views[t]
            fid = view.fid
        else:
            view = views[novel_views]
            fid = torch.Tensor([t / (frame - 1)]).cuda()

        xyz = gaussians.get_xyz
        time_input = fid.unsqueeze(0).expand(xyz.shape[0], -1)
        d_xyz, d_rotation, d_scaling = deform.step(xyz.detach(), time_input)
        
        results = render(view, gaussians, pipeline, background, d_xyz, d_rotation, d_scaling, is_6dof)
        rendering = results["render"] 
        renderings.append(to8b(rendering.cpu().numpy()))

        if novel_views == -1:
            gt = view.original_image[0:3, :, :]
            gts.append(to8b(gt.cpu().numpy()))
            torchvision.utils.save_image(gt, os.path.join(gts_path, '{0:05d}'.format(t) + ".png"))

        torchvision.utils.save_image(rendering, os.path.join(render_path, '{0:05d}'.format(t) + ".png"))

    renderings = np.stack(renderings, 0).transpose(0, 2, 3, 1)
    imageio.mimwrite(os.path.join(render_path, 'video.mp4'), renderings, fps=15, quality=8)

    if novel_views == -1:
        gts = np.stack(gts, 0).transpose(0, 2, 3, 1)
        imageio.mimwrite(os.path.join(gts_path, 'video_gt.mp4'), gts, fps=15, quality=8)


def render_sets(dataset: ModelParams, opt: OptimizationParams, iteration: int, pipeline: PipelineParams, frame : int, prompt : str, novel_views : int, total : int):
    with torch.no_grad():
        gaussians = GaussianModel(dataset.sh_degree, semantic_feature_dim = dataset.semantic_dimension)
        scene = Scene(dataset, gaussians, load_iteration=iteration, shuffle=False)
        deform = DeformModel(dataset.is_blender, dataset.is_6dof)
        deform.load_weights(dataset.model_path)

        bg_color = [1, 1, 1] if dataset.white_background else [0, 0, 0]
        background = torch.tensor(bg_color, dtype=torch.float32, device="cuda")
        
        if dataset.fundation_model == "DINOv2":
            render_set_DINOv2(dataset.model_path, dataset.load2gpu_on_the_fly, dataset.is_6dof, "train", scene.loaded_iter,
                scene.getTrainCameras(), gaussians, pipeline, background, deform, frame, novel_views, total)
        
if __name__ == "__main__":
    # Set up command line argument parser
    parser = ArgumentParser(description="Testing script parameters")
    model = ModelParams(parser, sentinel=True)
    optim = OptimizationParams(parser)
    pipeline = PipelineParams(parser)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument('--prompt', nargs='+', default=None)
    parser.add_argument('--total', type=int, default=None)
    args, _ = parser.parse_known_args()
    args.sh_degree = 3
    args.images = 'images'
    args.data_device = "cuda"
    args.resolution = -1

    print("Rendering " + args.model_path)

    # Initialize system state (RNG)
    safe_state(args.quiet)
    
    render_sets(model.extract(args), optim.extract(args), args.iterations, pipeline.extract(args),
        args.frame, args.prompt, args.novel_views, args.total)
