# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	speex
%define src_version	1.0.5
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	SFE%{src_name}
Summary:      	Speex: A Free Codec For Free Speech
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	BSD license
Source:         http://downloads.xiph.org/releases/speex/%{src_name}-%{version}.tar.gz
#Patch:        	yourpatch-name
URL:            http://www.speex.org
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

#Requires:      
#BuildRequires: 
BuildConflict: SUNWspeex

%description 
Speex is an Open Source/Free Software  patent-free audio compression format designed for speech. The Speex Project aims to lower the barrier of entry for voice applications by providing a free alternative to expensive proprietary speech codecs. Moreover, Speex is well-adapted to Internet applications and provides useful features that are not present in most other codecs.

 Speex is based on CELP  and is designed to compress voice at bitrates ranging from 2 to 44 kbps. Some of Speex's features include:

    * Narrowband (8 kHz), wideband (16 kHz), and ultra-wideband (32 kHz) compression in the same bitstream
    * Intensity stereo encoding
    * Packet loss concealment
    * Variable bitrate operation (VBR)
    * Voice Activity Detection (VAD)
    * Discontinuous Transmission (DTX)
    * Fixed-point port
    * Acoustic echo canceller
    * Noise suppression

Note that Speex has a number of features that are not present in other codecs, such as intensity stereo encoding, integration of multiple sampling rates in the same bitstream (embedded coding), and a VBR mode;

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix}

#%patch0 -p 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
make

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File permissions, ownership information. Note the difference between 
# bin(_bindir),share(_datadir) & share/applications
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, sys) %{_libdir}
%{_libdir}/*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/man
%{_datadir}/doc
%{_datadir}/aclocal

#%dir %attr (0755, root, other) %{_datadir}/applications
#%{_datadir}/applications/*


%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add BuildConflicts SUNWspeex.
* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
