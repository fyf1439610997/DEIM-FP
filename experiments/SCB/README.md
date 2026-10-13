# SCB training records / SCB训练记录

This folder contains training histories for the six classroom-detection runs: DEIM, its PSConv and FDPN variants, DEIM-FP, D-FINE-n, and RT-DETRv2-R18. No checkpoints, classroom images, or training-batch images are included.

本目录提供六组课堂检测实验的训练过程记录：DEIM、PSConv和FDPN变体、DEIM-FP、D-FINE-n及RT-DETRv2-R18。不包含模型权重、课堂图像或训练批次图片。

## Files / 文件

Each run has three files:

- `log.txt`: original JSON Lines log, one epoch per line. Learning rate, losses, COCO validation metrics, epoch index and logged parameter count are retained unchanged.
- `args.json`: original saved runtime configuration, including the resolved model architecture and training settings. Dataset paths are the original training-server paths; update local code configurations when reproducing the experiment.
- `metrics.csv`: the same per-epoch scalar values, with the 12 COCO metrics expanded into named columns for viewing in a spreadsheet.

每组实验包含原始逐轮日志`log.txt`、原始运行参数`args.json`及便于查看的逐轮指标`metrics.csv`。原始日志与参数文件未改写；参数中的数据路径仍指向原训练服务器。

`summary.csv` reports the highest logged validation AP and its epoch as the primary result for each run; final-epoch values are retained as reference columns. `source_checksums.json` contains SHA-256 hashes of the copied original files. All epoch indices are zero-based: epoch 159 is the 160th epoch.

`summary.csv`以各组历史最高验证AP及其轮次为主要汇总结果，最后一轮数值仅作为参考列；`source_checksums.json`记录原始文件的SHA-256。轮次编号从0开始，因此159对应第160轮。

## Best recorded validation results / 最佳验证结果

| Model | Logged epochs | Best AP50:95 | Best epoch index | Final AP50:95 (reference) |
|---|---:|---:|---:|---:|
| DEIM baseline | 160 | 0.394163 | 158 | 0.393739 |
| DEIM + PSConv | 160 | 0.391094 | 153 | 0.386629 |
| DEIM + FDPN | 160 | 0.420856 | 154 | 0.418256 |
| DEIM-FP | 160 | 0.436794 | 158 | 0.436453 |
| D-FINE-n | 160 | 0.332860 | 155 | 0.324901 |
| RT-DETRv2-R18 | 120 | 0.438717 | 96 | 0.407953 |

This repository summarizes each model using its **highest validation AP50:95 recorded during training**, rather than its final-epoch result. All runs use the same summary rule. DEIM-FP has the highest AP among the four DEIM ablation configurations; RT-DETRv2-R18 has the highest AP among all six runs shown here.

本仓库统一采用各模型训练过程中记录的**最高验证AP50:95**，不采用最后一轮结果作为主要汇总。DEIM-FP在四组DEIM组件实验中最高；六组模型中RT-DETRv2-R18最高。

The final-epoch values remain available for tracing the training history. The previously submitted manuscript used final-epoch values; the repository now presents best-recorded results as the primary summary. These values are extracted from the archived validation logs, not from a new checkpoint evaluation.

最后一轮数值保留用于追溯训练历史。此前提交的论文使用最后一轮数值；本仓库现以最佳记录值为主要汇总。这里的数值提取自原始验证日志，不是重新评估检查点得到的结果。

Epoch indices in this table are copied from `log.txt`. The training code can reload an earlier checkpoint during its second stage, affecting the saved `last_epoch` counter. That checkpoint field should not be substituted for the chronological epoch index in the log without verification.

表中轮次来自`log.txt`。训练代码在第二阶段可能重载较早的检查点，影响所保存的`last_epoch`计数；未核对前不能用该字段直接替代日志中的训练轮次。

The logger names the validation field `test_coco_eval_bbox`; these runs use the SCB validation split. This field name does not establish an independent test set. In `metrics.csv`, AP50:95 is the first value in that 12-element array; AP50 and AP75 are the second and third values. All AP/AR values are fractions, not percentages. `n_parameters` is the count recorded by the training logger, copied without adjustment.

日志字段名为`test_coco_eval_bbox`，但这些实验对应SCB验证集，不因此变成独立测试集。数组第1至3项依次为AP50:95、AP50和AP75；AP/AR采用0至1数值。`n_parameters`保留训练日志记录值，未另行调整。

These are archived experiment records, not new experiments rerun when publishing the repository. Re-evaluating a supplied checkpoint can produce a different result if it is a different epoch or is evaluated with different settings. The checkpoints themselves are not distributed in this folder.

这些文件是已有实验记录，不是发布仓库时重新运行的实验。若重新评估的检查点轮次或设置不同，结果可能不同。本目录不分发检查点。

Return to the [repository README](../../README.md).
