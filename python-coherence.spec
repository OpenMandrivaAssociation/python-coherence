%define tarball_name Coherence

Name: python-coherence
Summary: A DLNA/UPnP MediaServer/MediaRenderer in addition of a framework
Version: 0.6.6.2
Release: %mkrel 3
Group: Networking/File transfer 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL: https://coherence.beebits.net/
Source0: https://coherence.beebits.net/download/%{tarball_name}-%{version}.tar.gz
Source1: coherence.conf
Source2: coherence-32x32.png
Patch0: Coherence-0.6.0-daemon_name_fix.diff
License: MIT
Provides: coherence = %version
Requires: python-twisted-core
Requires: python-twisted-web
Requires: python-twisted-conch >= 0.8
#Requires: python-louie
Requires: python-axiom >= 0.5.7
Requires: python-epsilon >= 0.5.8
Requires: python-configobj
Requires: python-celementtree
Requires: python-elementtree
Requires: python-dbus
Requires: python-mechanize
Requires: pyid3lib
# Gstreamer
Requires: gstreamer0.10-python
Requires: gstreamer0.10-flac
Requires: gstreamer0.10-plugins-base

%if %mdkversion > 200900
Requires:	python-pkg-resources
%else
Requires: python-setuptools
%endif
Requires: python-nose
Requires: python-sqlite2
Requires(post):   rpm-helper
Requires(preun):  rpm-helper
BuildRequires: python-setuptools, imagemagick
BuildRequires: python-twisted-core
BuildRequires: python-twisted-web
%py_requires -d

%description
As a stand-alone application Coherence acts as a DLNA/UPnP MediaServer and
exports local and remote media files via its plugins to other UPnP clients.
And together with GStreamer it forms a controllable DLNA/UPnP MediaRenderer.

%post
%_post_service coherence

%preun
%_preun_service coherence

%files 
%defattr(-,root,root)
%doc docs/coherence.conf.example 
%_bindir/coherence
%_initrddir/coherence
%config(noreplace) %_sysconfdir/coherence/*conf
%py_platsitedir/*
/srv/public
%{_datadir}/dbus-1/services/

#------------------------------------------------------------

%package applet
Summary: Applet for controlling coherence
Group:  Networking/File transfer
Requires: %name
Requires: python-qt4, python-qt4-core, python-qt4-gui

%description applet
A simple desktop applet to control (start/stop) coherence

%files applet
%defattr(-,root,root)
%_bindir/applet-coherence
%{_iconsdir}/coherence/*
%{_datadir}/applications/%{name}-applet.desktop
%{_iconsdir}/coherence.png
%{_liconsdir}/coherence.png
%{_miconsdir}/coherence.png

#------------------------------------------------------------

%prep
%setup -q -n %{tarball_name}-%version
%patch0 -p0

%build
python setup.py build

%install
rm -rf %buildroot
mkdir -p %buildroot/%_initrddir
mkdir -p %buildroot/%_sysconfdir/coherence
mkdir -p %buildroot/usr/share/icons/coherence
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}/srv/public
# Install the D-Bus service file
%{__mkdir_p} %{buildroot}/%{_datadir}/dbus-1/services

python setup.py install --root=%buildroot --install-lib=%py_platsitedir
install -m 755 misc/coherence-initscript.sh %buildroot/%_initrddir/coherence
install -m 644 %SOURCE1 %buildroot/%_sysconfdir/coherence
mv "%buildroot/%py_platsitedir/misc/Desktop-Applet/tango-system-file-manager.png" %buildroot/usr/share/icons/coherence
install -m 644 misc/org.Coherence.service %{buildroot}/%{_datadir}/dbus-1/services/

# install icons
mkdir -p %{buildroot}%{_miconsdir}
mkdir -p %{buildroot}%{_iconsdir}
mkdir -p %{buildroot}%{_liconsdir}
install -m 644 %SOURCE2 %{buildroot}%{_iconsdir}/coherence.png
convert -scale 16x16 %SOURCE2 %{buildroot}%{_miconsdir}/coherence.png
convert -scale 48x48 %SOURCE2 %{buildroot}%{_liconsdir}/coherence.png

# menu
cat > %{buildroot}%{_datadir}/applications/%{name}-applet.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=Coherence
Comment=DLNA/UPnP MediaServer/MediaRenderer
Exec=applet-coherence
Icon=coherence
StartupNotify=true
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet;X-MandrivaLinux-CrossDesktop
EOF

%clean
rm -rf %buildroot

%changelog
