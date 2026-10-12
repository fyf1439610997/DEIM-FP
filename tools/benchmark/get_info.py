"""
Copyright (c) 2024 The D-FINE Authors. All Rights Reserved.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

import argparse
import torch
import torch.nn as nn
import thop

from engine.core import YAMLConfig


def custom_repr(self):
    return f'{{Tensor:{tuple(self.shape)}}} {original_repr(self)}'
original_repr = torch.Tensor.__repr__
torch.Tensor.__repr__ = custom_repr


def main(args, ):
    """main
    """
    cfg = YAMLConfig(args.config, resume=None)

    class Model_for_flops(nn.Module):
        def __init__(self, ) -> None:
            super().__init__()
            self.model = cfg.model.deploy()

        def forward(self, images):
            outputs = self.model(images)
            return outputs

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = Model_for_flops().eval().to(device)

    input_shape = (1, 3, *cfg.yaml_cfg['eval_spatial_size'])
    macs, params = thop.profile(model, inputs=(torch.randn(*input_shape).to(device),), verbose=False)
    flops = macs * 2
    print("Model FLOPs:%.2f   MACs:%.2f   Params:%.2f \n" % (flops, macs, params))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', default="configs/deim/deim_hgnetv2_psconv_fdpn_n_custom.yml", type=str)
    args = parser.parse_args()

    main(args)
