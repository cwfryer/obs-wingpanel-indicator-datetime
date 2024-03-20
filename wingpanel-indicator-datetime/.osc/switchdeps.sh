#!/bin/sh
#
## Better safe than sorry
## These changes apply to the entire project
## for pkg in $(osc ls PROJECT); do if osc ls PROJECT/$pkg/switchdeps.sh; then osc branch -c PROJECT/$pkg; fi; done
## cd BRANCH/PACKAGE-WITH-CHANGES
## for pkg in ../*; do if [ -f "$pkg/switchdeps.sh" ]; then cp -f switchdeps.sh $pkg; fi; done
#
set -e
# Switch to a new gsettings schemas
# See the following packages: pantheon-desktop pantheon-session
# pantheon-mutter pantheon-desktop-schemas pantheon-settings-daemon
# Include: org.gnome.desktop org.gnome.mutter org.gnome.settings-daemon org.gnome.system
# Exclude: org.gnome.SessionManager (gsettings name = DBus name) You will need to do this manually
sed -e '/org.gnome.[A-Z]/!s/org\.gnome\.desktop/org.opensuse.pantheon.wrap.gnome.desktop/g' \
    -e '/org.gnome.[A-Z]/!s/org\/gnome\/desktop/org\/opensuse\/pantheon\/wrap\/gnome\/desktop/g' \
    -e '/org.gnome.[A-Z]/!s/org\.gnome\.mutter/org.opensuse.pantheon.wrap.gnome.mutter/g' \
    -e '/org.gnome.[A-Z]/!s/org\/gnome\/mutter/org\/opensuse\/pantheon\/wrap\/gnome\/mutter/g' \
    -e '/org.gnome.[A-Z]/!s/org\.gnome\.settings-daemon/org.opensuse.pantheon.wrap.gnome.settings-daemon/g' \
    -e '/org.gnome.[A-Z]/!s/org\/gnome\/settings-daemon/org\/opensuse\/pantheon\/wrap\/gnome\/settings-daemon/g' \
    -e '/org.gnome.[A-Z]/!s/org\.gnome\.system/org.opensuse.pantheon.wrap.gnome.system/g' \
    -e '/org.gnome.[A-Z]/!s/org\/gnome\/system/org\/opensuse\/pantheon\/wrap\/gnome\/system/g' \
    -i $(grep -rl 'org.gnome' | grep -v '^\.') || :
## Switch to new dependencies
sed -e '/pantheon/I!s/\bgnome-desktop-/pantheon-desktop-/g' \
    -e '/pantheon/I!s/\blibgnome-desktop-/pantheon-desktop-/g' \
    -e '/pantheon/I!s/\bgnome-settings-daemon\b/pantheon-settings-daemon/g' \
    -e '/pantheon/I!s/\bgsettings-desktop-schemas\b/pantheon-desktop-schemas/g' \
    -e '/pantheon/I!s/\bGnomeDesktop-/PantheonGnomeDesktop-/g' \
    -e '/pantheon/I!s/\bGDesktopEnums-/PantheonGDesktopEnums-/g' \
    -e '/pantheon/I!s/\blibmutter-/pantheon-mutter-/g' \
    -e '/pantheon/I!s/\bmutter-/pantheon-mutter-/g' \
    -i $(grep -Erl 'gnome-desktop|gnome-settings-daemon|gsettings-desktop-schemas|GnomeDesktop|GDesktopEnums|mutter' | grep -v '^\.') || :
## Switch to new binary files
sed -re '/(http)/!s/([^._/])\bmutter\b([^._/])/\1pantheon-mutter\2/g' \
    -re '/(http)/!s/([^._/])\bgnome-session\b([^._/])/\1pantheon-session\2/g' \
    -i $(grep -Erl 'mutter|gnome-session' | grep -E '(\.c|\.h|\.vala)$' | grep -v '^\.') || :
##
#
# Switch to bugs.opensuse.org
sed -re '/(\\|]|>[^>]*<|opensuse)/!s#(bug.*)http.*elementary.*("'"|'"')#\1https://bugs.opensuse.org\2#i' \
    -re '/(\\|>[^>]*<|opensuse)/!s#(bug.*)http.*elementary.*(])#\1https://bugs.opensuse.org\2#i' \
    -re '/(>[^>]*<|opensuse)/!s#(bug.*)http.*elementary.*(\\)#\1https://bugs.opensuse.org\2#i' \
    -re '/opensuse/!s#(bug.*>)http.*elementary.*(<)#\1https://bugs.opensuse.org\2#i' \
     -i $(grep -rli 'bug.*http.*elementary' | grep -v '^\.') || :
#
