%define tarball_name Coherence

%define debug_package %{nil}

Name: python-coherence
Summary: A DLNA/UPnP MediaServer/MediaRenderer in addition of a framework
Version: 0.6.6.2
Release: 6
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

Requires:	python-pkg-resources
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
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
mkdir -p $RPM_BUILD_ROOT/srv/public
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
convert -scale 16x16 %SOURCE2 $RPM_BUILD_ROOT%{_miconsdir}/coherence.png
convert -scale 48x48 %SOURCE2 $RPM_BUILD_ROOT%{_liconsdir}/coherence.png

# menu
cat > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}-applet.desktop <<EOF
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



%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.6.2-3mdv2011.0
+ Revision: 667924
- mass rebuild

* Tue Nov 02 2010 Götz Waschk <waschk@mandriva.org> 0.6.6.2-2mdv2011.0
+ Revision: 591967
- rebuild for new python 2.7

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Clean spec file

* Sun Jan 03 2010 Frederik Himpe <fhimpe@mandriva.org> 0.6.6.2-1mdv2010.1
+ Revision: 485668
- Fix BuildRequires
- Update to new version 0.6.6.2

* Thu Oct 29 2009 Erwan Velu <erwan@mandriva.org> 0.6.4-3mdv2010.0
+ Revision: 460064
- Fixing dbus service file; solves #54984

* Wed Oct 07 2009 Erwan Velu <erwan@mandriva.org> 0.6.4-2mdv2010.0
+ Revision: 455573
- Using FHS is better. Putting the default file in /srv/public
- Removing default usage of /tmp

* Mon May 18 2009 Frederik Himpe <fhimpe@mandriva.org> 0.6.4-1mdv2010.0
+ Revision: 377315
- update to new version 0.6.4

* Mon Feb 23 2009 Erwan Velu <erwan@mandriva.org> 0.6.2-1mdv2009.1
+ Revision: 344324
- Fixing applet path
- 0.6.2

* Thu Jan 22 2009 Erwan Velu <erwan@mandriva.org> 0.6.0-4mdv2009.1
+ Revision: 332417
- Rebuild against new config file
- Removing dbus

* Wed Jan 21 2009 Erwan Velu <erwan@mandriva.org> 0.6.0-3mdv2009.1
+ Revision: 332385
- Disabling dbus as it can generate some high cpu usage

* Fri Jan 16 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-2mdv2009.1
+ Revision: 330134
- bump release
- fix the daemon name in the initscript

* Mon Jan 05 2009 Erwan Velu <erwan@mandriva.org> 0.6.0-1mdv2009.1
+ Revision: 325130
- 0.6.0

* Fri Dec 26 2008 Funda Wang <fwang@mandriva.org> 0.5.8-3mdv2009.1
+ Revision: 319370
- rebuild for new python

* Sat Nov 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.5.8-2mdv2009.1
+ Revision: 308076
- require python-pkg-resources for mdv version greater than 200900, instead of python-setuptools which requires bunch of useless python stuff and python-devel

* Thu Jul 03 2008 Erwan Velu <erwan@mandriva.org> 0.5.8-1mdv2009.0
+ Revision: 231380
- Adding source file
- 0.5.8

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 0.5.4-3mdv2009.0
+ Revision: 218439
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Use rpm macros

* Wed Apr 02 2008 Erwan Velu <erwan@mandriva.org> 0.5.4-3mdv2008.1
+ Revision: 191684
- Fixing menu icon

* Wed Apr 02 2008 Erwan Velu <erwan@mandriva.org> 0.5.4-2mdv2008.1
+ Revision: 191595
- Fixing buildrequires
- Finishing menu entry

  + Anne Nicolas <ennael@mandriva.org>
    - Add menu entry
      Increase release

* Wed Apr 02 2008 Erwan Velu <erwan@mandriva.org> 0.5.4-1mdv2008.1
+ Revision: 191550
- 0.5.4
  Splitting applet in another rpm

* Sat Mar 01 2008 Erwan Velu <erwan@mandriva.org> 0.5.2-1mdv2008.1
+ Revision: 177155
- 0.5.2

* Thu Feb 28 2008 Erwan Velu <erwan@mandriva.org> 0.5.2-0.20080228.1mdv2008.1
+ Revision: 176211
- Fixing requires (thx neocluster)
  Fixes bug #120 and #121

* Tue Feb 26 2008 Erwan Velu <erwan@mandriva.org> 0.5.2-0.2008025.3mdv2008.1
+ Revision: 175360
- Fixing tagpy dependency
  Fixing Summary
  Fixing Group

* Mon Feb 25 2008 Erwan Velu <erwan@mandriva.org> 0.5.2-0.2008025.2mdv2008.1
+ Revision: 175175
- More and more Requires
- Adding more requires
- Adding requires

* Mon Feb 25 2008 Erwan Velu <erwan@mandriva.org> 0.5.2-0.2008025mdv2008.1
+ Revision: 175063
- 0.5.2 (svn 20080225)

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - fix description-line-too-long

* Mon Jan 28 2008 Erwan Velu <erwan@mandriva.org> 0.5.0-2mdv2008.1
+ Revision: 159483
- Adding more restrictive buildrequires

* Sun Jan 27 2008 Helio Chissini de Castro <helio@mandriva.com> 0.5.0-1mdv2008.1
+ Revision: 158840
- import python-coherence


