import nibabel
from reslicer.dataloader import NiftiAndMaskLoader
from reslicer.conversion import get_affines, get_pixels, get_zooms, convert, create_niftis

n = NiftiAndMaskLoader(
        "/Users/georgioskaissis/Downloads/Task07_Pancreas/imagesTr",
        "/Users/georgioskaissis/Downloads/Task07_Pancreas/labelsTr",
    )

test_im = n.images[0]
test_mask = n.masks[0]

def test_pixels():
    im_px, mask_px = get_pixels(test_im, test_mask)

    assert all(im_px.shape) == all(mask_px.shape)

def test_affines():
    im_aff, mask_aff = get_affines(test_im, test_mask)
    assert im_aff.tolist() == mask_aff.tolist()

def test_zooms():
    im_zooms, mask_zooms = get_zooms(test_im, test_mask)
    assert im_zooms
    assert mask_zooms

def test_convert():
    (new_im, new_aff), (new_mask, new_mask_aff) = convert(test_im, test_mask)
    assert all(new_im.shape) == all(new_mask.shape)
    assert new_aff.tolist() == new_mask_aff.tolist()

def test_creation():
    im_obj = create_niftis(*convert(test_im, test_mask)[0])
    mask_obj = create_niftis(*convert(test_im, test_mask)[1])
    assert isinstance(im_obj, nibabel.Nifti1Image)
    assert isinstance(mask_obj, nibabel.Nifti1Image)