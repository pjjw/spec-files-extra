#
# spec file for package SFEbrlcad
#
# includes module(s): brlcad
#
%include Solaris.inc

Name:                    SFEbrlcad
Summary:                 The BRL-CAD package is a powerful Constructive Solid Geometry (CSG) solid modeling system with over 20 years development and production use by the U.S. military. 
Version:                 7.10.4
Source:                  %{sf_download}/brlcad/brlcad-%{version}.tar.bz2
URL:                     http://brlcad.org
Group:                   Productivity/Graphics/CAD
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n brlcad-%version

%build

bash autogen.sh

LDFLAGS='-lnsl -lsocket' ./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
	        --with-ldflags='-lnsl -lsocket'
gmake 

%install
gmake install DESTDIR=$RPM_BUILD_ROOT
DOC="$RPM_BUILD_ROOT/usr/share"
cp "$RPM_BUILD_ROOT/usr/share/COPYING" "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/AUTHORS" "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/INSTALL" "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/HACKING" "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/NEWS"    "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/README"  "$DOC/doc"

rm "$RPM_BUILD_ROOT/usr/share/COPYING"
rm "$RPM_BUILD_ROOT/usr/share/AUTHORS"
rm "$RPM_BUILD_ROOT/usr/share/INSTALL"
rm "$RPM_BUILD_ROOT/usr/share/HACKING"
rm "$RPM_BUILD_ROOT/usr/share/NEWS"   
rm "$RPM_BUILD_ROOT/usr/share/README" 

mkdir "$DOC/brlcad"
mv "$DOC"/doc/* "$DOC"/brlcad
mv "$DOC"/brlcad "$DOC"/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

#%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man5/*
%dir %attr(0755, root, bin) %{_mandir}/mann/*

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%dir %attr(0755, root, bin) %{_datadir}/tclscripts
%{_datadir}/tclscripts/*

%dir %attr(0755, root, bin) %{_datadir}/db
%{_datadir}/db/*

%dir %attr(0755, root, bin) %{_datadir}/pix
%{_datadir}/pix/*

%dir %attr(0755, root, bin) %{_datadir}/html
%{_datadir}/html/*

%dir %attr(0755, root, bin) %{_datadir}/awf
%{_datadir}/awf/*

%dir %attr(0755, root, bin) %{_datadir}/plugins
%{_datadir}/plugins/*

%dir %attr(0755, root, bin) %{_datadir}/sample_applications
%{_datadir}/sample_applications/*

%dir %attr(0755, root, bin) %{_datadir}/vfont
%{_datadir}/vfont/*

#%dir %attr(0755, root, bin) %{_datadir}/brlcad
#%{_datadir}/brlcad/*

%dir %attr(0755, root, bin) %{_datadir}/doc/brlcad
%{_datadir}/doc/brlcad/*


%changelog
- Tue Feb 5 2007 - pradhap (at) gmail.com
- Initial brlcad spec file.

