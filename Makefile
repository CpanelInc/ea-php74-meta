OBS_PROJECT := EA4
OBS_PACKAGE := ea-php74-meta
DISABLE_BUILD := arch=i586
DISABLE_BUILD += repository=CentOS_9 repository=xUbuntu_22.04
include $(EATOOLS_BUILD_DIR)obs.mk
