# Kage Bunshin Network Worm

![image](https://drive.google.com/uc?export=download&id=1lyXNnnGjDA1qYFj6bbvFLnzYL2lQZO9K)

## Disclaimer

This script is for educational purposes only, I don't endorse or promote it's illegal usage

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Languages](#languages)
4. [Installations](#installations)
5. [Usage](#usage)
6. [Run](#run)

## Overview

This script is a network worm that attempts to spread itself over a LAN by launching an SSH Brute force attack

## Features

- Scans a LAN for active devices
- Attempts SSH brute force attack on each devices in the LAN

## Languages

- Python 3.9.7

## Installations

```shell
git clone https://github.com/favoursyre/network-worm.git && cd network-worm
```

```shell
pip install requirements.txt
```

## Usage

Instantiating the network worm class

```python
port, attacker, target = 22, "Uchiha Minato", "Konoha"
worm = KageBunshin(port, attacker, target)
```

## Run

```bash
python networm.py
```
