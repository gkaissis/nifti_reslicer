#/usr/bin/env/python

import nibabel as nib
from dataloader import NiftiAndMaskLoader
from conversion import convert, create_niftis
from pathlib import Path
from tqdm import tqdm
import sys

if __name__ == "__main__":
    niftis = input("Enter the path to the NIFTIs:  ")
    masks = input("Enter the path to the masks:  ")

    output_vol_folder = Path(input("Enter the path to output the resampled volumes:  ")).resolve()
    if not output_vol_folder.exists() or not output_vol_folder.is_dir():
        raise RuntimeError("Please provide a path to a valid directory")

    output_mask_folder = Path(input("Enter the path to output the resampled masks:  ")).resolve()
    if not output_mask_folder.exists() or not output_vol_folder.is_dir():
        raise RuntimeError("Please provide a path to a valid directory")

    n = NiftiAndMaskLoader(niftis, masks)

    name_splitter = lambda x: x.stem.split(".")[0]

    for old_volume_name, old_mask_name, old_volume, old_mask in tqdm(zip(n.image_paths, n.mask_paths, n.images, n.masks)):

        new_volume_name = name_splitter(old_volume_name) + "_resampled.nii.gz"
        new_mask_name = name_splitter(old_mask_name) + "_resampled.nii.gz"

        conversion_result = convert(old_volume, old_mask)
        new_volume = create_niftis(*conversion_result[0])
        new_mask = create_niftis(*conversion_result[1])
        nib.save(new_volume, str(Path(output_vol_folder) / Path(new_volume_name)))
        nib.save(new_mask, str(Path(output_mask_folder) / Path(new_mask_name)))

    print("Conversion complete.")
    sys.exit(0)