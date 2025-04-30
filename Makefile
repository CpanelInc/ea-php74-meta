OBS_PROJECT := EA4
OBS_PACKAGE := ea-php74-meta
DISABLE_BUILD += repository=xUbuntu_22.04 repository=CentOS_9 repository=Almalinux_10
include $(EATOOLS_BUILD_DIR)obs.mk
