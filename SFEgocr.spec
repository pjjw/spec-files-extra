#
# spec file for package SFEgocr
#
#
%include Solaris.inc

Name:                    SFEgocr
Summary:                 GOCR Optical Character Recognition package.
Version:                 0.45
Source:                  http://www-e.uni-magdeburg.de/jschulen/ocr/gocr-%{version}.tar.gz
URL:                     http://jocr.sourceforge.net/download.html
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
License:	             GPL
Group:		             Graphics


%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n gocr-%{version}

%description
GOCR is an optical character recognition program. 
It reads images in many formats  and outputs a text file.
Possible image formats are pnm, pbm, pgm, ppm, some pcx and
tga image files. Other formats like pnm.gz, pnm.bz2, png, jpg, tiff, gif,
bmp will be automatically converted using the netpbm-progs, gzip and bzip2
via unix pipe.
A simple graphical frontend written in tcl/tk and some
sample files (you need transfig for the sample files) are included.
Gocr is also able to recognize and translate barcodes.
You do not have to train the program or store large font bases.
Simply call gocr from the command line and get your results.



%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --bindir=%{_prefix}/bin \
	        --sbindir=%{_prefix}/sbin \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
	        --includedir=%{_prefix}/include

make

%install
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

#%dir %attr (0755, root, bin) /bin
#/bin/*

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*


%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/lib*

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

#%dir %attr (0755, root, bin) %{_includedir}
#%{_includedir}/*


%changelog
- Sat Feb 2 2008 - pradhap (at) gmail.com
- Initial gocr spec file

