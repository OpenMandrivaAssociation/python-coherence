%define debug_package %{nil}
%define modname Coherence
%define gstapi 0.10

Summary:	A DLNA/UPnP MediaServer/MediaRenderer in addition of a framework
Name:		python-coherence
Version:	0.6.6.2
Release:	11
Group:		Networking/File transfer 
License:	MIT
Url:		https://coherence.beebits.net/
Source0:	https://coherence.beebits.net/download/%{modname}-%{version}.tar.gz
Source1:	coherence.conf
Source2:	coherence-32x32.png
Patch0:		Coherence-0.6.0-daemon_name_fix.diff
BuildRequires:	imagemagick
BuildRequires:	python-setuptools
BuildRequires:	python-twisted-core
BuildRequires:	python-twisted-web
Provides:	coherence = %{version}
Requires:	python-twisted-core
Requires:	python-twisted-web
Requires:	python-twisted-conch >= 0.8
#Requires:	python-louie
Requires:	python-axiom >= 0.5.7
Requires:	python-epsilon >= 0.5.8
Requires:	python-configobj
Requires:	python-celementtree
Requires:	python-elementtree
Requires:	python-dbus
Requires:	python-mechanize
Requires:	pyid3lib
# Gstreamer
Requires:	gstreamer%{gstapi}-python
Requires:	gstreamer%{gstapi}-flac
Requires:	gstreamer%{gstapi}-plugins-base

Requires:	python-pkg-resources
Requires:	python-nose
Requires:	python-sqlite2
Requires(post,preun):	rpm-helper
BuildRequires:  python-devel

%description
As a stand-alone application Coherence acts as a DLNA/UPnP MediaServer and
exports local and remote media files via its plugins to other UPnP clients.
And together with GStreamer it forms a controllable DLNA/UPnP MediaRenderer.

%post
%_post_service coherence

%preun
%_preun_service coherence

%files 
%doc docs/coherence.conf.example 
%{_bindir}/coherence
%{_initrddir}/coherence
%config(noreplace) %{_sysconfdir}/coherence/*conf
%{py_platsitedir}/*
/srv/public
%{_datadir}/dbus-1/services/

#------------------------------------------------------------

%package applet
Summary:	Applet for controlling coherence
Group:		Networking/File transfer
Requires:	%{name}
Requires:	python-qt4
Requires:	python-qt4-core
Requires:	python-qt4-gui

%description applet
A simple desktop applet to control (start/stop) coherence

%files applet
%{_bindir}/applet-coherence
%{_iconsdir}/coherence/*
%{_datadir}/applications/%{name}-applet.desktop
%{_iconsdir}/coherence.png
%{_liconsdir}/coherence.png
%{_miconsdir}/coherence.png

#------------------------------------------------------------

%prep
%setup -qn %{modname}-%{version}
%patch0 -p0

%build
python setup.py build

%install
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/coherence
mkdir -p %{buildroot}/usr/share/icons/coherence
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}/srv/public
# Install the D-Bus service file
mkdir -p %{buildroot}/%{_datadir}/dbus-1/services

python setup.py install --root=%{buildroot} --install-lib=%{py_platsitedir}
install -m 755 misc/coherence-initscript.sh %{buildroot}/%{_initrddir}/coherence
install -m 644 %SOURCE1 %{buildroot}/%{_sysconfdir}/coherence
mv "%{buildroot}/%{py_platsitedir}/misc/Desktop-Applet/tango-system-file-manager.png" %{buildroot}/usr/share/icons/coherence
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

