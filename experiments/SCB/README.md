# SCB training records / SCB训练记录

This folder contains training histories for the six classroom-detection runs: DEIM, its PSConv and FDPN variants, DEIM-FP, D-FINE-n, and RT-DETRv2-R18. No checkpoints, classroom images, or training-batch images are included.

本目录提供六组课堂检测实验的训练过程记录：DEIM、PSConv和FDPN变体、DEIM-FP、D-FINE-n及RT-DETRv2-R18。不包含模型权重、课堂图像或训练批次图片。

## Files / 文件

Each run has three files:

- `log.txt`: original JSON Lines log, one epoch per line. Learning rate, losses, COCO validation metrics, epoch index and logged parameter count are retained unchanged.
- `args.json`: original saved runtime configuration, including the resolved model architecture and training settings. Dataset paths are the original training-server paths; update local code configurations when reproducing the experiment.
- `metrics.csv`: the same per-epoch scalar values, with the 12 COCO metrics expanded into named columns for viewing in a spreadsheet.

每组实验包含原始逐轮日志`log.txt`、原始运行参数`args.json`及便于查看的逐轮指标`metrics.csv`。原始日志与参数文件未改写；参数中的数据路径仍指向原训练服务器。

`summary.csv` compares the final logged epoch and the highest logged validation AP. `source_checksums.json` contains SHA-256 hashes of the copied original files. All epoch indices are zero-based: epoch 159 is the 160th epoch.

`summary.csv`并列列出最后一轮与历史最高验证AP；`source_checksums.json`记录原始文件的SHA-256。轮次编号从0开始，因此159对应第160轮。

## Final epoch and historical maximum / 最后一轮与历史最佳

| Model | Logged epochs | Final AP50:95 | Highest logged AP50:95 | Best epoch index |
|---|---:|---:|---:|---:|
| DEIM baseline | 160 | 0.393739 | 0.394163 | 158 |
| DEIM + PSConv | 160 | 0.386629 | 0.391094 | 153 |
| DEIM + FDPN | 160 | 0.418256 | 0.420856 | 154 |
| DEIM-FP | 160 | 0.436453 | 0.436794 | 158 |
| D-FINE-n | 160 | 0.324901 | 0.332860 | 155 |
| RT-DETRv2-R18 | 120 | 0.407953 | 0.438717 | 96 |

The AP values in the manuscript tables match each run's **final logged epoch**, rounded to three decimal places. Historical maxima are also provided here; they are different summaries of the same training histories. Do not interpret a final-epoch result as the maximum achieved during training, or mix the two when comparing models.

论文表格中的AP数值与各组**最后一轮日志**保留三位小数后的数值一致。本目录同时提供历史最高值。最后一轮结果与历史最高结果是两种统计口径，不能混用。

The logger names the validation field `test_coco_eval_bbox`; these runs use the SCB validation split. This field name does not establish an independent test set. In `metrics.csv`, AP50:95 is the first value in that 12-element array; AP50 and AP75 are the second and third values. All AP/AR values are fractions, not percentages. `n_parameters` is the count recorded by the training logger, copied without adjustment.

日志字段名为`test_coco_eval_bbox`，但这些实验对应SCB验证集，不因此变成独立测试集。数组第1至3项依次为AP50:95、AP50和AP75；AP/AR采用0至1数值。`n_parameters`保留训练日志记录值，未另行调整。

These are archived experiment records, not new experiments rerun when publishing the repository. Re-evaluating a supplied checkpoint can produce a different result if it is a different epoch or is evaluated with different settings. The checkpoints themselves are not distributed in this folder.

这些文件是已有实验记录，不是发布仓库时重新运行的实验。若重新评估的检查点轮次或设置不同，结果可能不同。本目录不分发检查点。

Return to the [repository README](../../README.md).
