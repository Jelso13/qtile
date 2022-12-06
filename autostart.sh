#!/bin/sh

picom -b &
nm-applet &
sudo blueman-applet &
#anki &
/usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &
