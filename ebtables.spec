%define	name	ebtables
%define realver 2.0.8-1
%define version %(echo %realver | sed 's/-/_/')
%define release %mkrel 2

%define _ssp_cflags %nil

Summary:	A filtering tool for a bridging firewall
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		%{name}-v%{realver}.tar.gz
Group:		System/Kernel and hardware
URL:		http://ebtables.sourceforge.net/
License:	GPL
#BuildRequires:  kernel-source >= 2.6.0
Requires:	kernel >= 2.6.0
BuildRoot:	%{_tmppath}/%{name}-v%{version}-root

%description
The ebtables program is a filtering tool for a bridging firewall.
The filtering is focussed on the Link Layer Ethernet frame fields.
Apart from filtering, it also gives the ability to alter the
Ethernet MAC addresses and implement a brouter. 

%prep

%setup -q -n %{name}-v%{realver}

%build

#make CFLAGS="%{optflags} -fPIC" LIBDIR=/%{_lib}
%make \
    CFLAGS="%{optflags} -fPIC"
    LIBDIR=/%_lib/ebtables \

%if %{?_with_static:1}%{?!_with_static:0}
%make \
    CFLAGS="%{optflags} -fPIC" \
    LIBDIR=/%_lib/ebtables \
    static
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}/sbin

%if %{?_with_static:1}%{?!_with_static:0}
%{__install} -D -m0755 static %{buildroot}/sbin/ebtables-static
%endif
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


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc ChangeLog INSTALL THANKS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ethertypes
%attr(0755,root,root) /sbin/*
%attr(0644,root,root) %{_mandir}/man8/ebtables.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/ebtables-config
%config %{_initrddir}/ebtables
/%_lib/ebtables
