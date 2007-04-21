#
# spec file for package doxygen
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:           doxygen
License:        GPL
Version:        1.5.2
URL:            http://ftp.stack.nl/pub/users/dimitri
Summary:        Doxygen is a documentation system for various programming languages
Source:         http://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.gz
Patch1:		doxygen-01-iconv.diff
Patch2:		doxygen-02-nameconflict.diff
Patch3:		doxygen-03-solaris.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc

%package devel
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix %{_prefix}		\
	    --platform solaris-cc	\
	    --docdir %{_datadir}/doc	\
	    --release			\
	    --shared

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Apr 21 2007 - dougs@truemail.co.th
- Initial version
