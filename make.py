from distutils.core import setup
import glob
import py2exe
setup(windows=[{"script":"Analyze.py","icon_resources":[(1, u"OracleAnalyzeBig.ico")]}],data_files=[("bitmaps",["OracleAnalyze.ico"])])