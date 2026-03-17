#!/usr/bin/env python3
"""Minimal TensorFlow training stub for Jenkins pipeline."""

import os

def main():
    os.makedirs('models', exist_ok=True)
    with open('models/tensorflow_stub.txt', 'w') as f:
        f.write('TensorFlow training stub executed')
    print('TensorFlow stub complete; created models/tensorflow_stub.txt')

if __name__ == '__main__':
    main()
