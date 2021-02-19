"""
Copyright (C) 2019 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""

import os
from collections import OrderedDict

from gaugan import data
from gaugan.options.test_options import TestOptions
from gaugan.models.pix2pix_model import Pix2PixModel
from gaugan.util.visualizer import Visualizer
from gaugan.util import html


def doit(arg_list=None):
    opt = TestOptions().parse(arg_list)

    dataloader = data.create_dataloader(opt)

    model = Pix2PixModel(opt)
    model.eval()

    visualizer = Visualizer(opt)

    # create a webpage that summarizes the all results
    web_dir = os.path.join(opt.results_dir, opt.name,
                           '%s_%s' % (opt.phase, opt.which_epoch))
    webpage = html.HTML(web_dir,
                        'Experiment = %s, Phase = %s, Epoch = %s' %
                        (opt.name, opt.phase, opt.which_epoch))

    # test
    for i, data_i in enumerate(dataloader):
        if i * opt.batchSize >= opt.how_many:
            break

        generated = model(data_i, mode='inference')

        img_path = data_i['path']
        for b in range(generated.shape[0]):
            print('process image... %s' % img_path[b])
            visuals = OrderedDict([('input_label', data_i['label'][b]),
                                   ('synthesized_image', generated[b])])
            visualizer.save_images(webpage, visuals, img_path[b:b + 1])

    webpage.save()
