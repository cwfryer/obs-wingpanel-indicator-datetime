#
# spec file for package wingpanel-indicator-datetime
#
# Copyright (c) 2021 SUSE LLC
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


%global __provides_exclude_from ^%{_libdir}/wingpanel/.*\\.so$
Name:           wingpanel-indicator-datetime
Version:        2.4.0
Release:        0
Summary:        Wingpanel Date & Time Indicator
License:        GPL-3.0-only
Group:          System/X11/Utilities
URL:            https://build.opensuse.org
Source:         https://github.com/elementary/wingpanel-indicator-datetime/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source100:      switchdeps.sh
BuildRequires:  evolution-data-server-devel
BuildRequires:  fdupes
BuildRequires:  meson >= 0.40.0
BuildRequires:  pkgconfig
BuildRequires:  vala >= 0.56.14
BuildRequires:  pkgconfig(granite)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libedataserver-1.2)
BuildRequires:  pkgconfig(libhandy-1)
BuildRequires:  pkgconfig(libical)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(wingpanel)
%if 0%{?suse_version} < 1600
BuildRequires:  icu.691-devel
%endif
Requires:       wingpanel
Recommends:     %{name}-lang

%description
A date and time indicator for Wingpanel.

%lang_package

%prep
%setup -q

cp %{SOURCE100} ..
sh -x ../switchdeps.sh

%build
%meson
%meson_build

%install
%meson_install
%fdupes %{buildroot}%{_datadir}/locale
%find_lang datetime-indicator %{name}.lang

%files
%license COPYING
%doc README.md
%dir %{_libdir}/wingpanel
%{_libdir}/wingpanel/libdatetime.so
%{_datadir}/glib-2.0/schemas/io.elementary.desktop.wingpanel.datetime.gschema.xml
%{_datadir}/metainfo/io.elementary.wingpanel.datetime.appdata.xml

%files lang -f %{name}.lang

%changelog
