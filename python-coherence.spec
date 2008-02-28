%define tarball_name Coherence

Name: python-coherence
Summary: A DLNA/UPnP MediaServer/MediaRenderer in addition of a framework
Version: 0.5.2
Release: %mkrel 0.20080228.1
Group: Networking/File transfer 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL: https://coherence.beebits.net/
Source0: https://coherence.beebits.net/download/%{tarball_name}-%version.tar.gz
License: MIT
Provides: coherence = %version
Requires: python-twisted-core
Requires: python-twisted-web
Requires: python-twisted-conch >= 0.8
Requires: python-louie
Requires: python-axiom >= 0.5.7
Requires: python-epsilon >= 0.5.8
Requires: python-configobj
Requires: python-celementtree
Requires: python-elementtree
Requires: pyid3lib
Requires: gstreamer0.10-python
Requires: python-setuptools
Requires: python-nose
Requires: python-sqlite2
BuildRequires: python-setuptools
%py_requires -d

%description
As a stand-alone application Coherence acts as a DLNA/UPnP MediaServer and
exports local and remote media files via its plugins to other UPnP clients.
And together with GStreamer it forms a controllable DLNA/UPnP MediaRenderer.

%files 
%defattr(-,root,root)
%doc docs/coherence.conf.example 
%_bindir/*
%py_platsitedir/*

#------------------------------------------------------------

%prep
%setup -q -n %{tarball_name}-%version

%build
python setup.py build

%install
rm -rf %buildroot

python setup.py install --root=%buildroot --install-lib=%py_platsitedir

%clean
rm -rf %buildroot

