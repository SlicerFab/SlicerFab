Work in Progress - Please use with caution and add improvements if you can.


Usage:
1. Clone this repository
2. Install [Slicer](http://download.slicer.org)
3. Either add this as a module to Slicer by editing the application settings or run with a commmand like this: 
`./Slicer --additional-module-paths ~/slicer4/latest/SlicerFab/BitmapGenerator/`
4. Load data and set up Volume Rendering (see docs and examples at [slicer.org](http://slicer.org)
5. Select the BitmapGenerator module
6. Set the output path (/tmp by default, for windows change to c:/TEMP or something)
7. Click Apply and let the slices get generated.

More info:[paper](https://www.liebertpub.com/doi/pdf/10.1089/3dp.2017.0140), [discussion](https://discourse.slicer.org/t/printing-volume-renderings-in-plastic/3017)


# Process

Turns this:
![rendering.png](rendering.png)

Into this:
![slices.png](slices.png)
