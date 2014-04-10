%define _disable_ld_no_undefined 1
%define fversion 2.0.10-4

Name:		ebtables
Version:	2.0.10.4
Release:	10
Summary:	Ethernet Bridge frame table administration tool
License:	GPLv2+
Group:		System/Base
URL:		http://ebtables.sourceforge.net/
Source0:	http://downloads.sourceforge.net/ebtables/ebtables-v%{fversion}.tar.gz
Source1:	ebtables-save
Source2:	ebtables.systemd
Source3:	ebtables.service
Patch0:		ebtables-2.0.10-norootinst.patch
Patch3:		ebtables-2.0.9-lsb.patch
Patch4:		ebtables-2.0.10-linkfix.patch
Patch5:		ebtables-2.0.0-audit.patch
Patch6:		05link_with_no-as-needed.patch
BuildRequires:	systemd-units
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper

%description
Ethernet bridge tables is a firewalling tool to transparently filter network
traffic passing a bridge. The filtering possibilities are limited to link
layer filtering and some basic filtering on higher network layers.

This tool is the userspace control for the bridge and ebtables kernel
components (built by default in Fedora kernels).

The ebtables tool can be used together with the other Linux filtering tools,
like iptables. There are no known incompatibility issues.

%prep
%setup -q -n ebtables-v%{fversion}
%patch0 -p1 -b .norootinst
%patch3 -p1 -b .lsb
# extension modules need to link to libebtc.so for ebt_errormsg
%patch4 -p1 -b .linkfix
%patch5 -p1 -b .AUDIT
%patch6 -p1 -b .noasneeded

# Convert to UTF-8
f=THANKS; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f


%build
%setup_compile_flags

sed -i -e "s,^MANDIR:=.*,MANDIR:=%{_mandir}," \
        -e "s,^BINDIR:=.*,BINDIR:=/sbin," \
        -e "s,^LIBDIR:=.*,LIBDIR:=/%{_lib}/\$(PROGNAME)," Makefile
%make \
    CFLAGS="%{optflags} -fPIC" \
    LIBDIR=/%{_lib} BINDIR="/sbin" MANDIR="%{_mandir}"


%install
mkdir -p %{buildroot}%{_unitdir}
install -p %{SOURCE3} %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_prefix}/libexec
install -m0755 %{SOURCE2} %{buildroot}%{_prefix}/libexec/ebtables
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
make DESTDIR="%{buildroot}" LIBDIR="/%{_lib}" BINDIR="/sbin" MANDIR="%{_mandir}" install
touch %{buildroot}%{_sysconfdir}/sysconfig/ebtables.filter
touch %{buildroot}%{_sysconfdir}/sysconfig/ebtables.nat
touch %{buildroot}%{_sysconfdir}/sysconfig/ebtables.broute

# Do not need the sysvinit
rm -rf %{buildroot}%{_initrddir}

# install ebtables-save bash script
rm -f %{buildroot}/sbin/ebtables-save
install %{SOURCE1} %{buildroot}/sbin/ebtables-save

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_service %{name} 

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING THANKS
%doc %{_mandir}/man8/ebtables.8*
%config(noreplace) %{_sysconfdir}/ethertypes
%config(noreplace) %{_sysconfdir}/sysconfig/ebtables-config
%{_unitdir}/ebtables.service
%{_prefix}/libexec/ebtables
/%{_lib}/*.so
/sbin/ebtables*
%ghost %{_sysconfdir}/sysconfig/ebtables.filter
%ghost %{_sysconfdir}/sysconfig/ebtables.nat
%ghost %{_sysconfdir}/sysconfig/ebtables.broute
