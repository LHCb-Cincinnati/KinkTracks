#!/bin/bash

if test -e DecayAngle.py; then
  python DecayAngle.py
fi

if test -e DecayAngle_phi.py; then
  python DecayAngle_phi.py
fi

if test -e DecayAngle_theta.py; then
  python DecayAngle_theta.py
fi

if test -e DecayLength.py; then
  python DecayLength.py
fi