# Introduction

This extension for 3D Slicer creates a full-color image stack suitable for bitmap-based multimaterial 3D printing. In contrast to traditional 3D printing methods, this new technique does not require image segmentation (which is a difficult and labor-intensive processing step) and produces highly detailed physical models.

![Example printed models](https://discourse-cdn-sjc2.com/standard17/uploads/slicer/optimized/2X/a/a496d030927d0e4275076c12a22a39b048e7a5b0_1_382x500.jpg)

More info:
- Hosny et al., "From Improved Diagnostics to Presurgical Planning: High-Resolution Functionally Graded Multimaterial 3D Printing of Biomedical Tomographic Data Sets", 3D Printing and Additive Manufacturing VOL. 5, NO. 2, 2018 [reference](https://www.liebertpub.com/doi/pdf/10.1089/3dp.2017.0140) / [full text](https://www.researchgate.net/profile/Steven_Keating/publication/325436455_From_Improved_Diagnostics_to_Presurgical_Planning_High-Resolution_Functionally_Graded_Multimaterial_3D_Printing_of_Biomedical_Tomographic_Data_Sets/links/5b11804baca2723d997aefbe/From-Improved-Diagnostics-to-Presurgical-Planning-High-Resolution-Functionally-Graded-Multimaterial-3D-Printing-of-Biomedical-Tomographic-Data-Sets.pdf)
- [Article in Science Daily](https://www.sciencedaily.com/releases/2018/05/180530113214.htm)
- [Discussion](https://discourse.slicer.org/t/printing-volume-renderings-in-plastic/3017)

# Process

Turns this:
![rendering.png](rendering.png)

Into this:
![slices.png](slices.png)

# Usage

2. Install a recent nightly version of [3D Slicer](http://download.slicer.org)
3. Start Slicer, open Extension Manager, and install SlicerFab extension
4. Load data and set up Volume Rendering (see docs and examples at [slicer.org](http://slicer.org)
5. Select the BitmapGenerator module
6. Set the output path (/tmp by default, for windows change to c:/TEMP or something)
7. Click Apply and let the slices get generated.

Any questions? Post it on [SlicerFab discussion in Slicer forum](https://discourse.slicer.org/t/printing-volume-renderings-in-plastic/3017)

Work in Progress - Please use with caution and add improvements if you can.
