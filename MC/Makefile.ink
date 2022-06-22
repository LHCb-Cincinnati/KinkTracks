# PYTHIA configuration file.
# Generated on Wed Mar 30 11:23:15 EDT 2022 with the user supplied options:
# --with-python-config=python3-config
# --with-root=

# Install directory prefixes.
PREFIX_BIN=/Users/mohamedelashri/Desktop/LHCb/pythia/bin
PREFIX_INCLUDE=/Users/mohamedelashri/Desktop/LHCb/pythia/include
PREFIX_LIB=/Users/mohamedelashri/Desktop/LHCb/pythia/libecho 
PREFIX_SHARE=/Users/mohamedelashri/Desktop/LHCb/pythia/share/Pythia8

# Compilation flags (see ./configure --help for further documentation).
CXX=g++
CXX_COMMON=-O2 -std=c++11 -pedantic -W -Wall -Wshadow -fPIC -pthread
CXX_SHARED=-dynamiclib
CXX_SONAME=-Wl,-dylib_install_name,@rpath/
LIB_SUFFIX=.dylib
OBJ_COMMON=

EVTGEN_USE=false
EVTGEN_CONFIG=
EVTGEN_BIN=
EVTGEN_INCLUDE=
EVTGEN_LIB=

FASTJET3_USE=false
FASTJET3_CONFIG=
FASTJET3_BIN=
FASTJET3_INCLUDE=
FASTJET3_LIB=

HEPMC2_USE=false
HEPMC2_CONFIG=
HEPMC2_BIN=
HEPMC2_INCLUDE=
HEPMC2_LIB=

HEPMC3_USE=false
HEPMC3_CONFIG=
HEPMC3_BIN=
HEPMC3_INCLUDE=
HEPMC3_LIB=

LHAPDF5_USE=false
LHAPDF5_CONFIG=
LHAPDF5_BIN=
LHAPDF5_INCLUDE=
LHAPDF5_LIB=

LHAPDF6_USE=false
LHAPDF6_CONFIG=
LHAPDF6_BIN=
LHAPDF6_INCLUDE=
LHAPDF6_LIB=

POWHEG_USE=false
POWHEG_CONFIG=
POWHEG_BIN=
POWHEG_INCLUDE=
POWHEG_LIB=

RIVET_USE=false
RIVET_CONFIG=
RIVET_BIN=
RIVET_INCLUDE=
RIVET_LIB=

ROOT_USE=true
ROOT_CONFIG=root-config
ROOT_BIN=/opt/homebrew/Cellar/root/6.26.00/bin/
ROOT_INCLUDE=-I/opt/homebrew/Cellar/root/6.26.00/include/root
ROOT_LIB=-L/opt/homebrew/Cellar/root/6.26.00/lib/root -Wl,-rpath,/opt/homebrew/Cellar/root/6.26.00/lib/root -lCore

GZIP_USE=false
GZIP_CONFIG=
GZIP_BIN=
GZIP_INCLUDE=
GZIP_LIB=

PYTHON_USE=true
PYTHON_CONFIG=python3-config
PYTHON_BIN=
PYTHON_INCLUDE=-I/opt/homebrew/Cellar/python@3.8/3.8.13/Frameworks/Python.framework/Versions/3.8/include/python3.8 -I/opt/homebrew/Cellar/python@3.8/3.8.13/Frameworks/Python.framework/Versions/3.8/include/python3.8
PYTHON_LIB=

MG5MES_USE=false
MG5MES_CONFIG=
MG5MES_BIN=
MG5MES_INCLUDE=
MG5MES_LIB=

OPENMP_USE=false
OPENMP_CONFIG=
OPENMP_BIN=
OPENMP_INCLUDE=
OPENMP_LIB=

MPICH_USE=false
MPICH_CONFIG=
MPICH_BIN=
MPICH_INCLUDE=
MPICH_LIB=

HDF5_USE=false
HDF5_CONFIG=
HDF5_BIN=
HDF5_INCLUDE=
HDF5_LIB=

HIGHFIVE_USE=false
HIGHFIVE_CONFIG=
HIGHFIVE_BIN=
HIGHFIVE_INCLUDE=
HIGHFIVE_LIB=
