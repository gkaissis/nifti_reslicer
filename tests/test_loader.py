from reslicer.dataloader import NiftiAndMaskLoader


def test_loader():
    n = NiftiAndMaskLoader(
        "/Users/georgioskaissis/Downloads/Task07_Pancreas/imagesTr",
        "/Users/georgioskaissis/Downloads/Task07_Pancreas/labelsTr",
    )

    assert len(n.image_paths) == 281 == len(n.mask_paths)
    assert len(n.images) == 281 == len(n.masks)

