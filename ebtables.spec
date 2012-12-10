%define realver 2.0.10-4
%define version 2.0.10.4

Summary:	A filtering tool for a bridging firewall
Name:		ebtables
Version:	%{version}
Release:	%mkrel 2
Group:		System/Kernel and hardware
License:	GPLv2+
Source0:	%{name}-v%{realver}.tar.gz
# Add patch0 from fedora (fix permission install)
Patch0:		ebtables-2.0.8-norootinst.patch
Patch1:		ebtables-2.0.10-lsb.patch
URL:		http://ebtables.sourceforge.net/

%description
The ebtables program is a filtering tool for a bridging firewall.
The filtering is focussed on the Link Layer Ethernet frame fields.
Apart from filtering, it also gives the ability to alter the
Ethernet MAC addresses and implement a brouter. 

%prep
%setup -q -n %{name}-v%{realver}
%patch0 -p0 -b .nonroot-install
%patch1 -p1 -b .lsb

%build
%make \
    CFLAGS="%{optflags} -fPIC" \
    LIBDIR=/%_lib/ebtables BINDIR="/sbin" MANDIR="%{_mandir}"

%if %{?_with_static:1}%{?!_with_static:0}
%make \
    CFLAGS="%{optflags} -fPIC" \
    LIBDIR=/%_lib/ebtables \
    static
%endif

%install
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}/sbin
install -d %{buildroot}%{_initrddir}

%makeinstall_std LIBDIR="/%{_lib}/ebtables" BINDIR="/sbin"  MANDIR="%{_mandir}"
%{__install} -D -m0644 ethertypes %{buildroot}%{_sysconfdir}/ethertypes 

%if %{?_with_static:1}%{?!_with_static:0}
%{__install} -D -m0755 static %{buildroot}/sbin/ebtables-static
%endif

sed -i "s|__EXEC_PATH__|/sbin|g" ebtables-save
%{__install} -m 0755 ebtables-save %{buildroot}/sbin/ebtables-save

sed -i "s|__EXEC_PATH__|/sbin/|g" ebtables.sysv; 
sed -i "s|__SYSCONFIG__|%_sysconfdir/sysconfig|g" ebtables.sysv
%{__install} -m 0755 ebtables.sysv %{buildroot}%{_initrddir}/ebtables

sed -i "s|__SYSCONFIG__|%_sysconfdir/sysconfig|g" ebtables-config
%{__install} -m 0600 ebtables-config %{buildroot}%{_sysconfdir}/sysconfig/ebtables-config



%files
%defattr(-,root,root,0755)
%doc ChangeLog INSTALL THANKS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ethertypes
%attr(0755,root,root) /sbin/ebtables
%attr(0755,root,root) /sbin/ebtables-save
%attr(0755,root,root) /sbin/ebtables-restore
%attr(0644,root,root) %{_mandir}/man8/ebtables.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/ebtables-config
%config %{_initrddir}/ebtables
/%_lib/ebtables
