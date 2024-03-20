#
# spec file for package elementary-calendar
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global __provides_exclude_from ^%{_libdir}/.*/plugins/.*\\.so$
%define soname libelementary-calendar
%define sover 0
Name:           elementary-calendar
Version:        7.0.0
Release:        0
Summary:        Maya Calendar for the Pantheon Desktop
License:        GPL-3.0-or-later
Group:          Productivity/Office/Organizers
URL:            https://build.opensuse.org
Source:         https://github.com/elementary/calendar/archive/%{version}.tar.gz#/calendar-%{version}.tar.gz
Source100:      switchdeps.sh
BuildRequires:  elementary-icon-theme
BuildRequires:  fdupes
BuildRequires:  hicolor-icon-theme
BuildRequires:  meson
BuildRequires:  pkgconfig
BuildRequires:  update-desktop-files
BuildRequires:  pkgconfig(champlain-0.12)
BuildRequires:  pkgconfig(champlain-gtk-0.12)
BuildRequires:  pkgconfig(clutter-1.0)
BuildRequires:  pkgconfig(folks)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(geocode-glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(granite)
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.11.6
BuildRequires:  pkgconfig(libedataserver-1.2) >= 3.8.0
BuildRequires:  pkgconfig(libgeoclue-2.0)
BuildRequires:  pkgconfig(libhandy-1)
BuildRequires:  pkgconfig(libical)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libportal)
BuildRequires:  pkgconfig(libportal-gtk3)
BuildRequires:  pkgconfig(vapigen) >= 0.40.4
%if 0%{?suse_version} < 1600
BuildRequires:  icu.691-devel
%endif
Recommends:     %{name}-lang
Recommends:     %{name}-plugin-caldav
Recommends:     %{name}-plugin-google
Provides:       maya-calendar = %{version}
Obsoletes:      maya-calendar < %{version}

%description
A slim, lightweight GTK+3 calendar app written in Vala, designed for
Elementary OS where it is known simply as Calendar.

Also looks and works great on other GTK+ desktops.

%package -n     %{soname}%{sover}
Summary:        The Maya Calendar main library
Group:          System/Libraries

%description -n %{soname}%{sover}
A slim, lightweight GTK+3 calendar app written in Vala, designed for
Elementary OS where it is known simply as Calendar.

%package        plugin-caldav
Summary:        CalDAV Backend for %{name}
Group:          Productivity/Office/Organizers
Requires:       %{name} = %{version}
Provides:       %{name}-plugins

%description    plugin-caldav
A slim, lightweight GTK+3 calendar app written in Vala, designed for
Elementary OS where it is known simply as Calendar.

This plugin provides CalDAV synchronization.

%package        plugin-google
Summary:        Google Backend for %{name}
Group:          Productivity/Office/Organizers
Requires:       %{name} = %{version}
Provides:       %{name}-plugins

%description    plugin-google
A slim, lightweight GTK+3 calendar app written in Vala, designed for
Elementary OS where it is known simply as Calendar.

This plugin provides Google synchronization.

%package        devel
Summary:        Development files for %{soname}
Group:          Development/Libraries/C and C++
Requires:       %{soname}%{sover} = %{version}

%description    devel
This subpackage contains libraries and header files for developing
applications that want to make use of the libmaya shared library.

%lang_package

%prep
%setup -q -n calendar-%{version}

cp %{SOURCE100} ..
sh -x ../switchdeps.sh

%build
%meson
%meson_build

%install
%meson_install
%find_lang io.elementary.calendar %{name}.lang
%fdupes %{buildroot}/%{_datadir}

# dirlist HiDPI icons (see: hicolor/index.theme)
_dirlist=$PWD/dir.lst
pushd %{buildroot}
find ./ | while read _list; do
    echo $_list | grep '[0-9]\@[0-9]' || continue
    _path=$(echo $_list | sed 's/[^/]//')
    if ! ls ${_path%/*}; then
        grep -xqs "\%dir\ ${_path%/*}" $_dirlist || echo "%dir ${_path%/*}" >> $_dirlist
    fi
done
popd

%post -n %{soname}%{sover} -p /sbin/ldconfig
%postun -n %{soname}%{sover} -p /sbin/ldconfig

%files -f dir.lst
%license COPYING
%doc README*
%{_bindir}/io.elementary.calendar
%{_datadir}/applications/io.elementary.calendar.desktop
%{_datadir}/glib-2.0/schemas/io.elementary.calendar.gschema.xml
%{_datadir}/icons/hicolor/*/*/io.elementary.calendar.??g
%{_datadir}/metainfo/io.elementary.calendar.metainfo.xml
%dir %{_libdir}/io.elementary.calendar
%dir %{_libdir}/io.elementary.calendar/plugins

%files -n %{soname}%{sover}
%{_libdir}/libelementary-calendar.so.*

%files plugin-caldav
%dir %{_libdir}/io.elementary.calendar/plugins/CalDAV
%{_libdir}/io.elementary.calendar/plugins/CalDAV/libcaldav.so

%files plugin-google
%dir %{_libdir}/io.elementary.calendar/plugins/Google
%{_libdir}/io.elementary.calendar/plugins/Google/libgoogle.so

%files devel
%{_includedir}/elementary-calendar/
%{_libdir}/libelementary-calendar.so
%{_libdir}/pkgconfig/elementary-calendar.pc
%{_datadir}/vala/vapi/elementary-calendar.deps
%{_datadir}/vala/vapi/elementary-calendar.vapi

%files lang -f %{name}.lang

%changelog
