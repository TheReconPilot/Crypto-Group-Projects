# LPN and the HB Protocol

- Presentation Slides: http://bit.ly/lpnhb

## HB Protocol

The Hopper Blum protocol is a shared secret-key authentication protocol designed for low-cost devices like RFID tags. It is based on the Learning Parity with Noise (LPN) problem.

The files provided here:

- `HBProtocol.py` - Has an LPN oracle class for the protocol, used by the other programs
- `BruteForceHB.py` - Demonstration of a brute force attack against HB Protocol, with a very small key length of 5 (can be changed in the program)
- `DecisionTreeClassifier.py` - A program to train a Decision Tree Classifier on the network data sniffed from a HB cryptosystem and attempt to predict the secret key. A demonstration with key length 12 is shown.

## Requirements

The requirements for the program files are present in the `requirements.txt` file and can be installed with

```sh
pip install -r requirements.txt
```

## Demos

### Brute Force Attack

```sh
python BruteForceAttack.py
```

![](https://i.imgur.com/lrYc8Z7.png)

### Decision Tree Classifier

```sh
python DecisionTreeClassifier.py
```

![](https://i.imgur.com/8LSSOL7.png)

![](https://i.imgur.com/ZuFxKnl.png)