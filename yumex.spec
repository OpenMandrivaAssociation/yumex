%global app_id dk.yumex.Yumex
%global app_build release
%global dnf_backend DNF4
%global app_name yumex
%define gir 20240327

Name:     %{app_name}
Version:  4.99.4
Release:  3.%{git}.0
Summary:  Yum Extender graphical package management tool
Group:    Applications/System
License:  GPLv3+
URL:      http://yumex.dk
Source0:  https://github.com/timlau/yumex-ng/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: pkgconfig(python)
BuildRequires: meson
BuildRequires: pkgconfig(blueprint-compiler)
BuildRequires: python-blueprint-compiler
BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: appstream-util
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk4)
BuildRequires: pkgconfig(libadwaita-1)
BuildRequires: pkgconfig(pygobject-3.0)
BuildRequires: python-gobject3
BuildRequires: python3dist(pygobject)
BuildRequires: pkgconfig(gobject-introspection-1.0)


Requires: python-gobject3
Requires: python-gi
Requires: libadwaita-common
Requires: gtk4
Requires: flatpak

# dnf4 requirements
%if "%{dnf_backend}" == "DNF4"
Requires: python-dnfdaemon
Requires: python-dnf
%endif

# dnf5 requirements
%if "%{dnf_backend}" == "DNF5"
Requires: python3dist(libdnf5)
Requires: dnf5daemon-server
Requires: python3dist(dasbus)
%endif

Obsoletes: yumex-dnf <= 4.5.1

%description
Graphical package tool for maintain packages on the system

%prep
%autosetup -p1

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{app_id}.desktop

%build
%meson --buildtype=%{app_build} -Ddnf_backend=%{dnf_backend}
%meson_build

%install
%meson_install

%find_lang %{app_name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database %{_datadir}/applications &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files -f  %{app_name}.lang
%doc README.md
%license LICENSE
%{_datadir}/%{app_name}
%{_bindir}/%{app_name}
%{python3_sitelib}/%{app_name}/
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/icons/hicolor/
%{_metainfodir}/%{app_id}.metainfo.xml
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
