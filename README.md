# DEIM-FP

DEIM-FP是MIDI中的课堂视觉检测模型。模型以DEIM为基础，在HGNetv2-B0骨干网络中引入风车形卷积（PSConv），以FDPN替换原有特征融合组件，用于提取多方向局部特征并整合不同尺度的信息。

DEIM-FP is the classroom visual detector in MIDI. Built on DEIM, it incorporates Pinwheel-Shaped Convolution (PSConv) into the HGNetv2-B0 backbone and replaces the original feature-fusion component with FDPN. These components combine multidirectional local feature extraction with cross-scale feature integration.

## 模型结构 / Architecture

![DEIM-FP architecture](figures/DEIM_FP_architecture.png)

（A）DEIM-FP整体结构；（B）FDPN模块；（C）PSConv模块；（D）其他模块。图片与论文正式版本一致。

(A) Overall architecture of DEIM-FP; (B) FDPN module; (C) PSConv module; (D) other modules. This is the architecture figure used in the manuscript.

- **PSConv**：通过非对称填充及水平、垂直卷积分支提取多方向局部特征。 / Extracts multidirectional local features through asymmetric padding and horizontal and vertical convolution branches.
- **FDPN**：通过FocusFeature模块聚合不同尺度的特征，并沿自顶向下和自底向上的路径传递融合信息。 / Aggregates features at different scales through FocusFeature modules and propagates fused features along top-down and bottom-up paths.

## 论文实验结果 / Results Reported in the Manuscript

下表为SCB课堂数据子集上的验证集结果，检测类别为举手、阅读和书写。它不是表情识别实验结果，也不是本次整理代码后重新运行得到的结果。

The table reports validation results on the SCB classroom subset for hand raising, reading, and writing. These are the results reported in the manuscript, not facial-expression results or a new run of this release.

| Model | mAP50:95 | Parameters (M) | GFLOPs |
|---|---:|---:|---:|
| DEIM | 0.394 | 3.72 | 7.12 |
| DEIM + PSConv | 0.387 | 4.24 | 8.84 |
| DEIM + FDPN | 0.418 | 4.67 | 11.27 |
| **DEIM-FP** | **0.436** | **5.19** | **13.19** |

论文使用5,193张训练图像和1,671张验证图像，输入尺寸为640×640，训练160轮，batch size为8，优化器为AdamW，主学习率为0.0008，随机种子为42。DEIM-FP配置关闭骨干网络预训练。

The manuscript uses 5,193 training images and 1,671 validation images, an input size of 640×640, 160 epochs, a batch size of 8, AdamW with a main learning rate of 0.0008, and seed 42. Backbone pretraining is disabled in the DEIM-FP configuration.

## 代码目录 / Code Structure

| Path | 用途 / Purpose |
|---|---|
| `configs/deim/` | DEIM基线及模块消融配置。 / DEIM baseline and ablation configurations. |
| `engine/backbone/hgnetv2_psconv.py` | 引入PSConv的HGNetv2骨干。 / HGNetv2 backbone incorporating PSConv. |
| `engine/extre_module/custom_nn/conv_module/psconv.py` | PSConv实现。 / PSConv implementation. |
| `engine/extre_module/custom_nn/neck/FDPN.py` | FDPN实现。 / FDPN implementation. |
| `train.py` | 训练与验证入口。 / Training and validation entry point. |
| `tools/inference/torch_inf.py` | 图像推理。 / Image inference. |
| `figures/DEIM_FP_architecture.png` | 论文中的模型结构图。 / Architecture figure from the manuscript. |

## 环境与数据 / Environment and Data

先安装与本机CUDA环境匹配的PyTorch及torchvision，再安装其余依赖。以下命令均在本文件夹中执行。

Install PyTorch and torchvision compatible with your CUDA environment, then install the remaining dependencies. Run the commands below from this folder.

```bash
pip install -r requirements.txt
```

数据采用COCO格式。修改`configs/dataset/custom_detection.yml`中训练集和验证集的`img_folder`、`ann_file`，使其指向本机文件。当前配置保留原服务器路径。

Use COCO-format annotations. Set `img_folder` and `ann_file` for the training and validation datasets in `configs/dataset/custom_detection.yml` to your local paths. The configuration currently retains the original server paths.

本代码仓库不包含课堂图像数据或训练权重，请自行准备相应数据及模型文件。

This code repository does not include classroom images or trained weights. Prepare the corresponding data and model files separately.

## 训练与验证 / Training and Validation

| Model | Configuration |
|---|---|
| DEIM | [deim_hgnetv2_n_custom.yml](configs/deim/deim_hgnetv2_n_custom.yml) |
| DEIM + PSConv | [deim_hgnetv2_psconv_n_custom.yml](configs/deim/deim_hgnetv2_psconv_n_custom.yml) |
| DEIM + FDPN | [deim_hgnetv2_fdpn_n_custom.yml](configs/deim/deim_hgnetv2_fdpn_n_custom.yml) |
| DEIM-FP | [deim_hgnetv2_psconv_fdpn_n_custom.yml](configs/deim/deim_hgnetv2_psconv_fdpn_n_custom.yml) |

单GPU训练 / Single-GPU training:

```bash
python train.py -c configs/deim/deim_hgnetv2_psconv_fdpn_n_custom.yml --seed 42 --output-dir outputs/deim_fp
```

验证 / Validation:

```bash
python train.py -c configs/deim/deim_hgnetv2_psconv_fdpn_n_custom.yml --test-only -r outputs/deim_fp/best_stg2.pth --output-dir outputs/deim_fp_eval
```

代码按训练阶段保存`best_stg1.pth`和`best_stg2.pth`。请将命令中的路径替换为实际需要评估的模型文件。

The code saves `best_stg1.pth` and `best_stg2.pth` for the two training stages. Replace the checkpoint path with the model you intend to evaluate.

图像推理 / Image inference:

```bash
python tools/inference/torch_inf.py -c configs/deim/deim_hgnetv2_psconv_fdpn_n_custom.yml -r outputs/deim_fp/best_stg2.pth -i image.jpg -o inference_results/exp
```

## 致谢与许可证 / Acknowledgments and License

本代码基于DEIM及其相关开源实现，保留原有许可证和代码归属声明。 / This code builds on DEIM and related open-source implementations. The existing license and source attributions are retained.

- [DEIM](https://github.com/ShihuaHuang95/DEIM)
- [D-FINE](https://github.com/Peterande/D-FINE)
- [RT-DETR](https://github.com/lyuwenyu/RT-DETR)
- [PSConv](https://arxiv.org/abs/2412.16986)

详见[LICENSE](LICENSE)。此许可证文件属于模型代码目录，不自动授权公开课堂数据或教师教学设计。 / See [LICENSE](LICENSE). This license belongs to the model-code directory and does not by itself grant permission to publish classroom data or teachers' instructional designs.