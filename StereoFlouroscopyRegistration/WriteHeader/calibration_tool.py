from PIL import Image as image
from PIL.TiffTags import TAGS
import numpy
import os
import SimpleITK as sitk

class CalibrationTool:
    """Read and store calibration data from camera calibration"""

    def __init__(self):
        self.file = []

        self.principle_dist = 0
        self.x_offset = 0
        self.y_offset = 0
        self.pixel_size = 0

        self.xray_position = []
        self.image_normal = []
        self.image_up = []

        self.camera_path = 0
        self.image_all = []

        self.direction_matrix = []

    def read_file(self, base_dir, file_dir, filename):
        """Given filename, read all lines in file"""

        path = base_dir + file_dir + filename
        open_file = open(path, "r")
        self.file = open_file.readlines()

    def parse_file(self):
        """Parse and clean all values from the calibration file"""

        self.principle_dist = self.file[1].strip()
        self.x_offset = float(self.file[2].strip())
        self.y_offset = float(self.file[3].strip())
        self.pixel_size = float(self.file[4].strip())

        self.xray_position = self.file[6].strip().split()
        self.image_normal = self.file[7].strip().split()
        self.image_up = self.file[8].strip().split()

    def get_calibration_data(self, base_dir, file_dir, filename):
        self.read_file(base_dir, file_dir, filename)
        self.parse_file()
        self.get_direction()

    def open_directory(self, base_dir, image_path):
        self.camera_path = base_dir + image_path
        self.image_all = os.listdir(self.camera_path)

    def shift_origin(self, img):
        """Move the image origin from center to lower left for ITK"""
        w, h, z = img.GetSize()

        dx_mm = (float(w) / 2) * self.pixel_size
        dy_mm = (float(h) / 2) * self.pixel_size
        
        P = [self.x_offset, self.y_offset, 0]
        Q = [dx_mm, dy_mm, 0]
        
        origin = [-1 * float(self.principle_dist) * float(x) for x in self.image_normal]
        origin = numpy.subtract(numpy.subtract(origin, P), Q)

        return origin

    def get_direction(self):
        n_vector = numpy.array([float(x) for x in self.image_normal])
        v_vector = numpy.array([float(x) for x in self.image_up])
        u_vector = numpy.cross(n_vector, v_vector)
        u_vector = u_vector.tolist()

        direction_matrix = self.image_normal + self.image_up + u_vector
        self.direction_matrix = [float(x) for x in direction_matrix]

    def write_metadata(self, img_vol):
        origin = self.shift_origin(img_vol)
        img_vol.SetSpacing([self.pixel_size,self.pixel_size,1])
        img_vol.SetOrigin(origin)

        img_vol.SetDirection(self.direction_matrix)

        return img_vol

    def write_new_image(self, output_path):
        for i in range(0, len(self.image_all)-1):
            img = sitk.ReadImage(os.path.join(self.camera_path, self.image_all[i]))
            img_vol = sitk.JoinSeries(img)
            corrected_img = self.write_metadata(img_vol)

            img_path = os.path.join(self.camera_path, output_path)
            filename = self.image_all[i].split('.')
            sitk.WriteImage(corrected_img, os.path.join(img_path, 'EDITED-' + filename[0] + '.mha'))

    def open_edited(self, path):
        img = sitk.ReadImage(path)
    
    def write_3d(self,inputPath,outputPath,filename):
        img = sitk.ReadImage(inputPath)
        filename = filename.split('.')
        sitk.WriteImage(img, os.path.join(outputPath, 'EDITED-' + filename[0] + '.mha'))

