#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define        major      1
%define        minor      34
%define        patchlevel 1
%define src_url http://easynews.dl.sourceforge.net/sourceforge/boost

Name:                SFEboost-gpp
Summary:             Boost - free peer-reviewed portable C++ source libraries (g++-built)
Version:             %{major}.%{minor}.%{patchlevel}
License:             Boost Software License
Source:              %{src_url}/boost_%{major}_%{minor}_%{patchlevel}.tar.bz2
Patch1:              boost-01-studio.diff
Patch2:              boost-02-gcc34.diff
URL:                 http://www.boost.org/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWicu
BuildRequires: SUNWPython
Requires: SUNWicu

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%prep
%setup -q -n boost_%{major}_%{minor}_%{patchlevel}
%patch1 -p1
%patch2 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags"

BOOST_ROOT=`pwd`
TOOLSET=gcc
PYTHON_VERSION=`python -c "import sys; print (\"%%d.%%d\" %% (sys.version_info[0], sys.version_info[1]))"`
PYTHON_ROOT=`python -c "import sys; print sys.prefix"`

# Overwrite user-config.jam
cat > user-config.jam <<EOF
# Compiler configuration
import toolset : using ;
using $TOOLSET : : $CXX : <cxxflags>"$CXXFLAGS" <linkflags>"$LDFLAGS" <linker-type>sun ; 

# Python configuration
using python : $PYTHON_VERSION : $PYTHON_ROOT ;
EOF

# Build bjam
cd "tools/jam/src" && ./build.sh "$TOOLSET"
cd $BOOST_ROOT

# Build Boost
BJAM=`find tools/jam/src -name bjam -a -type f`
$BJAM --v2 -j$CPUS -sBUILD="release <threading>single/multi" -sICU_PATH=/usr \
  --layout=system --user-config=user-config.jam release stage

%install
BOOST_ROOT=`pwd`
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_cxx_libdir}

for i in stage/lib/*.a; do
  cp $i $RPM_BUILD_ROOT%{_cxx_libdir}
done
for i in stage/lib/*.so; do
  NAME=`basename $i`
  cp $i $RPM_BUILD_ROOT%{_cxx_libdir}/$NAME.%{version}
  ln -s $NAME.%{version} $RPM_BUILD_ROOT%{_cxx_libdir}/$NAME
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*.a

%changelog
* Wed Apr 23 2008 - laca@sun.com
- create, based on SFEboost.spec
- force building with g++ and install the libs to /usr/lib/g++/<version>
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Comment out SUNWicud dependency to get module to build.
* Mon Aug 13 2007 - trisk@acm.jhu.edu
- Initial version
