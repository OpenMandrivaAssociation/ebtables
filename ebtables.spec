%define realver 2.0.10-4
%define version 2.0.10.4

%define _ssp_cflags %nil

Summary:	A filtering tool for a bridging firewall
Name:		ebtables
Version:	%{version}
Release:	1
Group:		System/Kernel and hardware
License:	GPL
Source0:	%{name}-v%{realver}.tar.gz
URL:		http://ebtables.sourceforge.net/
Patch0:		makefiles_0644_mode.diff
%description
The ebtables program is a filtering tool for a bridging firewall.
The filtering is focussed on the Link Layer Ethernet frame fields.
Apart from filtering, it also gives the ability to alter the
Ethernet MAC addresses and implement a brouter. 

%prep
%setup -q -n %{name}-v%{realver}
%patch0 -p1

%build
#make CFLAGS="%{optflags} -fPIC" LIBDIR=/%{_lib}
#%make \
#    CFLAGS="%{optflags} -fPIC"
#    LIBDIR=/%_lib/ebtables \
 sed -i -e "s,^MANDIR:=.*,MANDIR:=/usr/share/man," \
        -e "s,^BINDIR:=.*,BINDIR:=/sbin," \
        -e "s,^INITDIR:=.*,INITDIR:=/usr/share/doc/%{name}," \
        -e "s,^SYSCONFIGDIR:=.*,SYSCONFIGDIR:=/usr/share/doc/%{name}," \
        -e "s,^LIBDIR:=.*,LIBDIR:=/lib/\$(PROGNAME)," Makefile

%make CFLAGS="%{optflags} -fPIC"

%install
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}/sbin

%{__install} -D -m0755 ebtables %{buildroot}/sbin/ebtables
%{__install} -D -m0755 ebtables-restore %{buildroot}/sbin/ebtables-restore
%{__install} -D -m0644 ethertypes %{buildroot}%{_sysconfdir}/ethertypes
%{__install} -D -m0644 ebtables.8 %{buildroot}%{_mandir}/man8/ebtables.8
%{__mkdir} -p %{buildroot}/%_lib/ebtables/
%{__mkdir} -p %{buildroot}/sbin
%{__mkdir} -p %{buildroot}%{_initrddir}
%{__mkdir} -p %{buildroot}%{_mysysconfdir}
%{__install} -m0755 extensions/*.so %{buildroot}/%{_lib}/ebtables/
%{__install} -m0755 *.so %{buildroot}/%{_lib}/ebtables/

export __iets=`printf '/sbin' | sed 's/\\//\\\\\\//g'`
export __iets2=`printf '%_sysconfdir/sysconfig' | sed 's/\\//\\\\\\//g'`

sed -i "s/__EXEC_PATH__/$__iets/g" ebtables-save
%{__install} -m 0755 ebtables-save %{buildroot}/sbin/ebtables-save
sed -i "s/__EXEC_PATH__/$__iets/g" ebtables.sysv; sed -i "s/__SYSCONFIG__/$__iets2/g" ebtables.sysv
%{__install} -m 0755 ebtables.sysv %{buildroot}%{_initrddir}/ebtables
sed -i "s/__SYSCONFIG__/$__iets2/g" ebtables-config
%{__install} -m 0600 ebtables-config %{buildroot}%{_sysconfdir}/sysconfig/ebtables-config

unset __iets
unset __iets2

%files
%doc ChangeLog INSTALL THANKS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ethertypes
%attr(0755,root,root) /sbin/ebtables
%attr(0755,root,root) /sbin/ebtables-save
%attr(0755,root,root) /sbin/ebtables-restore
%attr(0644,root,root) %{_mandir}/man8/ebtables.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/ebtables-config
%config %{_initrddir}/ebtables
/%_lib/ebtables
