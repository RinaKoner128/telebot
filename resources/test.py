import random
import matplotlib.pyplot as plt
import pymssql
import psycopg2
import numpy as np
import pandas as pd
from resources.conf_adm import adress, adress_adm
import resources.select as select
import time
import datetime
from collections import deque
import resources.TI_base_smev as bs

if datetime.datetime.now().strftime("%H:%M") == "09:02":
    if bs.get_rep_pgu_mfc()["mfc_yest"] < 50:
        print('иририри')
else:
    print(datetime.datetime.now().weekday())
