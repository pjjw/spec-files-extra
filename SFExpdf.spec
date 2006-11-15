# Because JDS has the gnome pdf viewer which is based on xpdf, there is
# a little bit of overlap between that implementation and this one, however
# IMO there are more than enough differences to justify offering a
# separate spec file for ordinary xpdf.
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFExpdf
Summary:             Open source viewer for PDF files
Version:             3.01
Source:              ftp://ftp.foolabs.com/pub/xpdf/xpdf-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWxwplt
BuildRequires: SUNWxwxft

Requires: SUNWxwplt
Requires: SUNWxwxft

%prep
%setup -q -n xpdf-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/sfw/include/freetype2 -I/usr/sfw/include"
export CPPFLAGS="-I/usr/sfw/include -I/usr/sfw/include/freetype2"
export CXXFLAGS="%cxx_optflags -I/usr/sfw/include/freetype2 -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

# The source hard-codes (in GlobalParams.cc) a list of directories to
# scan for ghostscript fonts; unfortunately it still doesn't find them on
# OpenSolaris. The following on-the-fly patch fixes that. Alternatively
# one can specify font locations in $HOME/.xpdfrc. A template .xpdfrc is
# in doc/sample-xpdfrc (in the source distribution).

perl -i.orig -lpe 's/local/sfw/ if m|/usr/local/share/ghostscript/fonts|' xpdf/GlobalParams.cc

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Omit the etc/xpdfrc file from this package because SUNWgnome-pdf-viewer
# (which is based on xpdf) already installs it. However, see the comments 
# above about using $HOME/.xpdfrc.

rm $RPM_BUILD_ROOT/usr/etc/xpdfrc
rmdir $RPM_BUILD_ROOT/usr/etc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man?
%{_mandir}/man?/*

%changelog
* 
* Tue Nov 14 2006 - Eric Boutilier
- Initial spec
