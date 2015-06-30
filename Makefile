TOCJS := $(shell ipython locate)/nbextensions/toc.js
TOCCSS := $(shell ipython locate)/nbextensions/toc.css
    
all: data custom

data: data/122.fits data/168.fits data/223.fits data/single-image.fits
    
custom: $(TOCJS) $(TOCCSS)

data/single-image.fits: /ngts/pipedev/ParanalOutput/running-the-pipeline/20150609-ng2000-802/Reduction/output/20150609-ng2000-802/20150609-ng2000-802_image_NG2000-4500/procIMAGE80220150610060740.fits
	cd data && ln -sv $< $(notdir $@)

data/122.fits: /ngts/pipedev/ParanalOutput/running-the-pipeline/20150609-ng2000-802/AperturePhot/output/20150609-ng2000-802/20150609-ng2000-802_image_NG2000-4500/output.fits
	cd data && ln -sv $< $(notdir $@)

data/168.fits: /ngts/pipedev/ParanalOutput/running-the-pipeline/20150611-ng2000-802/AperturePhot/output/20150611-ng2000-802/20150611-ng2000-802_image_NG2000-4500/output.fits
	cd data && ln -sv $< $(notdir $@)

data/223.fits: /ngts/pipedev/ParanalOutput/running-the-pipeline/20150610-ng2000-802/AperturePhot/output/20150610-ng2000-802/20150610-ng2000-802_image_NG2000-4500/output.fits
	cd data && ln -sv $< $(notdir $@)

$(TOCJS):
	curl -L https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.js > $@
    
$(TOCCSS):
	curl -L https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.css > $@
