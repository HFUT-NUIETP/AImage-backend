## style transfer

Introduction: Style transfer module of **[HFUT-NUIETP](https://github.com/HFUT-NUIETP)-[AImage](https://github.com/HFUT-NUIETP/AImage-app)**.

### File Structure

```
.
├── README.md
├── requirements.txt
├── in
│   └── content.jpg
├── main.py
├── out
│   └── output.jpg
└── utils
    ├── styles
    ├── models
    │   ├── predict_256_int8.tflite
    │   └── transform_256_int8.tflite
    ├── options.py
    ├── pre_processing.py
    ├── style.py
    └── styles
    └── test.py
```

### Requirements

1) ```Python 3.6```
2) Install dependent packages, try
```
pip install -r requirements.txt
```

### Tutorial

1) optional arguments (use ```python main.py -h```):

```
  -h, --help            show this help message and exit
  --path_content PATH_CONTENT
                        input content image path
  --path_styles PATH_STYLES
                        input style image path
  --style_no STYLE_NO   style no, 0-25
  --path_output PATH_OUTPUT
                        output result path
```

2) test

```
python train.py --path_content in/content.jpg --style_no 0
```

### Results

|  Content | Style  |  Output  |
|  ----  | ----  |  ----  |
| <img src="in/content.jpg" style="zoom:33%;" /> | <img src="utils/styles/style0.jpg" style="zoom:55%;" /> | <img src="out/output.jpg" style="zoom:75%;" /> |

### Reference

1) This implementation is inspired by [Artistic Style Transfer with TensorFlow Lite](https://colab.research.google.com/github/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/models/style_transfer/overview.ipynb?hl=zh-cn), thanks for the authors' open-source spirits.
2) The style transfer functions are based on [Tensorflow Android Demo](https://www.tensorflow.org/lite/examples?hl=zh-cn)