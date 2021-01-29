# Encounter the four seasons in oil painting

---

- Teng Li
- i@terrytengli.com
- issues contact at my email

---

In this repository, a runnable style transfer demo is included, which is based on cyclegan.

## Get start

Firstly, make sure your python version is ```python=3```

Secondly, the related toolkits should be installed. Try the following statement in your terminal.

```bash
pip install -r requirements.txt
```

Then, the tutorial is finished. Begin your playground by trying the following in your terminal.

```bash
python main.py
```

For more information of ```main.py```, try,

```bash
python main.py -h
```

## File structure

```bash
.
├── input
│   └── input.jpg
├── interface.py
├── main.py
├── models
│   ├── summer2winter.pb
│   └── winter2summer.pb
├── output
│   └── output.jpg
├── README.md
└── requirements.txt
```

## Interface

A flask interface for front-end scheduling is also given in ```interface.py```.

## Cite

**[1]** Zhu, Jun-Yan, et al. "Unpaired image-to-image translation using cycle-consistent adversarial networks." *Proceedings of the IEEE international conference on computer vision*. 2017.

**[2]** [CycleGan-Tensorflow_vanhuyz](https://github.com/vanhuyz/CycleGAN-TensorFlow)