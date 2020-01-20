import nibabel as nib
from dipy.align.reslice import reslice
import numpy as np
from typing import Tuple

def get_pixels(image:nib.Nifti1Image, mask:nib.Nifti1Image) ->np.ndarray:
    '''
    Get image pixels from a nifti image.
    '''
    return (image.get_data(), mask.get_data())

def get_affines(image:nib.Nifti1Image, mask:nib.Nifti1Image)->Tuple[np.ndarray, np.ndarray]:
    im_aff = image.affine
    mask_aff = mask.affine
    assert im_aff.tolist() == mask_aff.tolist(), ("Image and Mask Affines do not match.")
    return (image.affine, mask.affine)

def get_zooms(image:nib.Nifti1Image, mask:nib.Nifti1Image)-> Tuple[Tuple, Tuple]:
    im_zooms = image.header.get_zooms()
    mask_zooms = mask.header.get_zooms()
    assert all(im_zooms) == all(mask_zooms), ("Image and Mask Pixel Dimensions do not match.")
    return (im_zooms, mask_zooms)

def convert(image:nib.Nifti1Image, mask:nib.Nifti1Image, new_pixel_dims:Tuple[float,...]=(1.,1.,1.))-> Tuple[Tuple,Tuple]:

    im_pixels, mask_pixels=get_pixels(image, mask)
    im_affine, mask_affine=get_affines(image, mask)
    im_zooms, mask_zooms = get_zooms(image, mask)

    im_re, im_aff_re = reslice(im_pixels, im_affine, im_zooms, new_pixel_dims, order=1, num_processes=0)
    mask_re, mask_aff_re=reslice(mask_pixels, mask_affine, mask_zooms, new_pixel_dims, order=1, num_processes=0)

    assert all(im_re.shape) == all(mask_re.shape), ("New image and new mask shapes do not match")
    assert im_aff_re.tolist() == mask_aff_re.tolist(), ("New image and new mask affines do not match")

    return ((im_re, im_aff_re), (mask_re, mask_aff_re))

def create_niftis(array: np.array, affine: Tuple[float, float, float]) -> nib.Nifti1Image:
    return nib.Nifti1Image(array, affine)
