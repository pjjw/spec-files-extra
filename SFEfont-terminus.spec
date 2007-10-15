#
# spec file for package SFEfont-terminus
#

%include Solaris.inc
Name:                    SFEfont-terminus
Summary:                 terminus - font terminus
URL:                     http://www.is-vn.bg/hamster
Version:                 4.20
Source:                  http://www.is-vn.bg/hamster/terminus-font-%{version}.tar.gz
Patch1:                  terminus-font-01-x11dir.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n terminus-font-%version
%patch1 -p1

%build

# CXXFLAGS='-library=stlport4')

PATH=$PATH:/usr/openwin/bin:/usr/X11/bin

./configure --prefix=%{_prefix}  \
            --x11dir=%{_prefix}/openwin/lib/X11/fonts/pcf

#make psf
#make txt
#make raw
make pcf


%install
rm -rf $RPM_BUILD_ROOT


make install DESTDIR=$RPM_BUILD_ROOT

#make install-acm DESTDIR=$RPM_BUILD_ROOT
#make install-psf DESTDIR=$RPM_BUILD_ROOT
#make install-uni DESTDIR=$RPM_BUILD_ROOT
#make install-ref DESTDIR=$RPM_BUILD_ROOT
#make install.raw DESTDIR=$RPM_BUILD_ROOT
#make install-raw DESTDIR=$RPM_BUILD_ROOT
make install-pcf DESTDIR=$RPM_BUILD_ROOT
#make install-12b DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


### TODO: post-intall-script with cd /usr/openwin/lib/X11/fonts/pcf; mkfontdir `pwd`
###make fontdir 


%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_basedir}/openwin/lib/X11/fonts/pcf
%{_basedir}/openwin/lib/X11/fonts/pcf/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*


%changelog
* Sun Oct 14 2007 - laca@sun.com
- add /usr/X11/bin to PATH for FOX build
* Sat May 12 2007 - Thomas Wagner
- Initial spec
