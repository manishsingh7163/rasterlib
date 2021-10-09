# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:27:28 2018

@author: viveks01
"""


def extractByMaskReturnList(flRasterName, gdMask):
    """
    Takes a Raster Image and a Geopandas dataframe and returns 
    [outImage,outMeta,outTransform]
    """
    import rasterio
    with rasterio.open(flRasterName) as src:
        outImage, outTransform = rasterio.mask.mask(
            src, gdMask.geometry, crop=True)
        outMeta = src.meta

    outMeta.update({"driver": "GTiff",
                    "height": outImage.shape[1],
                    "width": outImage.shape[2],
                    "transform": outTransform})

    return [outImage, outMeta, outTransform]


def extractAndSaveByMaskReturnList(flRasterName, gdMask, newrasterFlName):
    '''
    Takes a Raster Image, a Geopandas dataframe and newrasterFlName:  file name. 
    filename should end with .tif
    Extract the image and saves it in a file by the newFLName
    returns nothing

    '''
    import rasterio
    with rasterio.open(flRasterName) as src:
        outImage, outTransform = rasterio.mask.mask(
            src, gdMask.geometry, crop=True)
        outMeta = src.meta

    outMeta.update({"driver": "GTiff",
                    "height": outImage.shape[1],
                    "width": outImage.shape[2],
                    "transform": outTransform})

    subsetNlList = [outImage, outMeta, outTransform]
    with rasterio.open(newrasterFlName, "w", **subsetNlList[1]) as dest:
        dest.write(subsetNlList[0])


def rasterZonalStats(flRasterName,vectorMask,tag='noTag',noDataVal=0, paramList=['count', 'sum', 'std', 'min', 'max', 'mean', 'median', 'nodata'],categorical=False, all_touched=False):
    print(paramList)
    import pandas as pd 
    from rasterstats import zonal_stats
    tagDict={ele:tag+'_'+ele  for ele in paramList}
    zsCity = zonal_stats(vectorMask.geometry, flRasterName, nodata=noDataVal,
                      stats=paramList,
                      categorical=categorical,
                      all_touched=all_touched)
    zsGridResults = pd.DataFrame(zsCity)
    zsGridResults.rename(columns=tagDict,inplace=True)
    gridZonalStats = vectorMask.join(zsGridResults)
    return gridZonalStats

def rasterZonalStatsCategorical(flRasterName,vectorMask,tag='noTag',noDataVal=0, paramList=['count', 'sum', 'std', 'min', 'max', 'mean', 'median', 'nodata'],categorical=False):
    print(paramList)
    import pandas as pd 
    from rasterstats import zonal_stats
    tagDict={ele:tag+'_'+ele  for ele in paramList}
    zsCity = zonal_stats(vectorMask.geometry, flRasterName, categorical=True)
    zsGridResults = pd.DataFrame(zsCity)
    zsGridResults.rename(columns=tagDict,inplace=True)
    gridZonalStats = vectorMask.join(zsGridResults)
    return gridZonalStats



def rasterZonalStatsCategoricalCMAP(flRasterName,vectorMask,tag='noTag',noDataVal=0, paramList=['count', 'sum', 'std', 'min', 'max', 'mean', 'median', 'nodata'],categorical=False,cmap={}):
    print(paramList)
    import pandas as pd 
    from rasterstats import zonal_stats
    tagDict={ele:tag+'_'+ele  for ele in paramList}
    zsCity = zonal_stats(vectorMask.geometry, flRasterName, categorical=True,category_map=cmap)
    zsGridResults = pd.DataFrame(zsCity)
    zsGridResults.rename(columns=tagDict,inplace=True)
    gridZonalStats = vectorMask.join(zsGridResults)
    return gridZonalStats

