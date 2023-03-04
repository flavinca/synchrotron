###import modules
import h5py
import numpy as np
import os.path

#initalize variables (determine mask value and input here)
file_path = './computer_science/synchrotron/scan2D_195488.h5'
mask_value = 1

#open h5py file, save data to det_data and scalr 
pyxrf =  h5py.File("./scan2D_195488.h5",'r')
det_data = pyxrf["xrfmap/detsum/counts"]
scalr = pyxrf["xrfmap/scalers/val"]

#evaluate shape of det_data and scalr
print(det_data.shape)
print(scalr.shape)

#set mask of the xrfmap data using numpy array. apply mask to det_data and scalr
mask1 = np.array(det_data) > mask_value
det_data_masked = det_data * mask1
mask2 = np.array(scalr) > mask_value
scalr_masked = scalr

#create new h5 file
path = file_path
savename = f"{os.path.basename(path).split('.')[0]}_pyxrf.h5"
hf = h5py.File(savename, 'w')
dataGrp = hf.create_group("xrfmap/detsum/")
ds_data = dataGrp.create_dataset("counts", data=np.array(det_data_masked))
dataGrp = hf.create_group('xrfmap' + "/positions")
dataGrp.create_dataset("name", data=np.array(pyxrf["xrfmap/positions/name"]))
dataGrp.create_dataset("pos", data=pyxrf["xrfmap/positions/pos"])
dataGrp = hf.create_group('xrfmap' + "/scalers")
dataGrp.create_dataset("name", data=np.array(pyxrf["xrfmap/scalers/name"]))
dataGrp.create_dataset("val", data=np.array(scalr_masked))
mdata = dict(pyxrf["xrfmap/scan_metadata"].attrs)
metadata_grp = hf.create_group('xrfmap' + "/scan_metadata")
for key, value in mdata.items():
    metadata_grp.attrs[key] = value
hf.close()
