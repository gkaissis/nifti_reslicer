from pathlib import Path
import nibabel as nib

class NiftiAndMaskLoader:
    def __init__(self, path_to_nifti_dir, path_to_mask_dir):
        self.path_to_nifti_dir = str(Path(path_to_nifti_dir).resolve())
        if not Path(self.path_to_nifti_dir).exists() and Path(self.path_to_nifti_dir).is_dir():
            raise RuntimeError("Folder does not exists or is not a directory")

        self.path_to_mask_dir = str(Path(path_to_mask_dir).resolve())
        if not Path(self.path_to_mask_dir).exists() and Path(self.path_to_mask_dir).is_dir():
            raise RuntimeError("Folder does not exists or is not a directory")

        self.image_paths = [nifti for nifti in Path(self.path_to_nifti_dir).rglob("*.nii.*")]

        get_mask = lambda x: Path(self.path_to_mask_dir).resolve() / Path(x.parts[-1])

        self.mask_paths = [get_mask(image) for image in self.image_paths]

        if not len(self.image_paths) == len(self.mask_paths):
            raise RuntimeError(
                f"Number of images should match number of masks. Found {len(self.images)} images and {len(self.masks)} masks."
            )

        self.images = [nib.load(str(image)) for image in self.image_paths]
        self.masks = [nib.load(str(mask)) for mask in self.mask_paths]
