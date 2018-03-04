# import win32ui
# import win32print
# import win32con

# INCH = 1440

# hDC = win32ui.CreateDC ()
# hDC.CreatePrinterDC (win32print.GetDefaultPrinter ())
# hDC.StartDoc ("Test doc")
# hDC.StartPage ()
# hDC.SetMapMode (win32con.MM_TWIPS)
# hDC.DrawText ("TEST", (0, INCH * -1, INCH * 8, INCH * -2), win32con.DT_CENTER)
# hDC.EndPage ()
# hDC.EndDoc ()

# ImagePrintWin   (formerly WinPILprint)
# by Kevin Cazabon (kevin@cazabon.com)
# Copyright 2003, all rights reserved
# Partially based on examples by Tim Golden, tim.golden@viacom-outdoor.co.uk

# Version 0.5
# VERSION = 0.5

# Requirements
#    Windows OS (probably won't work with Win95/98/ME?  Not yet tested)
#    A Windows printer
#    PIL (Python Imaging Library)
#    Optional:
#        Pmw (Python MegaWidgets) for the GUI functionality and printer setup dialogs
#        pyCMS (see http://www.cazabon.com/pyCMS) for ICC color management (optional)
#
#
# Usage:
#    ImagePrintWin.findPrinterNames()
#        returns a list of strings, each representing an available printer
#
#    ImagePrintWin.getPrinterCaps(printerName)
#        printerName = string, printer name as returned by ImagePrintWin.findPrinterNames()
#    
#        returns a dictionary describing the printer capabilities.  This info actually
#        isn't usually needed by the programmer except to preview the image layout or to
#        verify if a printer supports the required settings (it's used internally for
#        printing as well as the setup GUI).  Values included in the dictionary are:
#
        # "Standard" win32 printer capability values:
        #    HORZSIZE	        : width of full page in mm
        #    VERTSIZE		    : height of full page in mm
        #    HORZRES            : device units in width of printable area
        #    VERTRES            : device units in height of printable area
        #    PHYSICALWIDTH      : device units in full page width
        #    PHYSICALHEIGHT     : device units in full page height
        #    PHYSICALOFFSETX    : left device margin of unprintable area
        #    PHYSICALOFFSETY    : top device margin of unprintable area
        #    LOGPIXELSX         : device units per inch of horoz. axis (usually the DPI of the printer)
        #    LOGPIXELSY         : device units per inch of vert. axis (usually the DPI of the printer)
        #
        # "Convenience" values are dictionaries that consist of three entries each.  The dictionary keys
        #    in each case are UNITS_DEVICE, UNITS_INCH, and UNITS_MM, and hold the appropriate value
        #    in the units specified.  i.e. printerCaps["res"][UNITS_INCH] = [LOGPIXELSX, LOGPIXELSY]
        #    "res" = list of printer resolution in x and y dimensions, dots or pixels per unit (UNITS_DEVICE is always [1, 1])
        #    "printerMargins" = a 4-item list of left, top, right, bottom margins in the unit specified
        #    "printableArea" = a 2-item list of width, height of printable area in the unit specified
        #    "pageSize" = a 2-item list of the width, height of the full page area in the unit specified
        
#    ImagePrintWin.printImage(im, settings = None, **kw)
#        im = either a string path to an image file, or an already open PIL image object
#        settings = a settings dictionary to use for printing options (can be overridden with keywords)
#
#        returns a 3-tuple of (result, message, settings).
#            result == int, corresponding to a STATUS value as listed in the constants section below.
#            message == string that describes the result and/or any errors that may have happened
#            settings == a dictionary of settings that were used for printing the image.
#                you can actually pass settings back in for printing other images if you want
#                to use the same settings (this is the same type of settings object that the
#                printer setup GUI returns).  When settings are returned, all values will be converted
#                to UNITS_DEVICE, however the original units type will be stored in "displayUnits" if
#                that value was not specified originally.
#
#        keywords you can use for printing, NONE are required if you are ok with default behavior:
#
        #    printerName        : (string), name of the printer you wish to print with, uses default printer if not specified
        #                            use findPrinterNames to find the names you can use
        #    documentName       : (string), arbitrary name of the document you're printing, may show up in printer queue dialog
        #    imageRes           : tuple or list of (xRes, yRes) of the image per unit specified by the units value (defaults to inches)
        #    imageSize          : tuple or list of (xSize, ySize) of the final output image, specified in the units defined by the units value (defaults to UNITS_DEVICE)
        #    rotationType       : integer corresponding to one of the valid ROTATION constants defined below (defaults to ROTATION_NONE)
        #    sizingType         : integer corresponding to one of the SIZING constants defined below (defaults to SIZING_NONE)
        #    positioningType    : integer corresponding to one of the POSITIONING constants defined below (defaults to POSITIONING_MANUAL)
        #    units              : integer corresponding to one of the UNITS constants defined below (defaults to UNITS_DEVICE)
        #    displayUnits       : integer corresponding to one of the UNITS constants defined below (defualts to UNITS_DEVICE) (this value is only used in the printerSetup GUI)
        #    copies             : integer defining number of copies to print (defaults to 1)
        #    margins            : 2-item tuple or list defining the left, top corner of the image with respect to the top-left of the page, in the units specified by the units value (defaults to [0,0])
        #    marginsFromPrintableArea:   if True, the margins value is referenced from the top left corner of the printable area rather than the top left corner of the full page (defaults to False)
        #    applyColorManagement    : if True (and pyCMS is available), color management will be applied based on profiles specified, or used to convert color spaces as required (defaults to False)
        #    ICCinputProfileRGB      : (string), path to RGB profile for input images
        #    ICCinputProfileCMYK     : (string), path to CMYK profile for input images
        #    ICCoutputProfile        : (string), path to RGB output profile for your printer (yes, always RGB... even with a CMYK printer!)
        #    ICCrenderingIntent      : (int), rendering intent for ICC conversion.  See pyCMS or constants listed below for details (defaults to INTENT_COLORIMETRIC)
        #    currentProfileLUT       : do not manually specify, used internally for speed purposes when re-using settings.

#    class printerSetup (parent, im = None, allowPrinting = True, closeAfterPrint = True, hideICC = False, settings = None, **kw)
        #    parent = tkinter parent window to this tkinter.Toplevel widget
        #    im = either a PIL image object or a string path to a valid image file
        #    allowPrinting = bool (True/False), if True and im != None, user will have option of printing directly from the setup dialog with a "Print" button
        #    closeAfterPrint = bool (True/False), if True and the user clicks the "Print" button (if shown), the dialog will automatially close after sending the print to the printer
        #    hideICC = bool (True/False), if True the ICC setup tab will not be shown to the user (if pyCMS is available, if not it will always be hidden)
        #    settings = a valid (even if incomplete) settings dictionary the same as used with printImage()
        #    **kw = keyword arguments that will override items in settings or the default values for printing (i.e. you can specify imageRes = [300,300] in the arguments to printerSetup)
        
        #    Methods
            # (result, message, settings) = printerSetupInstance.getSettings()
            # result, message, and settings are the same as returned from printImage
            #
            # this method will result in the printerSetup GUI showing, and will block until the GUI is closed.  The GUI can be closed
            #    several ways, and the result value will tell you how the user closed the dialog.
            
        # Typical usage:

            ## simple use, show dialog and allow user to print directly from the setup GUI
            #import Image, tkinter
            #main = tkinter.Tk()
            #im = Image.open("c:\\temp\\test.tif")
            
            #gui = printerSetup(main, im)
            #result, message, settings = gui.getSettings()
            
            #main.mainloop()
        
            #------------------------------------------------
            ## getting settings separately from printing
            #import Image, tkinter
            #main = tkinter.Tk()
    
            #gui = printerSetup(main)    # you can pass in your own default settings by keyword or through a settings dictionary here
            #result, message, settings = gui.getSettings()
    
            ## do whatever else you want
    
            #im = Image.open("c:\\temp\\test.tif")
            #printImage(im, settings)

            #main.mainloop()
        

# Version History
#
#    0.5 (November 2, 2003)
#        -fixed error dialog when printing fails (missed tkinter. for a Label)
#        -did some work to fix printing to Network printers, but still not working properly
#
#    0.4 (October 28, 2003)
#        -upgraded preview tab look
#        -fixed image placement on printers with printerMargins other than 0
#        -fixed sizing issues when using mm... was off by a factor of 25.4^2  (oops!)
#        -fixed GUI update issues with SIZING_MAX_SIZE, doesn't automatically recalculate/override the other dimension when you input a new size
#        -fixed error message dialog when Pmw is not available
#        -added error dialog when printing is not successful (at least when sending to driver is unsuccessful)
#
#    0.3 (October 26, 2003)
#        -first release that incorporates a working Preview tab (yay!)
#        -numerous fixes to printerSetup GUI to resolve auto-updating issues
#        -fixes to sizing by resolution option in printerSetup GUI
#
#    0.2 (October 22, 2003)
#        -fixed printerSetup.getSettings() to return (status, message, settings) like in the documentation!
#
#    0.1 (October 17, 2003)
#        -Changed name to ImagePrintWin to follow PIL naming convention (in hopes of Fredrik
#            agreeing to including it in the core library distribution!)
#        -First version of Printer Setup GUI
#        -Major changes to the calling conventions to make it cleaner
#
#    0.0 (October 4, 2003) (released as WinPILprint.py
#        -First test version, basic functionality
#        -GUI for printer setup is NOT yet included


#######################################################################
# Imports
#######################################################################
import copy, os, string
import win32ui
import win32print
#import threading

try:
    from PIL import Image, ImageWin, ImageDraw, ImageTk
except ImportError:
    import Image, ImageWin, ImageDraw, ImageTk

# Try to import tkinter and Pmw to do the setup GUI
CAN_DO_tkinter = True
CAN_DO_PMW = True

try:
    import tkinter
    from tkinter import N,E,S,W,BOTH,YES,X,Y,TOP,BOTTOM,LEFT,RIGHT
    import tkinter.filedialog as tkFileDialog
    
except ImportError:
    CAN_DO_tkinter = False
try:
    import Pmw
except ImportError:
    CAN_DO_PMW = False

# Try to import pyCMS to do ICC Color Management
CAN_DO_ICC = True

try:
    import pyCMS
except ImportError:
    CAN_DO_ICC = False
    
    
#######################################################################
# Constants, you may want to import or copy these into your application
#######################################################################
# ImagePrintWin constants for arguments
UNITS_DEVICE = 0
UNITS_INCH = 1
UNITS_MM = 2
UNITS_CM = 3

ROTATION_NONE = 0        # do not rotate image
ROTATION_90 = 1          # rotate the image 90 degrees before placement
ROTATION_AUTO = 2        # automatically rotate the image to best fit the page, if possible by the sizing requested
ROTATION_PORTRAIT = 3    # automatically rotate the image to portrait orientation before placement ("vertical")
ROTATION_LANDSCAPE = 4   # automatically rotate the image to landscape orientation before placement ("horizontal")

POSITIONING_MANUAL = 0                        # position based on the margins argument, or at the upper-left corner of the printable area if that is not specified
POSITIONING_AUTO_CENTER_ON_PAGE = 1           # automatically center on the full page so top/bottom and left/right margins are equal
POSITIONING_AUTO_CENTER_IN_PRINTABLE_AREA = 2 # automatically center in the printable area, but margins may not be equal depending on printer capabilities

SIZING_NONE = 0                    # size the image based on the "natural" resolution of the image file as specified by imageRes, or default to 72 pixels/inch
SIZING_AUTO_FIT = 1                # automatically size the image as large as possible within the available printable area
SIZING_MAX_SIZE = 2                # fit the image within a bounding box specified by the imageSize argument without cropping or distorting the image.  The resulting image will be equal to or smaller than the size specified.
SIZING_EXACT_SIZE = 3              # center-crop the image (if necessary) to the exact size specified by the imageSize argument.
SIZING_MANUAL_RESOLUTION = 4       # same as SIZING_NONE (functionally, used as an override in the printerSetup GUI only)

# ImagePrintWin constants for printerSetup.getSettings() return status
STATUS_OK = 0            # returned by printerSetup.getSettings() if the user selected "OK" after making selections
STATUS_PRINTED = 1       # returned by printerSetup.getSettings() or printImage() if the user successfully printed the image
STATUS_USER_CANCEL = 2   # returned by printerSetup.getSettings() if the user selected cancel from the printerSetup GUI
STATUS_USER_CLOSE = 3    # returned by printerSetup.getSettings() if the user closed the printerSetup dialog using the "X" in the top right corner
STATUS_ERROR = -1        # returned by printerSetup.getSettings() or printImage() if there was an error during printing
  
# Default settings for some options
DEFAULT_PREVIEW_SIZE = (350,350)  
PREVIEW_PAGECOLOR = (235,235,235)

#---------------------------------------------
# Internal constants, you shouldn't need these
#---------------------------------------------

# Constants for DeviceCaps
HORZSIZE = 4		    #Paper size (mm)
VERTSIZE = 6		    #Paper size (mm)
HORZRES = 8		        #Total device units horiz in printable area
VERTRES = 10		    #Total device units vert in printable area

PHYSICALWIDTH = 110	    #Total device units in page width
PHYSICALHEIGHT = 111	#Total device units in page height
PHYSICALOFFSETX = 112	#Left margin unprintable in device units
PHYSICALOFFSETY = 113	#Top margin unprintable in device units

LOGPIXELSX = 88		    #Device units per inch
LOGPIXELSY = 90		    #Device units per inch

# Constants for pyCMS
INTENT_PERCEPTUAL =             0
INTENT_RELATIVE_COLORIMETRIC =  1
INTENT_SATURATION =             2
INTENT_ABSOLUTE_COLORIMETRIC =  3

#######################################################################
# Common Structures
#######################################################################

# printing settings
def getDefaultPrintingSettings():
    return {
    "printerName":                 None,
    "documentName":                None,
    "imageRes":                    None,    #[x, y]
    "imageSize":                   None,    #[x, y]
    "rotationType":                None,            
    "sizingType":                  None,
    "positioningType":             None,
    "units":                       UNITS_INCH,
    "displayUnits":                None,
    "copies":                      1,
    "margins":                     None,    #[left, top]
    "marginsFromPrintableArea":    False,
    "applyColorManagement":        False,
    "ICCInputProfileRGB":          None,
    "ICCInputProfileCMYK":         None,
    "ICCOutputProfile":            None,
    "ICCRenderingIntent":          INTENT_PERCEPTUAL,
    "ICCCurrentLUT":               None
    }

#######################################################################
# functions
#######################################################################   
def findPrinterNames():
    """ [printernames] = findPrinterNames()
    Returns a list of printer names available on this computer, as strings."""
    
    printers = []
    try:
        printerList = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    except:
        return printers
    
    for p in printerList:
        name = p[2]
        printers.append(name)       
        
    return printers

def getPrinterCaps(printerName = None):
    """{printerCapabilities} = getPrinterCaps("printerName")
    
    printerName = string containing the name of the printer you want to query, as returned
        by findPrinterNames()
        
    {printerCapabilities} is a dictionary of the printer capabilities and their values (see
        documentation in the ImagePrintWin module for details)"""
    
    try:
        hDC = win32ui.CreateDC ()
        if printerName != None:
            hDC.CreatePrinterDC (printerName)        
        else:
            # use the default printer
            hDC.CreatePrinterDC ()
        
        
        printerCaps = {
            "HORZSIZE"           :hDC.GetDeviceCaps (HORZSIZE),		
            "VERTSIZE"           :hDC.GetDeviceCaps (VERTSIZE),		
            "HORZRES"            :hDC.GetDeviceCaps (HORZRES),
            "VERTRES"            :hDC.GetDeviceCaps (VERTRES),       
            "PHYSICALWIDTH"      :hDC.GetDeviceCaps (PHYSICALWIDTH),
            "PHYSICALHEIGHT"     :hDC.GetDeviceCaps (PHYSICALHEIGHT),
            "PHYSICALOFFSETX"    :hDC.GetDeviceCaps (PHYSICALOFFSETX),
            "PHYSICALOFFSETY"    :hDC.GetDeviceCaps (PHYSICALOFFSETY),
            "LOGPIXELSX"         :hDC.GetDeviceCaps (LOGPIXELSX),
            "LOGPIXELSY"         :hDC.GetDeviceCaps (LOGPIXELSY)
            }
        # add a bunch of convenience items
        printerCaps["res"] = {UNITS_DEVICE: [1, 1],
                              UNITS_INCH: [printerCaps["LOGPIXELSX"], printerCaps["LOGPIXELSY"]],
                              UNITS_MM: [float(printerCaps["LOGPIXELSX"]) / 25.4, float(printerCaps["LOGPIXELSY"]) / 25.4]}

        # printerMargins are listed [left, top, right, bottom] of unprintable area
        printerCaps["printerMargins"] = {UNITS_DEVICE: [printerCaps["PHYSICALOFFSETX"], \
                                                        printerCaps["PHYSICALOFFSETY"], \
                                                        printerCaps["PHYSICALWIDTH"] - printerCaps["HORZRES"] - printerCaps["PHYSICALOFFSETX"], \
                                                        printerCaps["PHYSICALHEIGHT"] - printerCaps["VERTRES"] - printerCaps["PHYSICALOFFSETY"] ],
                                         UNITS_INCH: [float(printerCaps["PHYSICALOFFSETX"]) / printerCaps["LOGPIXELSX"], \
                                                      float(printerCaps["PHYSICALOFFSETY"]) / printerCaps["LOGPIXELSY"], \
                                                      float(printerCaps["PHYSICALWIDTH"] - printerCaps["HORZRES"] - printerCaps["PHYSICALOFFSETX"]) / printerCaps["LOGPIXELSX"], \
                                                      float(printerCaps["PHYSICALHEIGHT"] - printerCaps["VERTRES"] - printerCaps["PHYSICALOFFSETY"]) / printerCaps["LOGPIXELSY"] ],
                                         UNITS_MM: [float(printerCaps["PHYSICALOFFSETX"]) / printerCaps["res"][UNITS_MM][0], \
                                                    float(printerCaps["PHYSICALOFFSETY"]) / printerCaps["res"][UNITS_MM][1], \
                                                    float(printerCaps["PHYSICALWIDTH"] - printerCaps["HORZRES"] - printerCaps["PHYSICALOFFSETX"]) / printerCaps["res"][UNITS_MM][0],\
                                                    float(printerCaps["PHYSICALHEIGHT"] - printerCaps["VERTRES"] - printerCaps["PHYSICALOFFSETY"]) / printerCaps["res"][UNITS_MM][1] ]
                                         }
        printerCaps["printableArea"] = {UNITS_DEVICE: [printerCaps["HORZRES"], \
                                                       printerCaps["VERTRES"]],
                                        UNITS_INCH: [float(printerCaps["HORZRES"]) / float(printerCaps["LOGPIXELSX"]), \
                                                     float(printerCaps["VERTRES"]) / float(printerCaps["LOGPIXELSY"])],\
                                        UNITS_MM: [(float(printerCaps["HORZRES"]) / float(printerCaps["LOGPIXELSX"])) * 25.4, \
                                                   (float(printerCaps["VERTRES"]) / float(printerCaps["LOGPIXELSY"])) * 25.4] \
                                        }
                
        printerCaps["pageSize"] = {UNITS_DEVICE: [printerCaps["PHYSICALWIDTH"], \
                                                  printerCaps["PHYSICALHEIGHT"]], \
                                   UNITS_INCH: [float(printerCaps["PHYSICALWIDTH"]) / float(printerCaps["LOGPIXELSX"]), \
                                                float(printerCaps["PHYSICALHEIGHT"]) / float(printerCaps["LOGPIXELSY"])], \
                                   UNITS_MM: [float(printerCaps["PHYSICALWIDTH"]) / float(printerCaps["LOGPIXELSX"] / 25.4), \
                                              float(printerCaps["PHYSICALHEIGHT"]) / float(printerCaps["LOGPIXELSY"] / 25.4)] \
                                   }            
        return printerCaps
    except IOError:
        return {}
    
def convertToCommonUnits(settings, printerCaps = None):
    # printerCaps are needed for converting to UNITS_DEVICE
    if printerCaps == None:
        printerCaps = getPrinterCaps(settings["printerName"])
        
    if printerCaps == {}:
        # no printers available!
        raise Exception #, "Cannot print or do printer setup, no printers available."
        return settings
    
    # figure out what the units are
    if ("units" in settings.keys()) and (settings["units"] != None):
        units = settings["units"]
        
        # These convenience functions shouldn't really be here... but we'll be nice for now
        if type(units) == type("string"):
            if string.lower(units) in ["in", "inch", "inches"]:
                units = UNITS_INCH
            elif string.lower(units) in ["mm", "milimeter", "milimeters"]:
                units = UNITS_MM
            elif string.lower(units) in ["cm", "centimeter", "centimeters"]:
                units = UNITS_CM
            else:
                units = UNITS_DEVICE
                
        displayUnits = units
    else:
        units = UNITS_DEVICE
        displayUnits = UNITS_INCH    # to default to inches... sorry!
    
    # preserve the old unit type for display purposes
    if settings["displayUnits"] == None:
        settings["displayUnits"] = units
       
    # convert imageRes to pixels/inch
    if settings["imageRes"] != None:
        if units == UNITS_DEVICE:
            settings["imageRes"] = [settings["imageRes"][0] * printerCaps["res"][UNITS_DEVICE][0], settings["imageRes"][1] * printerCaps["res"][UNITS_DEVICE][1]]
        elif units == UNITS_INCH:
            pass
        elif units == UNITS_MM:
            settings["imageRes"] = [settings["imageRes"][0] * 25.4, settings["imageRes"][1] * 25.4]

    # convert everything else to UNITS_DEVICE
    res = [float(printerCaps["res"][units][0]), float(printerCaps["res"][units][1])]

    if settings["imageSize"] != None:
        settings["imageSize"] = [settings["imageSize"][0] * res[0], settings["imageSize"][1] * res[1]]
        
    if settings["margins"] != None:
        settings["margins"] = [settings["margins"][0] * res[0], settings["margins"][1] * res[1]]
    
    # convert the units type to UNITS_DEVICE so we don't double-convert
    settings["units"] = UNITS_DEVICE
    
    return settings

def findImageSizeAndMargins(imSize, pSettings):
    """ findImageSizeAndMargins(imSize, settings)
    
    returns [xMargin, yMargin], [outputSize], needsRotation
    
    xMargin = device units
    yMargin = device units
    needsRotation = bool
    [outputSize] = tuple of [deviceUnitsX,deviceUnitsY]
    """
    # convert the settings to common units
    pSettings = convertToCommonUnits(pSettings)
    
    needsRotation = False
    
    # get the printer capabilities
    printerCaps = getPrinterCaps(pSettings["printerName"])
    if printerCaps == {}:
        return [-1, "Could not get printerCaps (printer capabilities), check printer name (%s) or ensure existance of a Default Printer" %pSettings["printerName"]], [pSettings, None], None

    # if requested, set up the printer margins for the start of the printable area
    #     instead of being absolute from the page edge
    if pSettings["marginsFromPrintableArea"]:
        extraLeftMargin = printerCaps["printerMargins"][UNITS_DEVICE][0]
        extraTopMargin = printerCaps["printerMargins"][UNITS_DEVICE][1]
    else:
        extraLeftMargin = 0
        extraTopMargin = 0

    # find the rotation type
    #     but we can't handle autorotation yet... do it later with sizing and margins
    if pSettings["rotationType"] == ROTATION_90:
        imSize = (imSize[1], imSize[0])
        needsRotation = True
    elif pSettings["rotationType"] == ROTATION_PORTRAIT:
        if imSize[0] > imSize[1]:
            needsRotation = True
            imSize = (imSize[1], imSize[0])
    elif pSettings["rotationType"] == ROTATION_LANDSCAPE:
        if imSize[0] < imSize[1]:
            needsRotation = True
            imSize = (imSize[1], imSize[0])

    # fix None margins
    if pSettings["margins"] == None:
        pSettings["margins"] = [printerCaps["printerMargins"][UNITS_DEVICE][0], printerCaps["printerMargins"][UNITS_DEVICE][1]]
        
    # find the area within we are positioning
    if pSettings["positioningType"] == POSITIONING_MANUAL or (pSettings["positioningType"] == None and pSettings["margins"] != None):
        areaX = printerCaps["printableArea"][UNITS_DEVICE][0] - (pSettings["margins"][0] - printerCaps["printerMargins"][UNITS_DEVICE][0] + extraLeftMargin)
        areaY = printerCaps["printableArea"][UNITS_DEVICE][1] - (pSettings["margins"][1] - printerCaps["printerMargins"][UNITS_DEVICE][1] + extraTopMargin)
        
    elif pSettings["positioningType"] == POSITIONING_AUTO_CENTER_ON_PAGE:
        # we have to handle auto-sizing with auto-centering on page separately
        if pSettings["sizingType"] == SIZING_AUTO_FIT:
            maxXMargin = max(printerCaps["printerMargins"][UNITS_DEVICE][0], printerCaps["printerMargins"][UNITS_DEVICE][2])
            maxYMargin = max(printerCaps["printerMargins"][UNITS_DEVICE][1], printerCaps["printerMargins"][UNITS_DEVICE][3])
            areaX = printerCaps["pageSize"][UNITS_DEVICE][0] - (2 * maxXMargin)
            areaY = printerCaps["pageSize"][UNITS_DEVICE][1] - (2 * maxYMargin)
        else:
            areaX = printerCaps["pageSize"][UNITS_DEVICE][0]
            areaY = printerCaps["pageSize"][UNITS_DEVICE][1]
            
    elif pSettings["positioningType"] == POSITIONING_AUTO_CENTER_IN_PRINTABLE_AREA:
        areaX = printerCaps["printableArea"][UNITS_DEVICE][0]
        areaY = printerCaps["printableArea"][UNITS_DEVICE][1]
        
    else:    # no positioning type specified, or an invalid one
        areaX = printerCaps["printableArea"][UNITS_DEVICE][0]
        areaY = printerCaps["printableArea"][UNITS_DEVICE][1]

    # figure out the sizing
    if pSettings["sizingType"] in [SIZING_NONE, None, SIZING_MANUAL_RESOLUTION]:
        if pSettings["imageRes"] != None:
            # res is in pixels per inch by default
            outputSizeX = int(((imSize[0] * printerCaps["res"][UNITS_INCH][0]) / pSettings["imageRes"][0])+ 0.5)
            outputSizeY = int(((imSize[1] * printerCaps["res"][UNITS_INCH][1]) / pSettings["imageRes"][1])+ 0.5)
        else:    # default to 72dpi and they can live with it, sorry!
            outputSizeX = int(((imSize[0] * printerCaps["res"][UNITS_INCH][0]) / 72.0)+ 0.5)
            outputSizeY = int(((imSize[1] * printerCaps["res"][UNITS_INCH][1]) / 72.0)+ 0.5)
            
    elif pSettings["sizingType"] == SIZING_EXACT_SIZE:
        outputSizeX = pSettings["imageSize"][0]
        outputSizeY = pSettings["imageSize"][1]
        
    elif pSettings["sizingType"] == SIZING_MAX_SIZE:
        # calculate how to fit the image within this bounding box
        #    while maintaining the aspect ratio
        aspectIm = float(imSize[0])/float(imSize[1])
        aspectOut = float(pSettings["imageSize"][0])/float(pSettings["imageSize"][1])
        if aspectIm >= aspectOut:
            # keep imageSizeX, adjust imageSizeY
            outputSizeX = pSettings["imageSize"][0]
            outputSizeY = int(float(pSettings["imageSize"][0]) / aspectIm + 0.5)
        else:    # aspectIm < aspectOut:
            # keep imageSizeY, adjust imageSizeX
            outputSizeX = int(float(pSettings["imageSize"][1]) * aspectIm + 0.5)
            outputSizeY = pSettings["imageSize"][1]
                    
    else:    #SIZING_AUTO_FIT
        if pSettings["rotationType"] == ROTATION_AUTO:
            
            if pSettings["positioningType"] == POSITIONING_AUTO_CENTER_ON_PAGE:
                # auto center on page and auto sizing have to work together so the image doesn't go out of the printable area
                maxXMargin = max(printerCaps["printerMargins"][UNITS_DEVICE][0], printerCaps["printerMargins"][UNITS_DEVICE][2])
                maxYMargin = max(printerCaps["printerMargins"][UNITS_DEVICE][1], printerCaps["printerMargins"][UNITS_DEVICE][3])
                areaX = printerCaps["pageSize"][UNITS_DEVICE][0] - (2 * maxXMargin)
                areaY = printerCaps["pageSize"][UNITS_DEVICE][1] - (2 * maxYMargin)         
            
            # match the aspect ratios of image size and printable area as best as possible
            aspectIm = float(imSize[0])/float(imSize[1])
            aspectPage = float(areaX) / float(areaY)
            
            if (aspectIm > 1.0 and aspectPage < 1.0) or (aspectIm < 1.0 and aspectPage > 1.0):
                # they're a mismatch, rotate them
                needsRotation = True
                imSize = (imSize[1], imSize[0])
            else:
                # they match, or one of them is square, so don't rotate.
                pass
        # size to fit the printable area!
        # calculate how to fit the image within this bounding box
        #    while maintaining the aspect ratio
        aspectIm = float(imSize[0])/float(imSize[1])
        aspectPage = float(areaX)/float(areaY)
        if aspectIm >= aspectPage:
            # fit to page width
            outputSizeX = areaX
            outputSizeY = int(float(areaX) / aspectIm + 0.5)
        else:    # aspectIm < aspectOut:
            # fit to page height
            outputSizeX = int(float(areaY) * aspectIm + 0.5)
            outputSizeY = areaY
            
    # if not SIZING_AUTO_FIT, but ROTATION_AUTO is still set, see if we need to rotate the image to fit the printable area
    if (pSettings["sizingType"] != SIZING_AUTO_FIT) and (pSettings["rotationType"] == ROTATION_AUTO):
        if (outputSizeX > areaX) or (outputSizeY > areaY):
            if outputSizeX <= areaY and outputSizeY <= areaX:
                needsRotation = True
                temp = outputSizeX
                outputSizeX = outputSizeY
                outputSizeY = outputSizeX
                imSize = (imSize[1], imSize[0])
            
    # figure out the margins
    if pSettings["positioningType"] == POSITIONING_AUTO_CENTER_ON_PAGE:
        xMargin = (printerCaps["pageSize"][UNITS_DEVICE][0] - outputSizeX) / 2
        yMargin = (printerCaps["pageSize"][UNITS_DEVICE][1] - outputSizeY) / 2

    elif pSettings["positioningType"] == POSITIONING_AUTO_CENTER_IN_PRINTABLE_AREA:
        xMargin = ((areaX - outputSizeX) / 2) + printerCaps["printerMargins"][UNITS_DEVICE][0]
        yMargin = ((areaY - outputSizeY) / 2) + printerCaps["printerMargins"][UNITS_DEVICE][1]
    else:    # pSettings["positioningType"] == POSITIONING_MANUAL: #(or none specified)
        if pSettings["margins"] != None:
            xMargin = pSettings["margins"][0] + extraLeftMargin
            yMargin = pSettings["margins"][1] + extraTopMargin
        else:
            xMargin = printerCaps["printerMargins"][UNITS_DEVICE][0]
            yMargin = printerCaps["printerMargins"][UNITS_DEVICE][1]
            pSettings["margins"] = [xMargin, yMargin]
        
    return [xMargin, yMargin], [outputSizeX, outputSizeY], needsRotation 

    
def printImage(im, settings = None, **kw):
    """ (status, message, settings) = printImage(im, settings = None, **kw)
    
    status = 0 on success, -1 on error
    message = string, describing error or success details
    settings = a dictionary of the settings used for this print job.  It can be passed
        back in to printImage for future images if you want to use the same settings each
        time.

    im = either a string pathname to a valid image file, or a PIL image object
    
    **kw = keyword options for print settings you want to use.  See the ImagePrintWin module
        for details on what keywords and values are available."""
    
    pSettings = getDefaultPrintingSettings()
   
    # if a full settings dictionary was passed in, use them to override the default settings above
    if (settings != None) and (type(settings) == type({})):
        for item in settings.keys():
            pSettings[item] = settings[item]
        
    # override using any individual settings passed in
    for item in kw.keys():
        pSettings[item] = kw[item]

    # make sure the image is loaded
    if type(im) == type("string"):
        try:
            if pSettings["documentName"] == None:
                pSettings["documentName"] = im
            im = Image.open(im)
        except Exception:#, reason:
            return (-1, reason, pSettings)
    try:
        im.load()
    except Exception:#, reason:
        return (-1, "Image could not be .load() ed (%s)" %reason, pSettings)
  
    # if imageRes isn't specified in pSettings, see if it's in the image.info dictionary
    if pSettings["imageRes"] == None:
        if "dpi" in dir(im.info):
            pSettings["imageRes"] = im.info["dpi"]
  
    # Convert all the settings to a standard format (device units)
    pSettings = convertToCommonUnits(pSettings)
  
    [xMargin, yMargin], outputSize, needsRotation = findImageSizeAndMargins(im.size, pSettings)
    
    if outputSize[0] <= 0 or outputSize[1] <= 0:
        return (-1, "Image is sized to less than 0 units, can't print using these settings.", pSettings)
    
    if xMargin == -1 and needsRotation is None:
        # findImageSizeAndMargins failed, probably when trying to get printerCaps
        # xMargin, yMargin, and outputSizeX are actually the status, message, and settings for the failure
        return (xMargin, yMargin, outputSize)
        
    if needsRotation:
        im = im.rotate(-90)
            
    # Convert the image to RGB, either through PIL or through ICC profiles (PyCMS)
    if im.mode != "RGB":
        if not(im.mode == "CMYK" and pSettings["applyColorManagement"] and CAN_DO_ICC):
            im = im.convert("RGB")

    if pSettings["applyColorManagement"] and CAN_DO_ICC:
        # see if there's already a good LUT (to save time)
        ICC_LUT = None
        
        if (pSettings["currentProfileLUT"] != None):
            if im.mode == "RGB":
                if (pSettings["ICCCurrentLUT"][0] == pSettings["ICCInputProfileRGB"]) and \
                   (pSettings["ICCCurrentLUT"][2] == pSettings["ICCOutputProfile"]) and \
                   (pSettings["ICCCurrentLUT"][3] == pSettings["ICCRenderingIntent"]):
                    ICC_LUT = pSettings["ICCCurrentLUT"][4]
            elif im.mode == "CMYK":
                if (pSettings["ICCCurrentLUT"][0] == pSettings["ICCInputProfileCMYK"]) and \
                   (pSettings["ICCCurrentLUT"][2] == pSettings["ICCOutputProfile"]) and \
                   (pSettings["ICCCurrentLUT"][3] == pSettings["ICCRenderingIntent"]):
                    ICC_LUT = pSettings["ICCCurrentLUT"][4]
            else:
                # shouldn't ever get here
                return (-1, "Programatic error in ICC routines (existing LUT)!  Please report to kevin@cazabon.com!", pSettings)
            
        # no good LUT already, build one from the profiles
        if ICC_LUT == None:
            if im.mode == "RGB":
                try:
                    ICC_LUT = pyCMS.buildTransform(pSettings["ICCInputProfileRGB"], pSettings["ICCOutputProfile"], "RGB", "RGB", pSettings["ICCRenderingIntent"])
                    pSettings["ICCCurrentLUT"] = [pSettings["ICCinputProfileRGB"], "RGB", pSettings["ICCoutputProfile"], pSettings["ICCRenderingIntent"], ICC_LUT]
                except Exception:#, reason:
                    return (-1, "Color management failed to create LUT (%s)" %reason, pSettings)
            elif im.mode == "CMYK":
                try:
                    ICC_LUT = pyCMS.buildTransform(pSettings["ICCinputProfileCMYK"], pSettings["ICCoutputProfile"], "CMYK", "RGB", pSettings["ICCrenderingIntent"])
                    pSettings["ICCCurrentLUT"] = [pSettings["ICCinputProfileCMYK"], "CMYK", pSettings["ICCoutputProfile"], pSettings["ICCRenderingIntent"], ICC_LUT]
                except Exception:#, reason:
                    return (-1, "Color management failed to create LUT (%s)" %reason, pSettings)
            else:
                # shouldn't ever get here
                return (-1, "Programatic error in ICC routines (New LUT)!  Please report to kevin@cazabon.com!", pSettings)
            
        # apply the transform
        try:
            im = pyCMS.applyTransform(im, ICC_LUT)
        except Exception:#, reason:
            return (-1, "Color management failed during application (%s)" %reason, pSettings)

    # if the image is too big, resize it using PIL... Windows drivers don't resize down well
    # use 1 pixel per printer unit for now (even though printer units are usually dots, not pixels)... seems to work well enough
    if im.size[0] > outputSize[0]:
        im = maxSize(im, outputSize, Image.BICUBIC)

    # Connect to the printer
    try:
        hDC = win32ui.CreateDC ()
        
        if pSettings["printerName"] != None:
            if pSettings["printerName"] not in findPrinterNames():
                try:
                    hDC.CreatePrinterDC(pSettings["printerName"])
                except Exception:#, reason:
                    return (-1, "Printer named \"%s\" does not exist (%s)." %(pSettings["printerName"], reason), pSettings)
            else:
                hDC.CreatePrinterDC(pSettings["printerName"])
        else:
            # use the default printer
            hDC.CreatePrinterDC()
            
    except Exception:#, reason:
        #print "Could not connect to printer (%s)" %reason
        return (-1, "Could not connect to printer (%s)" %reason, pSettings)
        
    # Create the printer document and send the page
    try:
        printerCaps = getPrinterCaps(pSettings["printerName"])
        lpm, tpm, rpm, bpm = printerCaps["printerMargins"][UNITS_DEVICE]
        
        if pSettings["documentName"] == None:
            pSettings["documentName"] = "Python ImagePrintWin image file"
            
        for i in range (pSettings["copies"]):
            hDC.StartDoc (pSettings["documentName"])
            hDC.StartPage ()
            
            dib = ImageWin.Dib (im)
            dib.draw (hDC.GetHandleOutput (), [int(xMargin - lpm), int(yMargin - tpm), int(outputSize[0] + xMargin - lpm), int(outputSize[1] + yMargin - tpm)])
            hDC.EndPage ()
            hDC.EndDoc ()
        
    except Exception:#, reason:
        return (-1, "Could not print document (%s)" %reason, pSettings)

    return (STATUS_PRINTED, "Printing Successful", pSettings)

def maxSize(image, maxSize, method = 3):
    """ im = maxSize(im, (maxSizeX, maxSizeY), method = Image.BICUBIC)
    
    Resizes a PIL image to a maximum size specified while maintaining
    the aspect ratio of the image.  Similar to Image.thumbnail(), but allows
    usage of different resizing methods and does NOT modify the image in place."""
    
    imAspect = float(image.size[0])/float(image.size[1])
    outAspect = float(maxSize[0])/float(maxSize[1])

    if imAspect >= outAspect:
        #set to maxWidth x maxWidth/imAspect
        return image.resize((maxSize[0], int((float(maxSize[0])/imAspect) + 0.5)), method)
    else:
        #set to maxHeight*imAspect x maxHeight
        return image.resize((int((float(maxSize[1])*imAspect) + 0.5), maxSize[1]), method)

def fit(inputImage, outputSize, method=3, bleed=0.0, centering= None):
    """ 
        This method returns a sized and cropped version of the image, cropped to the aspect ratio and
        size that you request.  It can be customized to your needs with "method", "bleed", and "centering"
        as required.
    
        inputImage = an PIL Image object, could easily be changed to "self" to make this a method of an Image object.
        outputSize = (width, height) in pixels of image to return
        method = resizing method:  0=(replication), 2=(bi-linear), 3=(bi-cubic)
        bleed = decimal percentage (0-0.49999) of width/height to crop off as a minumum around the outside of the image
                    This allows you to remove a default amount of the image around the outside, for
                    'cleaning up' scans that may have edges of negs showing, or whatever.
                    This percentage is removed from EACH side, not a total amount.
        centering = [left, top], percentages to crop of each side to fit the aspect ratio you require.
                    This function allows you to customize where the crop occurs, whether it is a 
                    'center crop' or a 'top crop', or whatever. Default is center-cropped.
                    [0.5, 0.5] is center cropping (i.e. if cropping the width, take 50% off of the left side (and therefore 50% off the right side), and same with Top/Bottom)
                    [0.0, 0.0] will crop from the top left corner (i.e. if cropping the width, take all of the crop off of the right side, and if cropping the height, take all of it off the bottom)
                    [1.0, 0.0] will crop from the bottom left corner, etc. (i.e. if cropping the width, take all of the crop off the left side, and if cropping the height take none from the Top (and therefore all off the bottom)) 
                    
                    by Kevin Cazabon, Feb 17/2000
                    kevin@cazabon.com 
                    http://www.cazabon.com """
    
    if centering == None:
        centering = [0.50,0.50]
        
    # ensure inputs are valid
    if type(centering) != type([]):
        centering = [centering[0], centering[1]]

    if centering[0] > 1.0 or centering[0] < 0.0:
        centering [0] = 0.50
    if centering[1] > 1.0 or centering[1] < 0.0:
        centering[1] = 0.50
        
    if bleed > 0.49999 or bleed < 0.0:
        bleed = 0.0
        
    if method not in [0, 2, 3]:
        method = 0

    # calculate the area to use for resizing and cropping, subtracting the 'bleed' around the edges           
    bleedPixels = (int((float(bleed) * float(inputImage.size[0])) + 0.5), int((float(bleed) * float(inputImage.size[1])) + 0.5)) # number of pixels to trim off on Top and Bottom, Left and Right
    liveArea = (bleedPixels[0], bleedPixels[1], inputImage.size[0] - bleedPixels[0] - 1, inputImage.size[1] - bleedPixels[1] - 1)
    liveSize = (liveArea[2] - liveArea[0], liveArea[3] - liveArea[1])
    
    # calculate the aspect ratio of the liveArea
    liveAreaAspectRatio = float(liveSize[0])/float(liveSize[1])
    
    # calculate the aspect ratio of the output image
    aspectRatio = float(outputSize[0])/float(outputSize[1])
    
    # figure out if the sides or top/bottom will be cropped off
    if liveAreaAspectRatio >= aspectRatio:
        # liveArea is wider than what's needed, crop the sides
        cropWidth = int((aspectRatio * float(liveSize[1])) + 0.5)
        cropHeight = liveSize[1]
        
    else:
        #liveArea is taller than what's needed, crop the top and bottom
        cropWidth = liveSize[0]
        cropHeight = int((float(liveSize[0])/aspectRatio) + 0.5)
        
    # make the crop    
    leftSide = int(liveArea[0] + (float(liveSize[0] - cropWidth) * centering[0]))
    if leftSide < 0:
        leftSide = 0
    topSide = int(liveArea[1] + (float(liveSize[1] - cropHeight) * centering[1]))
    if topSide < 0:
        topSide = 0
    
    
    outputImage = inputImage.crop((leftSide, topSide, leftSide + cropWidth, topSide + cropHeight))
    
    # resize the image and return it    
    return outputImage.resize(outputSize, method)



def validateFloat(arg):
    try:
        float(arg)
        return Pmw.OK
    except ValueError:
        for i in range(len(arg)):
            if arg[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                pass
            elif arg[i] in ["."]:
                if len(arg) == 1:
                    return Pmw.PARTIAL
                if string.count(arg, ".") > 1:
                    return Pmw.ERROR
            elif arg[i] in ["+", "-"]:
                if i == 0:
                    if len(arg) == 1:
                        return Pmw.PARTIAL
                else:
                    return Pmw.ERROR
            else:
                return Pmw.ERROR
        return Pmw.OK
    
#######################################################################
# Printer Setup GUI Class
#######################################################################
def browseForImageFile(initialdir = None, initialfile = None):
    f = tkFileDialog.askopenfilename(filetypes = [("Image Files", ("*.tif", "*.jpg", "*.tga", "*.bmp", "*.gif", "*.png"))], title = "Select Image File", initialdir = initialdir, initialfile = initialfile)

    if os.path.isfile(f):
        return f
    else:
        return None
    
class spawnPrintJob:
    """ This is used to spawn printing off on another thread.  When an error occurs in printing, a try/except
    doesn't always catch it, so the only way to "save" the program is to have it occur in a thread.
    Unfortunately this means we can't show an error dialog if something catchable goes wrong.  FIXME in the
    long term if you can. """
    
    def __init__(self, im, settings = None):
        status, message, settings = printImage(im, settings)
    
class previewPageClass:
    def __init__(self, parent, im = None, previewSize = None):
        self.im = im
        self.loadIm()
        if previewSize == None:
            previewSize = DEFAULT_PREVIEW_SIZE
        self.previewSize = previewSize
        
        # draw the main frame for the GUI, don't pack it, let the calling app do it, so you can be flexible
        self.frame = tkinter.Frame(parent)
        
        self.main = tkinter.Frame(self.frame, relief = tkinter.SUNKEN, bd = 2)
        self.main.pack(side = TOP, expand = YES, fill = BOTH)


        self.previewPage = tkinter.Label(self.main, text = "No image to preview yet")
        self.previewPage.grid(row = 0, column = 0, padx = 2, pady = 2)
            
    def loadIm(self):
        if type(self.im) == type("string"):
            try:
                self.im = Image.open(self.im)
            except:
                self.im = None
                
    def update(self, settings, printerCaps):
        # redraw the preview using the printerCaps and settings provided
        self.printerCaps = printerCaps
        
        self.settings = getDefaultPrintingSettings()
       
        # if a full settings dictionary was passed in, use them to override the default settings above
        if (settings != None) and (type(settings) == type({})):
            for item in settings.keys():
                self.settings[item] = settings[item]

        self.settings = convertToCommonUnits(self.settings, self.printerCaps)
        
        # if imageRes isn't specified in settings, see if it's in the im.info dictionary
        if self.settings["imageRes"] == None:
            if "dpi" in dir(self.im.info):
                self.settings["imageRes"] = self.im.info["dpi"]

        [xMargin, yMargin], outputSize, needsRotation = findImageSizeAndMargins(self.im.size, self.settings)

        if outputSize[0] <= 0 or outputSize[1] <= 0:
            return (-1, "Image is sized to less than 0 units, can't print using these settings.", self.settings)
        
        if xMargin == -1 and needRotation is None:
            # findImageSizeAndMargins failed, probably when trying to get printerCaps
            # xMargin, yMargin, and outputSizeX are actually the status, message, and settings for the failure
            return (xMargin, yMargin, outputSizeX)
            
        if needsRotation:
            im = self.im.rotate(-90)
        else:
            im = self.im
            
        # Convert the image to RGB, either through PIL or through ICC profiles (PyCMS)
        if im.mode != "RGB":
            im = im.convert("RGB")

        # figure out the page size
        maxPageSize = self.previewSize
        maxPageAspect = float(maxPageSize[0]) / float(maxPageSize[1])
        pageAspect = float(self.printerCaps["pageSize"][UNITS_DEVICE][0]) / float(self.printerCaps["pageSize"][UNITS_DEVICE][1])
        
        if maxPageAspect > pageAspect:
            # use maxPageSize[1] * pageAspect,  maxPageSize[1]
            pageSize = [int(maxPageSize[1] * pageAspect + 0.5), maxPageSize[1]]
        else:
            pageSize = [maxPageSize[0], int(maxPageSize[0] / pageAspect + 0.5)]

        # figure out the margins in pixels
        pageScale = float(pageSize[0]) / float(self.printerCaps["pageSize"][UNITS_DEVICE][0])
        leftPrinterMargin = int(pageScale * self.printerCaps["printerMargins"][UNITS_DEVICE][0] + 0.5)
        topPrinterMargin = int(pageScale * self.printerCaps["printerMargins"][UNITS_DEVICE][1] + 0.5)
        rightPrinterMargin = int(pageScale * self.printerCaps["printerMargins"][UNITS_DEVICE][2] + 0.5)
        bottomPrinterMargin = int(pageScale * self.printerCaps["printerMargins"][UNITS_DEVICE][3] + 0.5)
    
        # figure out the printable area
        printableArea = [pageSize[0] - leftPrinterMargin - rightPrinterMargin, pageSize[1] - topPrinterMargin - bottomPrinterMargin]
        
        # create the preview background, and a mask file the same size
        self.preview = Image.new("RGB", pageSize, (255,255,255))
            
        # size and crop self.im
        im = fit(im, (int(outputSize[0] * pageScale + 0.5), int(outputSize[1] * pageScale + 0.5)))
        
        # paste self.im
        self.preview.paste(im, (int(xMargin * pageScale + 0.5), int(yMargin * pageScale + 0.5)))    #, mask)
        
        # overlay the printer margins
        mask = Image.new("1", pageSize, 1)
        # draw the printable area on it
        draw = ImageDraw.Draw(mask)
        draw.rectangle((leftPrinterMargin, topPrinterMargin, leftPrinterMargin + printableArea[0], topPrinterMargin + printableArea[1]), fill=0)
        del draw 
        
        marginColor = Image.new("RGB", pageSize, PREVIEW_PAGECOLOR)
        
        # paste the printable area using the mask
        self.preview.paste(marginColor, (0,0), mask)        
        
        # convert self.preview to a tkinter.PhotoImage and show it
        self.preview = ImageTk.PhotoImage(self.preview)
        
        try:
            self.previewPage.grid_forget()
        except:
            pass
        
        self.previewPage = tkinter.Label(self.main, image = self.preview, relief = tkinter.RAISED, bd = 2)
        self.previewPage.grid(row = 0, column = 0, padx = 2, pady = 2)
        self.main.update_idletasks()        
    
        return (0, "Preview Successful", settings)        
          
    def replaceImage(self, im):
        self.im = im
        self.loadIm()
            
    def pack(self, **kw):
        self.frame.pack(**kw)
    
    def grid(self, **kw):
        self.frame.grid(**kw)
        
class printerSetup:
    def __init__(self, parent, im = None, allowPrinting = True, closeAfterPrint = True, hideICC = False, settings = None, **kw):
        self.parent = parent        
        self.im = im
        self.allowPrinting = allowPrinting
        self.closeAfterPrint = closeAfterPrint
        self.hideICC = hideICC
        self.GUI_OK = False

        # Start with a default settings dictionary
        self.pSettings = getDefaultPrintingSettings()
        
        if self.pSettings["printerName"] == None:
            # find the default printer name
            self.pSettings["printerName"] = win32print.GetDefaultPrinter()
            
        # if a full settings dictionary was passed in, use them to override the default settings above
        if (settings != None) and (type(settings) == type({})):
            for item in settings.keys():
                self.pSettings[item] = settings[item]
            
        # override using any individual settings passed in through **kw
        for item in kw.keys():
            self.pSettings[item] = kw[item]
                
        # backup the "untouched" settings
        self.backupSettings = copy.copy(self.pSettings)
                
        # make sure the image is loaded
        if self.im != None and type(self.im) == type("string"):
            try:
                self.im = Image.open(self.im)
            except Exception:#, reason:
                self.im = None
                #FIXME: find some better way to handle a bad image passed to this GUI

        # make sure we have a usable image resolution, take it from the file if it's not passed in
        if self.pSettings["imageRes"] == None:
            if self.im != None:
                # if imageRes isn't specified in pSettings, see if it's in the image.info dictionary
                if "dpi" in dir(self.im.info):
                    self.pSettings["imageRes"] = self.im.info["dpi"]
                else:
                    self.pSettings["imageRes"] = (72, 72)
            else:
                # default to 72 dpi
                self.pSettings["imageRes"] = (72, 72)
                
        # backup the original res so we can reset it later
        self.pSettings["origImRes"] = self.pSettings["imageRes"]
        
        # create the main window for the GUI, if tkinter is available.
        if not CAN_DO_tkinter:
            #print "Cannot create ImagePrintWin.printerSetup() dialog, tkinter is not installed on this system."
            pass
        
        else: # at least we can do a tkinter GUI, even if just for an error message...
            try:
                self.main = tkinter.Toplevel(parent)
                self.main.withdraw()
                self.main.title("Printer Setup")
            except Exception:#, reason:
                #print "ImagePrintWin.printerSetup() failed, error while creating self.main:  %s" %reason
                while 1:
                    pass
    
            # Set the self.main.protocol() for window closure so we can clean up nicely
            self.main.protocol("WM_DELETE_WINDOW", lambda x = None, self = self: self.die("Close"))
    
            # Check to see if we can use Pmw, if not display an error in the new GUI.
            if not CAN_DO_PMW:
                tkinter.Label(self.main, text = "Cannot create ImagePrintWin.printerSetup() dialog because\nPmw (Python Megawidgets) is not available on this system.\n\nPlease see http://pmw.sourceforge.net/ for details on Pmw.").pack(padx = 20, pady = 20)
                self.main.deiconify()
            
            else:
                # create the main GUI!
                self.makeGUI()

    def getPrinterCaps(self):
        try:
            self.printerCaps = getPrinterCaps(self.pSettings["printerName"])
        except Exception:#, reason:
            # no printers available, or error while getting settings
            self.printerCaps = {}
            #FIXME: how should we handle this?

    def makeGUI(self):
        # make sure we have the printerCaps, if available
        self.getPrinterCaps()
        
        self.pSettings = convertToCommonUnits(self.pSettings)

        self.updateInProgress = False

        #------------------------------
        # Create and pack the NoteBook.
        #------------------------------
        self.notebook = Pmw.NoteBook(self.main, raisecommand = self.changePages)
        self.notebook.pack(fill = BOTH, expand = YES, padx = 10, pady = 10)

        #----------------------------------------
        # Add the "Printer" page to the notebook.
        #----------------------------------------
        self.printerPage = self.notebook.add('Printer')
        self.notebook.tab('Printer').focus_set()

        # Set up the Select Printer Group
        self.selectPrinterGroup = Pmw.Group(self.printerPage, tag_text = 'Select Printer')
        self.selectPrinterGroup.pack(expand = YES, fill = BOTH, padx = 5, pady = 5)
        
        self.selectedPrinterVar = tkinter.StringVar()
        self.selectedPrinterVar.set(self.pSettings["printerName"])
        self.printerSelectionMenu = Pmw.OptionMenu(self.selectPrinterGroup.interior(),
                labelpos = 'w',
                label_text = 'Select Printer:',
                label_width = 15,
                menubutton_textvariable = self.selectedPrinterVar,
                items = [self.pSettings["printerName"]],
                menubutton_width = 40,
                command = self.changePrinter
        )
        self.printerSelectionMenu.grid(padx = 5, pady = 5, sticky = E)
        
        # Set up the Printer Info Group
        self.printerInfoGroup = Pmw.Group(self.printerPage, tag_text = 'Printer Info')
        self.printerInfoGroup.pack(expand = YES, fill = BOTH, padx = 5, pady = 5)

        tkinter.Label(self.printerInfoGroup.interior(), text = "Resolution:").grid(row = 0, column = 0, sticky = W)
        self.dpiLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.dpiLabel.grid(row = 0, column = 1, sticky = W, padx = 5)
        self.dpmmLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.dpmmLabel.grid(row = 0, column = 2, sticky = W, padx = 5)

        tkinter.Label(self.printerInfoGroup.interior(), text = "Page Size:").grid(row = 1, column = 0, sticky = W)
        self.pageSizeInchesLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.pageSizeInchesLabel.grid(row = 1, column = 1, sticky = W, padx = 5)
        self.pageSizeMMLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.pageSizeMMLabel.grid(row = 1, column = 2, sticky = W, padx = 5)

        tkinter.Label(self.printerInfoGroup.interior(), text = "Printable Area:").grid(row = 2, column = 0, sticky = W)
        self.printableWidthInchesLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.printableWidthInchesLabel.grid(row = 2, column = 1, sticky = W, padx = 5)
        self.printableWidthMMLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.printableWidthMMLabel.grid(row = 2, column = 2, sticky = W, padx = 5)

        tkinter.Label(self.printerInfoGroup.interior(), text = "Left Printer Margin:").grid(row = 3, column = 0, sticky = W)
        self.leftPrinterMarginInchesLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.leftPrinterMarginInchesLabel.grid(row = 3, column = 1, sticky = W, padx = 5)
        self.leftPrinterMarginMMLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.leftPrinterMarginMMLabel.grid(row = 3, column = 2, sticky = W, padx = 5)
        
        tkinter.Label(self.printerInfoGroup.interior(), text = "Right Printer Margin:").grid(row = 4, column = 0, sticky = W)
        self.rightPrinterMarginInchesLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.rightPrinterMarginInchesLabel.grid(row = 4, column = 1, sticky = W, padx = 5)
        self.rightPrinterMarginMMLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.rightPrinterMarginMMLabel.grid(row = 4, column = 2, sticky = W, padx = 5)
        
        tkinter.Label(self.printerInfoGroup.interior(), text = "Top Printer Margin:").grid(row = 5, column = 0, sticky = W)
        self.topPrinterMarginInchesLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.topPrinterMarginInchesLabel.grid(row = 5, column = 1, sticky = W, padx = 5)
        self.topPrinterMarginMMLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.topPrinterMarginMMLabel.grid(row = 5, column = 2, sticky = W, padx = 5)
        
        tkinter.Label(self.printerInfoGroup.interior(), text = "Bottom Printer Margin:").grid(row = 6, column = 0, sticky = W)
        self.bottomPrinterMarginInchesLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.bottomPrinterMarginInchesLabel.grid(row = 6, column = 1, sticky = W, padx = 5)
        self.bottomPrinterMarginMMLabel = tkinter.Label(self.printerInfoGroup.interior(), text = "")
        self.bottomPrinterMarginMMLabel.grid(row = 6, column = 2, sticky = W, padx = 5)

        # Set up the "Units" group
        self.unitsGroup = Pmw.Group(self.printerPage, tag_text = 'Sizing Units')
        self.unitsGroup.pack(expand = YES, fill = X, side = TOP, padx = 5, pady = 5)

        self.unitsVar = tkinter.StringVar()
        self.unitsVar.set("Inches")
        self.unitsSelectionMenu = Pmw.OptionMenu(self.unitsGroup.interior(),
                labelpos = 'w',
                label_text = 'Units to use for margins and sizing:',
                menubutton_textvariable = self.unitsVar,
                items = ["Inches", "mm", "Device units"],
                menubutton_width = 20,
                command = self.changeUnits
        )
        self.unitsSelectionMenu.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = E)

        # Set up the Copies group
        self.copyGroup = Pmw.Group(self.printerPage, tag_text = 'Copies')
        self.copyGroup.pack(expand = YES, fill = BOTH, padx = 5, pady = 5)
        
        self.copyCountEntry = Pmw.EntryField(self.copyGroup.interior(),
                labelpos = 'w',
                value = 1,
                label_text = 'Number of copies:',
                label_width = 15,
                validate = {'validator' : 'integer', 'min' : 1, 'max' : 999, 'minstrict' : 0},
                modifiedcommand = self.changeCopies)
        self.copyCountEntry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W)

        #----------------------
        # Add the "Layout" tab.
        #----------------------
        self.layoutPage = self.notebook.add('Layout')

        # Set up the Rotation Group
        self.rotationGroup = Pmw.Group(self.layoutPage, tag_text = 'Rotation')
        self.rotationGroup.pack(expand = YES, fill = X, side = TOP, padx = 5, pady = 5)
        
        self.rotationVar = tkinter.StringVar()
        self.rotationVar.set("None")
        self.rotationSelectionMenu = Pmw.OptionMenu(self.rotationGroup.interior(),
                labelpos = 'w',
                label_text = 'Rotation:',
                label_width = 15,
                menubutton_textvariable = self.rotationVar,
                items = ["None", "Auto-Rotate image to best fit page", "Image to Portrait orientation", "Image to Landscape orientation", "90 degrees"],
                menubutton_width = 40,
                command = self.changeRotation
        )
        self.rotationSelectionMenu.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = E)
      
        # set up the Margins Group
        self.marginsGroup = Pmw.Group(self.layoutPage, tag_text = "Margins and Positioning")
        self.marginsGroup.pack(expand = YES, fill = BOTH, side = TOP, padx = 5, pady = 5)
        
        self.positioningTypeVar = tkinter.StringVar()
        self.positioningTypeVar.set("User-defined margins")
        self.positioningTypeMenu = Pmw.OptionMenu(self.marginsGroup.interior(),
                labelpos = 'w',
                label_text = 'Positioning Method:',
                menubutton_textvariable = self.positioningTypeVar,
                items = ["User-defined margins", "Auto-Center on Page", "Auto-Center in Printable Area"],
                menubutton_width = 40,
                command = self.changePositioning)
        self.positioningTypeMenu.grid(row = 0, column = 0, columnspan = 4, padx = 5, pady = 5, sticky = E)        
        
        tkinter.Label(self.marginsGroup.interior(), text = "Top Margin:").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = W)
        tkinter.Label(self.marginsGroup.interior(), text = "Left/Right Margins:").grid(row = 2, column = 0, padx = 5, pady = 5, sticky = W)
        tkinter.Label(self.marginsGroup.interior(), text = "Bottom Margin:").grid(row = 3, column = 0, padx = 5, pady = 5, sticky = W)
        
        self.topMarginEntry = Pmw.EntryField(self.marginsGroup.interior(),
                value = 0,
                entry_width = 12,
                validate = validateFloat,
                modifiedcommand = self.changeTopMargin
        )
        self.topMarginEntry.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = W)        
                
        self.leftMarginEntry = Pmw.EntryField(self.marginsGroup.interior(),
                value = 0,
                entry_width = 12,
                validate = validateFloat,
                modifiedcommand = self.changeLeftMargin
        )
        self.leftMarginEntry.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = W)
        
        self.rightMarginVar = tkinter.StringVar()
        self.rightMarginVar.set(0)
        self.rightMarginEntry = tkinter.Entry(self.marginsGroup.interior(), textvariable = self.rightMarginVar, width = 12)
        self.rightMarginEntry.grid(row = 2, column = 3, padx = 5, pady = 5, sticky = W)
        self.rightMarginEntry.configure(state = tkinter.DISABLED, bg = "light gray")
        
        self.bottomMarginVar = tkinter.StringVar()
        self.bottomMarginVar.set(0)
        self.bottomMarginEntry = tkinter.Entry(self.marginsGroup.interior(), textvariable = self.bottomMarginVar, width = 12)
        self.bottomMarginEntry.grid(row = 3, column = 2, padx = 5, pady = 5, sticky = W)
        self.bottomMarginEntry.configure(state=tkinter.DISABLED, bg = "light gray")

        self.resetManualMarginsButton = tkinter.Button(self.marginsGroup.interior(), text = "Reset", command = self.resetManualMargins)
        self.resetManualMarginsButton.grid(row = 2, column = 2)

        # set up the sizing group
        self.sizingGroup = Pmw.Group(self.layoutPage, tag_text = "Sizing")
        self.sizingGroup.pack(expand = YES, fill = BOTH, side = TOP, padx = 5, pady = 5)

        self.sizingTypeVar = tkinter.StringVar()
        self.sizingTypeVar.set("No resizing")
        self.sizingTypeMenu = Pmw.OptionMenu(self.sizingGroup.interior(),
                labelpos = 'w',
                label_text = 'Sizing Method:',
                label_width = 20,
                menubutton_textvariable = self.sizingTypeVar,
                items = ["No resizing", "Auto-fit to page size", "User-defined maximum size", "User-defined exact size (crop)", "User-defined image resolution (pixels/unit)"],
                menubutton_width = 40,
                command = self.changeSizingTypes
        )
        self.sizingTypeMenu.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = E)        
        
        tkinter.Label(self.sizingGroup.interior(), text = "Image Resolution (pixels/unit):").grid(row = 1, column = 0, sticky = W, padx = 5, pady = 5)
        tkinter.Label(self.sizingGroup.interior(), text = "Image Width:").grid(row = 2, column = 0, sticky = W, padx = 5, pady = 5)
        tkinter.Label(self.sizingGroup.interior(), text = "Image Height:").grid(row = 3, column = 0, sticky = W, padx = 5, pady = 5)

        self.imageResolutionEntry = Pmw.EntryField(self.sizingGroup.interior(),
                value = 1,
                entry_width = 20,
                validate = {'validator' : 'real', 'min' : 1, 'max' : 99999, 'minstrict' : 1},
                modifiedcommand = self.changeResolution
        )
        self.imageResolutionEntry.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = W)
        
        self.resetImageResButton = tkinter.Button(self.sizingGroup.interior(), text = "Reset", command = self.resetImageRes)
        self.resetImageResButton.grid(row = 1, column = 2)

        self.widthEntry = Pmw.EntryField(self.sizingGroup.interior(),
                value = 0,
                entry_width = 20,
                validate = {'validator' : 'real', 'min' : 0, 'max' : 99999, 'minstrict' : 0},
                modifiedcommand = self.changeWidth
        )
        self.widthEntry.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = W)
        
        self.heightEntry = Pmw.EntryField(self.sizingGroup.interior(),
                value = 0,
                entry_width = 20,
                validate = {'validator' : 'real', 'min' : 0, 'max' : 99999, 'minstrict' : 0},
                modifiedcommand = self.changeHeight
        )
        self.heightEntry.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = W)
        
        #--------------------------------
        # Add the "Color Management" tab.
        #--------------------------------
        if CAN_DO_ICC and not self.hideICC:
            self.colorManagementPage = self.notebook.add('Color Management')
            self.ICCenabledVar = tkinter.IntVar()
            self.ICCenabledVar.set("")
            self.ICCgroup = Pmw.Group(self.colorManagementPage, tag_text = 'Enable ICC Color Management',
                                      tag_pyclass = tkinter.Checkbutton,
                                      tag_variable = self.ICCenabledVar,
                                      tag_command = self.toggleICC)
            self.ICCgroup.pack(expand = YES, fill = X, side = TOP, padx = 5, pady = 5)
            
            # set up the input profiles
            self.ICCinputGroup = Pmw.Group(self.ICCgroup.interior(), tag_text = 'Input Profiles')
            self.ICCinputGroup.pack(expand = YES, fill = X, side = TOP, padx = 5, pady = 5)
            tkinter.Label(self.ICCinputGroup.interior(), text = "RGB Input Profile:").grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W)
            tkinter.Label(self.ICCinputGroup.interior(), text = "CMYK Input Profile:").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = W)
            
            self.ICCinputProfileRGBVar = tkinter.StringVar()
            self.ICCinputProfileRGBVar.set("")
            self.ICCinputProfileCMYKVar = tkinter.StringVar()
            self.ICCinputProfileCMYKVar.set("")
    
            self.ICCinputProfileRGBEntry = tkinter.Entry(self.ICCinputGroup.interior(), textvariable = self.ICCinputProfileRGBVar, width = 35)
            self.ICCinputProfileRGBEntry.grid(row = 0, column = 1, padx = 5, pady = 5)
            self.ICCinputProfileRGBEntry.configure(state = tkinter.DISABLED)
            self.ICCinputProfileCMYKEntry = tkinter.Entry(self.ICCinputGroup.interior(), textvariable = self.ICCinputProfileCMYKVar, width = 35)
            self.ICCinputProfileCMYKEntry.grid(row = 1, column = 1, padx = 5, pady = 5)
            self.ICCinputProfileCMYKEntry.configure(state = tkinter.DISABLED)
            
            tkinter.Button(self.ICCinputGroup.interior(), text = "Browse", command = lambda x = None, self = self: self.browseForProfile("ICCInputProfileRGB")).grid(row = 0, column = 2, padx = 5, pady = 2)
            tkinter.Button(self.ICCinputGroup.interior(), text = "Browse", command = lambda x = None, self = self: self.browseForProfile("ICCInputProfileCMYK")).grid(row = 1, column = 2, padx = 5, pady = 2)
            
            # set up the output profiles
            self.ICCoutputGroup = Pmw.Group(self.ICCgroup.interior(), tag_text = 'Printer Profile')
            self.ICCoutputGroup.pack(expand = YES, fill = X, side = TOP, padx = 5, pady = 5)
            
            tkinter.Label(self.ICCoutputGroup.interior(), text = "Printer profiles MUST be in RGB format, even if you have a 4-color (CMYK) printer!", wraplength = 300).grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5)
            tkinter.Label(self.ICCoutputGroup.interior(), text = "RGB Printer Profile:").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = W)
            
            self.ICCoutputProfileVar = tkinter.StringVar()
            self.ICCoutputProfileVar.set("")

            self.ICCoutputProfileEntry = tkinter.Entry(self.ICCoutputGroup.interior(), textvariable = self.ICCoutputProfileVar, width = 35)
            self.ICCoutputProfileEntry.grid(row = 1, column = 1, padx = 5, pady = 5)
            self.ICCoutputProfileEntry.configure(state = tkinter.DISABLED)

            tkinter.Button(self.ICCoutputGroup.interior(), text = "Browse", command = lambda x = None, self = self: self.browseForProfile("ICCOutputProfile")).grid(row = 1, column = 2, padx = 5, pady = 2)
            
            # set up the rendering intent
            self.ICCintentGroup = Pmw.Group(self.ICCgroup.interior(), tag_text = 'Rendering Intent')
            self.ICCintentGroup.pack(expand = YES, fill = X, side = TOP, padx = 5, pady = 5)

            self.renderingIntentVar = tkinter.StringVar()
            self.renderingIntentVar.set("Perceptual")
            
            self.renderingIntentMenu = Pmw.OptionMenu(self.ICCintentGroup.interior(),
                    labelpos = 'w',
                    label_text = 'Rendering Intent:',
                    label_width = 20,
                    menubutton_textvariable = self.renderingIntentVar,
                    items = ["Perceptual", "Relative Colorimetric", "Saturation", "Absolute Colorimetric"],
                    menubutton_width = 40,
                    command = self.changeRenderingIntent
            )
            self.renderingIntentMenu.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = E)
            
        #-----------------------
        # Add the "Preview" tab.
        #-----------------------
        self.previewPage = self.notebook.add('Preview')

        self.previewPageFrame = previewPageClass(self.previewPage, im = self.im)
        self.previewPageFrame.pack(expand = YES, fill = BOTH)

        self.notebook.setnaturalsize()
        
        # add the buttons
        self.buttonFrame = tkinter.Frame(self.main)
        self.buttonFrame.pack(expand = YES, fill = X)

        if self.im != None and self.allowPrinting:
            tkinter.Button(self.buttonFrame, text = "Print", command = self.clickPrint, width = 8).pack(side = tkinter.RIGHT, padx = 5, pady = 5)
        tkinter.Button(self.buttonFrame, text = "Apply", command = self.clickApply, width = 8).pack(side = tkinter.RIGHT, padx = 5, pady = 5)
        tkinter.Button(self.buttonFrame, text = "Cancel", command = self.clickCancel, width = 8).pack(side = tkinter.RIGHT, padx = 5, pady = 5)
        tkinter.Button(self.buttonFrame, text = "OK", command = self.clickOK, width = 8).pack(side = tkinter.RIGHT, padx = 5, pady = 5)

        # update the GUI, then call all the change handlers to configure the GUI for the current settings
        self.updateGUI()
        self.changeSizingTypes()
        self.changeUnits()
        self.changeRotation()
        self.changePositioning()
        if CAN_DO_ICC:
            self.toggleICC()
            self.changeRenderingIntent()
        
        # bind <Control-H> to show the version in the title
        self.main.bind("<Control-h>", self.showVersion)
        self.main.bind("<Control-H>", self.showVersion)
        
        # flag that the GUI was created properly
        self.GUI_OK = True
        
    def changePages(self, pageName):
        if pageName == "Preview":
            self.getPrinterCaps()
            self.previewPageFrame.update(self.pSettings, self.printerCaps)
            
    def showVersion(self, event = None):
        # Show the version of WinPILprint.py in the title, accessed by Control-H
        #     leave my contact info here alone please!!!  Thanks!
        self.main.title("WinPILprint.py version %s by Kevin Cazabon (kevin@cazabon.com)" %VERSION)
        
    def browseForProfile(self, profileType):
        curProfile = self.pSettings[profileType]
        if curProfile == None or not os.path.isfile(curProfile):
            initialdir = None
            initialfile = None
        else:
            initialdir, initialfile = os.path.split(curProfile)

                    
        newProfile = tkFileDialog.askopenfilename(filetypes = [("ICC profiles", ("*.icm", "*.icc"))], initialdir = initialdir, initialfile = initialfile, title = "Select Profile")

        if os.path.isfile(newProfile):
            self.pSettings[profileType] = newProfile
            
        self.updateGUI()
        
    def toggleICC(self, event = None):
        self.pSettings["applyColorManagement"] = self.ICCenabledVar.get()
        
        # depending on the value of colorManagement, show or hide the setup dialogs
        if self.pSettings["applyColorManagement"]:
            self.ICCinputGroup.pack(expand = YES, fill = X, side = TOP, padx = 5, pady = 5)
            self.ICCoutputGroup.pack(expand = YES, fill = X, side = TOP, padx = 5, pady = 5)
            self.ICCintentGroup.pack(expand = YES, fill = X, side = TOP, padx = 5, pady = 5)

        else:
            self.ICCinputGroup.pack_forget()
            self.ICCoutputGroup.pack_forget()
            self.ICCintentGroup.pack_forget()

    def changeRenderingIntent(self, event = None):
        intent = self.renderingIntentVar.get()
        if intent == "Perceptual":
            self.pSettings["ICCrenderingIntent"] = INTENT_PERCEPTUAL
        elif intent == "Relative Colorimetric":
            self.pSettings["ICCrenderingIntent"] = INTENT_RELATIVE_COLORIMETRIC
        elif intent == "Saturation":
            self.pSettings["ICCrenderingIntent"] = INTENT_SATURATION
        elif intent == "Absolute Colorimetric":
            self.pSettings["ICCrenderingIntent"] = INTENT_ABSOLUTE_COLORIMETRIC       
        
    def changeCopies(self, tabName = None):
        self.pSettings["copies"] = int(self.copyCountEntry.getvalue())
        self.updateGUI()

    def changePrinter(self, event = None):
        self.pSettings["printerName"] = self.selectedPrinterVar.get()
        self.getPrinterCaps()
        self.resetManualMargins()
        self.updateGUI()
        
    def changeUnits(self, event = None):
        # the Layout page needs to be converted to the new units
        units = self.unitsVar.get()

        if units == "Inches":
            self.pSettings["displayUnits"] = UNITS_INCH
        elif units == "mm":
            self.pSettings["displayUnits"] = UNITS_MM
        else:
            self.pSettings["displayUnits"] = UNITS_DEVICE
            
        self.updateGUI()

    def changeRotation(self, event = None):
        rotation = self.rotationVar.get()

        if rotation == "Auto-Rotate image to best fit page":
            self.pSettings["rotationType"] = ROTATION_AUTO
        elif rotation == "Image to Portrait orientation":
            self.pSettings["rotationType"] = ROTATION_PORTRAIT
        elif rotation == "Image to Landscape orientation":
            self.pSettings["rotationType"] = ROTATION_LANDSCAPE
        elif rotation == "90 degrees":
            self.pSettings["rotationType"] = ROTATION_90
        else:
            self.pSettings["rotationType"] = ROTATION_NONE

        self.updateGUI()
        
    def changePositioning(self, event = None):
        positioning = self.positioningTypeVar.get()
        
        if positioning == "Auto-Center on Page":
            self.pSettings["positioningType"] = POSITIONING_AUTO_CENTER_ON_PAGE
        elif positioning == "Auto-Center in Printable Area":
            self.pSettings["positioningType"] = POSITIONING_AUTO_CENTER_IN_PRINTABLE_AREA
        else:
            self.pSettings["positioningType"] = POSITIONING_MANUAL

        # depending on positoning option, hide or show margin entries
        if self.pSettings["positioningType"] == POSITIONING_MANUAL:
            self.leftMarginEntry._entryFieldEntry.configure(bg = "white", state = tkinter.NORMAL)
            self.topMarginEntry._entryFieldEntry.configure(bg = "white", state = tkinter.NORMAL)
        else:
            self.leftMarginEntry._entryFieldEntry.configure(bg = "light gray", state = tkinter.DISABLED)
            self.topMarginEntry._entryFieldEntry.configure(bg = "light gray", state = tkinter.DISABLED)

        self.updateGUI()

    def changeLeftMargin(self, event = None):
        if self.pSettings["margins"] == None:
            self.pSettings["margins"] = [None, None]
            
        if self.pSettings["positioningType"] != POSITIONING_MANUAL:
            return

        try:
            units = self.pSettings["displayUnits"]
            res = float(self.printerCaps["res"][units][0])
            self.pSettings["margins"][0] = int((float(self.leftMarginEntry.getvalue()) * res) + 0.5)
        except ValueError:
            pass
        
        self.updateGUI(ignore = "leftMargin")

        
    def changeTopMargin(self, event = None):
        if self.pSettings["margins"] == None:
            self.pSettings["margins"] = [None, None]
            
        if self.pSettings["positioningType"] != POSITIONING_MANUAL:
            return
        
        try:
            units = self.pSettings["displayUnits"]
            res = float(self.printerCaps["res"][units][1])
            self.pSettings["margins"][1] = int((float(self.topMarginEntry.getvalue()) * res) + 0.5)
        except ValueError:
            pass
        
        self.updateGUI(ignore = "topMargin")
        
    def changeSizingTypes(self, event = None):
        sizing = self.sizingTypeVar.get()
        
        if sizing == "Auto-fit to page size":
            self.pSettings["sizingType"] = SIZING_AUTO_FIT
        elif sizing == "User-defined maximum size":
            self.pSettings["sizingType"] = SIZING_MAX_SIZE
        elif sizing == "User-defined exact size (crop)":
            self.pSettings["sizingType"] = SIZING_EXACT_SIZE
        elif sizing == "User-defined image resolution (pixels/unit)":
            self.pSettings["sizingType"] = SIZING_MANUAL_RESOLUTION
        else:
            self.pSettings["sizingType"] = SIZING_NONE

        # depending on the sizing type, show or hide the sizing entries
        # FIXME: you should be able to show the sizing that's generated automatically if there's an image... upgrade later
        if self.pSettings["sizingType"] in [SIZING_MAX_SIZE, SIZING_EXACT_SIZE]:
            if self.pSettings["imageSize"] == None:
                self.pSettings["imageSize"] = self.printerCaps["pageSize"][UNITS_DEVICE]
                
            self.widthEntry._entryFieldEntry.configure(bg = "white", state = tkinter.NORMAL)
            self.heightEntry._entryFieldEntry.configure(bg = "white", state = tkinter.NORMAL)
        else:
            self.widthEntry._entryFieldEntry.configure(bg = "light gray", state = tkinter.DISABLED)
            self.heightEntry._entryFieldEntry.configure(bg = "light gray", state = tkinter.DISABLED)
            
        if self.pSettings["sizingType"] == SIZING_MANUAL_RESOLUTION:
            # enable the image resolution boxes
            self.imageResolutionEntry._entryFieldEntry.configure(bg = "white", state = tkinter.NORMAL)
        else:
            # hide the image resolution boxes
            self.imageResolutionEntry._entryFieldEntry.configure(bg = "light gray", state = tkinter.DISABLED)
            
        self.updateGUI()

    def resetManualMargins(self, event = None):
        self.pSettings["margins"] = [self.printerCaps["printerMargins"][UNITS_DEVICE][0], self.printerCaps["printerMargins"][UNITS_DEVICE][1]]
        self.updateGUI()
        
    def changeResolution(self, event = None):
        if self.pSettings["sizingType"] not in [SIZING_MANUAL_RESOLUTION, SIZING_NONE]:
            return
        
        try:
            units = self.pSettings["displayUnits"]
            if units == UNITS_INCH:
                res = [float(self.imageResolutionEntry.getvalue())] * 2
            elif units == UNITS_MM:
                res = [float(self.imageResolutionEntry.getvalue()) * 25.4] * 2
            else:
                res = [float(self.imageResolutionEntry.getvalue()) * self.printerCaps["res"][UNITS_DEVICE][0]] * 2
                
            self.pSettings["imageRes"] = res
        except ValueError:
            # blank input likely
            pass
        
        self.updateGUI(ignore = "res")
        
    def resetImageRes(self, event = None):
        self.pSettings["imageRes"] = self.pSettings["origImRes"]
        self.updateGUI()
        
    def changeWidth(self, event = None):
        if self.pSettings["sizingType"] in [SIZING_MANUAL_RESOLUTION, SIZING_NONE]:
            return
        
        if self.pSettings["imageSize"] == None:
            self.pSettings["imageSize"] = [None, None]
            
        try:
            units = self.pSettings["displayUnits"]
            res = float(self.printerCaps["res"][units][0])
            self.pSettings["imageSize"][0] = int((float(self.widthEntry.getvalue()) * res) + 0.5)
        except ValueError:
            pass
        
        self.updateGUI(ignore = "width")
    
    def changeHeight(self, event = None):
        if self.pSettings["sizingType"] in [SIZING_MANUAL_RESOLUTION, SIZING_NONE]:
            return
        
        if self.pSettings["imageSize"] == None:
            self.pSettings["imageSize"] = [None, None]
            
        try:
            units = self.pSettings["displayUnits"]
            res = float(self.printerCaps["res"][units][1])
            self.pSettings["imageSize"][1] = int((float(self.heightEntry.getvalue()) * res) + 0.5)
        except ValueError:
            pass
        
        self.updateGUI(ignore = "height")
            
    def clickCancel(self, event = None):
        self.die("Cancel")
        
    def clickOK(self, event = None):
        self.getSettingsFromGUI()
        self.backupSettings = copy.copy(self.pSettings)
        self.die("OK")
        
    def clickApply(self, event = None):
        self.getSettingsFromGUI()
        self.backupSettings = copy.copy(self.pSettings)
        
    def clickPrint(self, event = None):
        self.clickApply()
        self.setCursor("busy")
        
        #FIXME: this is a hack because we can't try/except all the win32 errors that can occur during
        #    printing, sorry!
        #printThread = threading.Thread(target = spawnPrintJob, args = (self.im, self.pSettings))
        #printThread.start()
        
        #FIXME: this is what it should be, assuming printImage could catch errors in printing
        status, message, settings = printImage(self.im, settings = self.pSettings)
        if status != STATUS_PRINTED:
            self.showError("Error during printing", message)
            
        self.setCursor("normal")
        if self.closeAfterPrint:
            self.die("Print")

    def setCursor(self, state):
        if state == "busy":
            self.main.configure(cursor = "watch")
            self.main.update_idletasks()
        else:
            self.main.configure(cursor = "arrow")
            
    def showError(self, title, message):
        self.errorTopLevel = tkinter.Toplevel(self.main)
        self.errorTopLevel.title(title)
        tkinter.Label(self.errorTopLevel, text = message, wraplength = 300).pack(padx = 20, pady = 20)
            
    def updateGUI(self, event = None, ignore = None):
        # Check and/or set the updateInProgress flag, so we don't get double updates or loops
        if self.updateInProgress == True:
            return
        else:
            self.updateInProgress = True
            
        # update the Printer tab
        self.printerSelectionMenu.setitems(findPrinterNames())
        self.getPrinterCaps()
        
        resInches = [float(self.printerCaps["res"][UNITS_INCH][0]), float(self.printerCaps["res"][UNITS_INCH][1])]
        resMM = [float(self.printerCaps["res"][UNITS_MM][0]), float(self.printerCaps["res"][UNITS_MM][1])]
                
        self.dpiLabel.configure(text = "%s x %s dpi" %(round(resInches[0], 4), round(resInches[1], 4)))
        self.dpmmLabel.configure(text = "%s x %s dpmm" %(round(resMM[0], 4), round(resMM[1], 4)))
        self.pageSizeInchesLabel.configure(text = "%s\" x %s\"" %(round(self.printerCaps["pageSize"][UNITS_INCH][0], 4), round(self.printerCaps["pageSize"][UNITS_INCH][1], 4)))
        self.pageSizeMMLabel.configure(text = "%s mm x %s mm" %(round(self.printerCaps["pageSize"][UNITS_MM][0], 4), round(self.printerCaps["pageSize"][UNITS_MM][1], 4)))
        self.printableWidthInchesLabel.configure(text = "%s\" x %s\"" %(round(self.printerCaps["printableArea"][UNITS_INCH][0], 4), round(self.printerCaps["printableArea"][UNITS_INCH][1], 4)))
        self.printableWidthMMLabel.configure(text = "%s mm x %s mm" %(round(self.printerCaps["printableArea"][UNITS_MM][0], 4), round(self.printerCaps["printableArea"][UNITS_MM][1], 4)))
        self.leftPrinterMarginInchesLabel.configure(text = "%s\"" %(round(self.printerCaps["printerMargins"][UNITS_INCH][0], 4)))
        self.rightPrinterMarginInchesLabel.configure(text = "%s\"" %(round(self.printerCaps["printerMargins"][UNITS_INCH][2], 4)))
        self.topPrinterMarginInchesLabel.configure(text = "%s\"" %(round(self.printerCaps["printerMargins"][UNITS_INCH][1], 4)))
        self.bottomPrinterMarginInchesLabel.configure(text = "%s\"" %(round(self.printerCaps["printerMargins"][UNITS_INCH][3], 4)))   
        
        self.leftPrinterMarginMMLabel.configure(text = "%s mm" %(round(self.printerCaps["printerMargins"][UNITS_MM][0], 4)))
        self.rightPrinterMarginMMLabel.configure(text = "%s mm" %(round(self.printerCaps["printerMargins"][UNITS_MM][2], 4)))
        self.topPrinterMarginMMLabel.configure(text = "%s mm" %(round(self.printerCaps["printerMargins"][UNITS_MM][1], 4)))
        self.bottomPrinterMarginMMLabel.configure(text = "%s mm" %(round(self.printerCaps["printerMargins"][UNITS_MM][3], 4)))   
        
        # update the Layout tab
        if self.pSettings["displayUnits"] == UNITS_DEVICE:
            self.unitsVar.set("Device units")
        elif self.pSettings["displayUnits"] == UNITS_MM:
            self.unitsVar.set("mm")
        else:    # default to inches... sorry Europeans!
            self.pSettings["displayUnits"] = UNITS_INCH
            self.unitsVar.set("Inches")
        
        if self.pSettings["rotationType"] == ROTATION_90:
            self.rotationVar.set("90 degrees")
        elif self.pSettings["rotationType"] == ROTATION_AUTO:
            self.rotationVar.set("Auto-Rotate image to best fit page")
        elif self.pSettings["rotationType"] == ROTATION_PORTRAIT:
            self.rotationVar.set("Image to Portrait orientation")
        elif self.pSettings["rotationType"] == ROTATION_LANDSCAPE:
            self.rotationVar.set("Image to Landscape orientation")
        else:
            self.pSettings["rotationType"] = ROTATION_NONE
            self.rotationVar.set("None")
        
        if self.pSettings["positioningType"] == POSITIONING_AUTO_CENTER_ON_PAGE:
            self.positioningTypeVar.set("Auto-Center on Page")
        elif self.pSettings["positioningType"] == POSITIONING_AUTO_CENTER_IN_PRINTABLE_AREA:
            self.positioningTypeVar.set("Auto-Center in Printable Area")
        else:
            self.pSettings["positioningType"] = POSITIONING_MANUAL
            self.positioningTypeVar.set("User-defined margins")
        
        if self.pSettings["sizingType"] == SIZING_AUTO_FIT:
            self.sizingTypeVar.set("Auto-fit to page size")
        elif self.pSettings["sizingType"] == SIZING_MAX_SIZE:
            self.sizingTypeVar.set("User-defined maximum size")
        elif self.pSettings["sizingType"] == SIZING_EXACT_SIZE:
            self.sizingTypeVar.set("User-defined exact size (crop)")
        elif self.pSettings["sizingType"] == SIZING_MANUAL_RESOLUTION:
            self.sizingTypeVar.set("User-defined image resolution (pixels/unit)")
        else:
            self.pSettings["sizingType"] = SIZING_NONE
            self.sizingTypeVar.set("No resizing")
        
        # figure out the margins in UNITS_DEVICE first
        if self.im == None:
            imSize = (1,1)
        else:
            imSize = self.im.size

        [xMargin, yMargin], outputSize, needsRotation = findImageSizeAndMargins(imSize, self.pSettings)
        
        rMargin = self.printerCaps["pageSize"][UNITS_DEVICE][0] - outputSize[0] - xMargin
        bMargin = self.printerCaps["pageSize"][UNITS_DEVICE][1] - outputSize[1] - yMargin

        # figure out the effective resolution of the image now, for display purposes
        #     we cheat and force the same x/y resolution... maybe upgrade later.
        if self.pSettings["sizingType"] != SIZING_MANUAL_RESOLUTION:
            if self.im != None and outputSize[0] > 0:
                imRes = float(self.im.size[0]) / (float(outputSize[0]) / resInches[0])
                self.pSettings["imageRes"] = [imRes, imRes]
            else:
                pass
  
        # now convert to displayUnits
        if self.pSettings["displayUnits"] == UNITS_INCH:
            if ignore != "leftMargin":
                self.leftMarginEntry.setvalue(round(xMargin / resInches[0], 4))      
            if ignore != "topMargin":
                self.topMarginEntry.setvalue(round(yMargin / resInches[1], 4))
            self.rightMarginVar.set(round(rMargin / resInches[0], 4))
            self.bottomMarginVar.set(round(bMargin / resInches[1], 4))
            if ignore != "res":
                self.imageResolutionEntry.setvalue(round(self.pSettings["imageRes"][0], 4))
            if ignore != "width" and self.pSettings["sizingType"] != SIZING_MAX_SIZE:
                self.widthEntry.setvalue(round(outputSize[0] / resInches[0], 4))
            if ignore != "height" and self.pSettings["sizingType"] != SIZING_MAX_SIZE:
                self.heightEntry.setvalue(round(outputSize[1] / resInches[1], 4))
            
        elif self.pSettings["displayUnits"] == UNITS_MM:
            if ignore != "leftMargin":
                self.leftMarginEntry.setvalue(round(xMargin / resMM[0], 4))      
            if ignore != "topMargin":
                self.topMarginEntry.setvalue(round(yMargin / resMM[1], 4))
            self.rightMarginVar.set(round(rMargin / resMM[0], 4))
            self.bottomMarginVar.set(round(bMargin / resMM[1], 4))
            if ignore != "res":
                self.imageResolutionEntry.setvalue(round(self.pSettings["imageRes"][0] / 25.4, 4))
            if ignore != "width" and self.pSettings["sizingType"] != SIZING_MAX_SIZE:
                self.widthEntry.setvalue(round(outputSize[0] / resMM[0], 4))
            if ignore != "height" and self.pSettings["sizingType"] != SIZING_MAX_SIZE:
                self.heightEntry.setvalue(round(outputSize[1] / resMM[1], 4))
            
        else:    # device units
            if ignore != "leftMargin":
                self.leftMarginEntry.setvalue(xMargin)
            if ignore != "topMargin":
                self.topMarginEntry.setvalue(yMargin)
            self.rightMarginVar.set(rMargin)
            self.bottomMarginVar.set(bMargin)
            if ignore != "res":
                self.imageResolutionEntry.setvalue(round(self.pSettings["imageRes"][0], 4))
            if ignore != "width" and self.pSettings["sizingType"] != SIZING_MAX_SIZE:
                self.widthEntry.setvalue(outputSize[0])
            if ignore != "height" and self.pSettings["sizingType"] != SIZING_MAX_SIZE:
                self.heightEntry.setvalue(outputSize[1])

        # show or hide the resetManualMarginsButton
        if self.pSettings["positioningType"] == POSITIONING_MANUAL:
            self.resetManualMarginsButton.grid(row = 2, column = 2, sticky = E+W)
        else:
            try:
                self.resetManualMarginsButton.grid_forget()
            except:
                pass 
 
        # update the Color Management tab
        if CAN_DO_ICC and not self.hideICC:
            self.ICCenabledVar.set(self.pSettings["applyColorManagement"])
            self.ICCinputProfileRGBVar.set(self.pSettings["ICCInputProfileRGB"])
            self.ICCinputProfileCMYKVar.set(self.pSettings["ICCInputProfileCMYK"])
            self.ICCoutputProfileVar.set(self.pSettings["ICCOutputProfile"])        
    
            if self.pSettings["ICCRenderingIntent"] == INTENT_PERCEPTUAL:
                self.renderingIntentVar.set("Perceptual")
            elif self.pSettings["ICCRenderingIntent"] == INTENT_RELATIVE_COLORIMETRIC:
                self.renderingIntentVar.set("Relative Colorimetric")
            elif self.pSettings["ICCRenderingIntent"] == INTENT_SATURATION:
                self.renderingIntentVar.set("Saturation")
            elif self.pSettings["ICCRenderingIntent"] == INTENT_ABSOLUTE_COLORIMETRIC:
                self.renderingIntentVar.set("Absolute Colorimetric")    

        # call update so any pending callbacks are processed (such as updateGUI)
        self.main.update()

        # turn off the updateInProgress flag
        self.updateInProgress = False

    def getSettingsFromGUI(self):
        # call all the update features in case they haven't hit enter for each yet:
        self.changeCopies()
        self.changeWidth()
        self.changeHeight()
        self.changeLeftMargin()
        self.changeTopMargin()
        self.changeResolution()
        self.changeWidth()
        self.changeHeight()
          
    def getSettings(self):
        """Show the ImagePrintWin.printerSetup() dialog to the user and return the settings
        after they click OK.
        
        returns a tuple of (status, message, settings)
        
        status = 0 on success, -1 on user cancel, -2 on failure to create GUI
        settings = settings dictionary"""
        
        # if not self.GUI_OK (couldn't do a GUI properly), simply return the settings as-is
        if not self.GUI_OK:
            return (STATUS_ERROR, "Could not create GUI!", self.pSettings)
        
        # otherwise, show the GUI
        self.main.deiconify()
        self.main.lift(self.parent)
        self.main.focus_set()
        
        # wait until self.main is hidden or destroyed, and return the settings
        self.main.wait_window()
        
        if self.exitStatus == "OK":
            status = STATUS_OK
        if self.exitStatus == "Print":
            status = STATUS_PRINTED
        elif self.exitStatus == "Cancel":
            status = STATUS_USER_CANCEL
        elif self.exitStatus == "Close":
            status = STATUS_USER_CLOSE

        return (status, "Normal exit from printerSetup.getSettings()", self.pSettings)

    def die(self, exitStatus):
        self.exitStatus = exitStatus

        if type in ("Close", "Cancel"):
            # restore the last "applied" settings before returning
            self.pSettings = self.backupSettings
            
        self.main.destroy()
    

if __name__ == "__main__":
    # self test / demo
    
    # find all printers and print their printerCaps
    printers = findPrinterNames()
    print("*" *72)
    print("Printers:\n")
    for p in printers:
        print("\nPrinter:  %s" %p)
        caps = getPrinterCaps(p)
        items = caps.keys()
        items = sorted(items)
        for item in items:
            print("\t%s:\t%s" %(item, caps[item]))
    print("*" *72)

    # Test the printerSetup() GUI
    test = tkinter.Tk()
    im = browseForImageFile()
    if not os.path.isfile(im):
        im = None

    GUI = printerSetup(test, im = im, allowPrinting = True, closeAfterPrint = False)

    status, message, settings = GUI.getSettings()
    
    print("Settings returned!")
    for item in settings.keys():
        print("%s:\t%s" %(item, settings[item]))

    # you could print the image this way too, now that you have the settings
    #printImage(im, settings = settings)    
    
    test.mainloop()
    