# -*- coding: utf-8 -*-
"""plot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AUPvFP0MMr0siziFfLGg1QfGjqGCX4nW
"""
import os, sys
ROOT_WDIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, ROOT_WDIR)
import csv
import matplotlib.pyplot as plt

with open(ROOT_WDIR +"/generated_data/latlng.csv") as counties:
      countyReader = csv.DictReader(counties)

      for county in countyReader:
          plt.plot(float(county['Longitude']),float(county['Latitude']),'b.')
 
plt.show()