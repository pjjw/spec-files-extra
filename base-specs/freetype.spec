#
# spec file for package freetype
#
# includes module(s): freetype
#
%define src_name     freetype
%define src_url	     http://savannah.nongnu.org/download/%{src_name}

Name:                freetype
Summary:             Freetype
Version:             2.3.5
Source:              %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		     freetype-01-options.diff

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"


bash ./autogen.sh
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --libdir=%{_libdir}			\
	    --includedir=%{_includedir}		\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Yuk. Some apps still need the internal headers :(
( cd include
  find freetype/internal | cpio -pdm $RPM_BUILD_ROOT%{_includedir}/freetype2
)

rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Aug 15 2007 - trisk@acm.jhu.edu
- Bump to 2.3.5
* Tue Jun  5 2007 - Doug Scott
- Change to isabuild
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial spec - some apps need modern freetype
