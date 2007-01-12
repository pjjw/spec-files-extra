#
# spec file for package SFEtightvnc
#
# includes module(s): tightvnc
#
%include Solaris.inc

Name:                    SFEtightvnc
Summary:                 tightvnc - remote control software package derived from the popular VNC software
Version:                 1.2.9
Source:                  http://mesh.dl.sourceforge.net/sourceforge/vnc-tight/tightvnc-%{version}_unixsrc.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Requires: SUNWxwrtl
#Requires: SUNWzlib
#Requires: SUNWlibms
BuildRequires: SUNWxwopt

%prep
%setup -q -n vnc_unixsrc

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PATH=/usr/openwin/bin:${PATH}
export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags"
cd Xvnc
./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}                 \
	    --mandir=%{_mandir}
	    
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Fri Jan 12 2007 - daymobrew@users.sourceforge.net
- Initial spec

