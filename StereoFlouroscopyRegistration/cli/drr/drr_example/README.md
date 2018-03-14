This is an example folder containing the following files: 
MAIN_DRR_EXAMPLE.PY  			This file runs all the scripts listed below to generate drr images.

SCRIPT_FILTERS.PY			This file contains all necessary filters 
SCRIPT_LIBRARIES.PY			This file imports all necessary libraries
SCRIPT_RAYCASTINTERPOLATOR.PY		This file initializes the raycast filter. 
SCRIPT_READER.PY			This file reads the image information. 
SCRIPT_SETCALIBRATIONINFO.PY		This file reads calibration information and sets the calibration files. 
SCRIPT_TRANSFORMATION.PY		This file initializes the transformation matrix (here identity)
SCRIPT_WRITEIMAGE.PY			This file writes the generated drr images. 
SCRIPT_WRITETRANSFORMEDVOL.PY		This file writes the generated transformed volume (inactive for now). 

CAL_CAM1.TXT				This file contains the calibration information -- sagittal plane view.
CAL_CAM2.TXT				This file contains the calibration information -- frontal plane view. 
	
TEST_CAM1.NII				This file contains the drr in the sagittal plane. 
TEST_CAM2.NII				This file contains the drr in the frontal plane. 

TRANSFORMED_CT.NII			This file contains the 3D CT model to be used to generate the drrs. 

-> To do: 
		1- incorporate the rigid body transformation into the function. 
		2- incorporate the volume writing module into the code. 
		3- Making sure that the calibration information, image generated, etc all match. 
		4- Study the header files and make sure that the image metadata makes sense. 
		5- Input these images to the registration code for debug. 
		
